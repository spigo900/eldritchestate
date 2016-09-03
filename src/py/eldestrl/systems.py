import logging
import random
import tdl
import tdl.event as ev
import tdl.map as mapfn
from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity
import eldestrl.map as emap
import eldestrl.tiles as tiles
import eldestrl.input as eldinput
import eldestrl.lighting as light
import eldestrl.components as comp
import eldestrl.utils as utils
import eldestrl.ui.events as uievents
import eldestrl.ui.states as uistates


class UpdateWorldSys(System):
    def update(self, dt):
        from eldestrl.components import World, Position
        ent_mgr = self.entity_manager
        new_ents = {}
        for (entity, world) in ent_mgr.pairs_for_type(World):
            try:
                coords = ent_mgr.component_for_entity(entity, Position).coords
                if not new_ents.get(coords, None):
                    new_ents[coords] = []
                new_ents[coords].append(entity)
            except NonexistentComponentTypeForEntity:
                print('Entity %s has world but no position! Skipping...'
                      % repr(entity))
        world.ents = new_ents


class LightingSys(System):
    def __init__(self, output_map):
        self.output_map = output_map
        super(LightingSys, self).__init__()

    def update(self, dt):
        from eldestrl.components import Position, LightSource
        ent_mgr = self.entity_manager

        sources = {(x, y): [emap.get_tile_type(self.output_map, self.output_map[x, y])]
                   for (x, y) in self.output_map
                   if "light_properties" in
                   emap.get_tile_type(self.output_map, self.output_map[x, y])}

        for (entity, source) in ent_mgr.pairs_for_type(LightSource):
            try:
                coords = ent_mgr.component_for_entity(entity, Position).coords
                sources.setdefault(coords, []).append(source.props)
            except NonexistentComponentTypeForEntity:
                print('Entity %s has world but no position! Skipping...'
                      % repr(entity))

        light_map = {(x, y): 0.2 for (x, y) in self.output_map}
        for (x1, y1), srcs in sources.items():
            for src in srcs:
                coordset = (x1 - src['radius'], y1 - src['radius'],
                            x1 + src['radius'], y1 + src['radius'])
                points_checked = utils.hollow_box(*coordset)
                minimap = {}

                for (x2, y2) in points_checked:
                    line = [(x, y) for (x, y)
                            in utils.bresenham_line(x1, y1, x2, y2)
                            if (x, y) in self.output_map]
                    if not line:
                        continue
                    if len(line) > 2:
                        line = utils.remove_duplicates(line)
                    lights = light.light_line(
                        1.0, line, light.lighting_linear,
                        lambda x, y: emap.light_attenuation(self.output_map, x, y))
                    minimap.update(zip(line, lights))

                for pos, intensity in minimap.items():
                    light_map[pos] = max(light_map[pos], minimap[pos])
        self.output_map.light_map = light_map


class FOVSys(System):
    def update(self, dt):
        ent_mgr = self.entity_manager
        for (entity, sight) in ent_mgr.pairs_for_type(comp.Sight):
            try:
                world_map = ent_mgr.component_for_entity(entity, comp.World) \
                                   .world
                x, y = ent_mgr.component_for_entity(entity, comp.Position) \
                              .coords

                def transparent(x, y):
                    return not emap.blocks_sight(world_map, x, y)

                fov = mapfn.quick_fov(x, y, transparent, radius=sight.radius)
                sight.in_sight = \
                    set(tile for tile in fov if
                        world_map.light_map.get(tile, 0.0) >= sight.min_light)
            except NonexistentComponentTypeForEntity:
                print('Entity %s ! Skipping...'
                      % repr(entity))


class FOWSys(System):
    def update(self, dt):
        ent_mgr = self.entity_manager
        for (entity, _) in ent_mgr.pairs_for_type(comp.PlayerControlled):
            try:
                world_map = ent_mgr.component_for_entity(entity, comp.World) \
                                   .world
                sight = ent_mgr.component_for_entity(entity, comp.Sight)
                world_map.seen |= sight.in_sight
            except NonexistentComponentTypeForEntity:
                pass


class FogSys(System):
    MAX_FOG = 15
    RUN_TICKS = 100
    def __init__(self, map_size):
        (x_size, y_size) = map_size
        map_init = {(x, y): random.randint(0, self.MAX_FOG)
                    for x in range(x_size)
                    for y in range(y_size)}

        self._sources = set((x, y)
            for x in range(x_size)
            for y in range(y_size)
                            if random.random() < 0.05)

        self.map_a = map_init
        self.map_b = self.map_a.copy()

        self.ticks = 0

        super(FogSys, self).__init__()

    def update(self, dt):
        ent_mgr = self.entity_manager
        ortho_adjacents = utils.ortho_adjacent_tiles
        if self.ticks < self.RUN_TICKS:
            # print(dt)
            self.ticks += dt
            return
        else:
            self.ticks -= self.RUN_TICKS
        for coord_pair in self._sources:
            # if self.map_b[coord_pair] < 15:
            #     print(self.map_b[coord_pair])
            self.map_b[coord_pair] = min(self.MAX_FOG, self.map_a[coord_pair] + 1)
        for coord_pair in self.map_b:
            (x, y) = coord_pair
            self.map_b[coord_pair] = (max(0, self.map_a[coord_pair] - 2))
            filtered_adj = [pair for pair in ortho_adjacents(coord_pair)
                            if pair in self.map_b]
            rand_adj = random.choice(filtered_adj)
            # transfer_amt = random.randint(1, 2)
            transfer_amt = 1
            if rand_adj:
                # self.map_b[coord_pair] -= (transfer_amt - 1)
                self.map_b[rand_adj] = min(self.MAX_FOG, self.map_b[rand_adj] + transfer_amt)
        tmp = self.map_a
        self.map_a = self.map_b
        self.map_b = tmp

    def get_fogmap(self):
        return self.map_a.items()


class FollowEntitySys(System):
    def update(self, dt):
        from eldestrl.components import Position, FollowsEntity
        ent_mgr = self.entity_manager
        for (entity, follower) in ent_mgr.pairs_for_type(FollowsEntity):
            pos = ent_mgr.component_for_entity(entity, Position)
            followed_pos = ent_mgr.component_for_entity(follower.followed,
                                                        Position)
            pos.coords = followed_pos.coords


class EventSys(System):
    def __init__(self, con_width, con_height):
        self.game_ended = False
        self.initialized = False
        self.ui_console = tdl.Console(con_width, con_height)
        self.ui_states = []
        super(EventSys, self).__init__()

    def initialize(self):
        self.ui_states.append(uistates.Play(self.ui_console,
                                            self.entity_manager))
        self.initialized = True

    def update(self, dt):
        if not self.initialized:
            self.initialize()
        events = ev.get()
        for event in events:
            if event.type == "KEYUP":
                continue
            elif event.type == "NEWSTATE":
                self.ui_states.append(event.state)
                continue
            elif event.type == "DONECURSTATE" or event.type == "ESCAPESTATE":
                self.ui_states.pop()
                continue
            if self.ui_states:
                cur_state = self.ui_states[-1]
                cur_state.handle_event(event)
        if not self.ui_states:
            self.game_ended = True


class AISys(System):
    def update(self, dt):
        import eldestrl.ai.types as aitypes
        from eldestrl.components import AI
        ent_mgr = self.entity_manager
        for (ent, ai_comp) in ent_mgr.pairs_for_type(AI):
            if ai_comp.type.startswith("_"):
                raise Exception("Illegal AI type for entity {}! "
                                "Tried to use private function {} as AI type!"
                                .format(ent, ai_comp.type))
            ai_function = getattr(aitypes, ai_comp.type)
            ai_function(ent_mgr, ent)


class ActorSys(System):
    def update(self, dt):
        from eldestrl.components import Actor, World, Position, BlocksMove
        from operator import add
        ent_mgr = self.entity_manager
        ent_pairs = tuple(ent_mgr.pairs_for_type(Actor))
        shortest = min(len(actor.queue) for (_, actor) in ent_pairs)
        for i in range(shortest):
            for (entity, actor) in ent_pairs:
                try:
                    action = actor.queue.popleft()
                    if action[0] == 'do_action_tile':
                        entity_position = \
                            ent_mgr.component_for_entity(entity, Position)
                        pos = entity_position.coords
                        new_pos = tuple(map(add, pos, action[1]))
                        world_map = \
                            ent_mgr.component_for_entity(entity, World).world
                        blocked = False
                        ttype = emap.maybe_get_type(world_map,
                                                    world_map.get(
                                                        new_pos, None))
                        if not emap.passable(ent_mgr, world_map, new_pos):
                            blocked = True
                            tiles.maybe_do_action(
                                ent_mgr, entity, world_map, new_pos,
                                tiles.get_behavior(ttype, 'open'))
                        else:
                            for other_ent in world_map.ents.get(new_pos, []):
                                try:
                                    ent_mgr.component_for_entity(entity,
                                                                 BlocksMove)
                                    blocked = True
                                except NonexistentComponentTypeForEntity:
                                    pass
                        if not blocked:
                            entity_position.coords = new_pos
                            tiles.maybe_do_action(
                                ent_mgr, entity, world_map, new_pos,
                                tiles.get_behavior(ttype, 'enter'))
                except IndexError:
                    continue
                except NonexistentComponentTypeForEntity:
                    continue


class RenderDisplaySys(System):
    def __init__(self, fogmap):
        self.fogmap = fogmap
        super(RenderDisplaySys, self).__init__()

    def update(self, dt):
        from eldestrl.utils import to_local_coords
        from eldestrl.render import render_map
        from eldestrl.components import Char, Position, World, Display, Sight
        import tdl
        from tdl import TDLError
        ent_mgr = self.entity_manager
        for (player_ent, _) in ent_mgr.pairs_for_type(comp.PlayerControlled):
            try:
                sight = ent_mgr.component_for_entity(player_ent, Sight)
                fov = sight.in_sight
            except NonexistentComponentTypeForEntity:
                pos = ent_mgr.component_for_entity(player_ent, Position)
                fov = set(pos.coords)
            for (display_ent, display) in ent_mgr.pairs_for_type(Display):
                (display_x, display_y) = \
                    ent_mgr.component_for_entity(display_ent, Position).coords
                refpoint = (display_x - display.con.width // 2,
                            display_y - display.con.height // 2)
                try:
                    world_map = ent_mgr.component_for_entity(display_ent,
                                                             World).world
                    con = display.con
                except NonexistentComponentTypeForEntity:
                    print('Display entity %s has no associated world!'
                          % repr(display_ent))
                else:
                    con.clear()
                    render_map(con, world_map, refpoint, fov,
                               self.fogmap(), world_map.seen)
                    for (entity, renderinfo) in ent_mgr.pairs_for_type(Char):
                        try:
                            pos = \
                                ent_mgr.component_for_entity(entity, Position)
                            draw_x, draw_y = \
                                to_local_coords(refpoint, pos.coords)
                            lighting = world_map.light_map[pos.coords]
                            if not (draw_x, draw_y) in con or \
                               pos.coords not in fov:
                                continue
                            con.draw_char(
                                draw_x, draw_y,
                                renderinfo.char,
                                tuple(int(lighting * n)
                                      for n in renderinfo.color))
                        except NonexistentComponentTypeForEntity as err:
                            print('Entity %s has no %s; skipping...'
                                  % (repr(entity), str(err)))
                        except TDLError as err:
                            print('Got TDLError %s, skipping...' % str(err))
        tdl.flush()
