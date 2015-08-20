import logging
import untdl.event as ev
from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity
import eldestrl.map as emap
import eldestrl.tiles as tiles
import eldestrl.input as eldinput
import eldestrl.components as comp


class UpdateWorldSys(System):
    def update(self, dt):
        ent_mgr = self.entity_manager
        from eldestrl.components import World, Position
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


class FollowEntitySys(System):
    def update(self, dt):
        ent_mgr = self.entity_manager
        from eldestrl.components import Position, FollowsEntity
        for (entity, follower) in ent_mgr.pairs_for_type(FollowsEntity):
            pos = ent_mgr.component_for_entity(entity, Position)
            followed_pos = ent_mgr.component_for_entity(follower.followed,
                                                        Position)
            pos.coords = followed_pos.coords


class EventSys(System):
    def __init__(self):
        self.game_ended = False
        self.input_handlers = \
            {"do_action_tile": self.do_action_tile,
             "run_dir": self.run_dir,
             "quit": self.quit}
        super(EventSys, self).__init__()

    def _do_move_tile_common(self, player_ent, move_diff, action_type):
        assert (-1, -1) <= move_diff <= (1, 1)
        ent_mgr = self.entity_manager
        actor = ent_mgr.component_for_entity(player_ent, comp.Actor)
        actor.queue.append((action_type, move_diff))

    def do_action_tile(self, player_ent, move_diff):
        self._do_move_tile_common(player_ent, move_diff, 'do_action_tile')

    def run_dir(self, player_ent, move_diff):
        self._do_move_tile_common(player_ent, move_diff, 'run_dir')

    def quit(self, *_):
        self.game_ended = True

    def update(self, dt):
        from eldestrl.components import PlayerControlled
        ent_mgr = self.entity_manager
        events = ev.get()
        for event in events:
            if isinstance(event, ev.KeyUp) or event.type == "QUIT":
                return
            for (entity, _) in ent_mgr.pairs_for_type(PlayerControlled):
                action, *params = eldinput.get_action(event)
                try:
                    handler_fn = self.input_handlers[action]
                    handler_fn(entity, *params)
                except KeyError:
                    log = logging.getLogger(__name__)
                    log.info("Pressed unbound key {}.".format(event))
                except AttributeError as err:
                    print('AttributeError! Event was:' '\n'
                          '%s' '\n\n'
                          'Error was:'
                          '%s' '\n'
                          % (repr(event), repr(err)))
                except NonexistentComponentTypeForEntity as err:
                    print('Player-controlled entity %(entity)s'
                          'has no component %(component)s!'
                          % {'entity': str(err.entity),
                             'component': str(err.compoent_type)})


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
    def update(self, dt):
        from eldestrl.utils import to_local_coords
        from eldestrl.render import render_map
        from eldestrl.components import Char, Position, World, Display
        import untdl
        from untdl import TDLError
        ent_mgr = self.entity_manager
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
                render_map(con, world_map, refpoint)
                for (entity, renderinfo) in ent_mgr.pairs_for_type(Char):
                    try:
                        pos = ent_mgr.component_for_entity(entity, Position)
                        draw_x, draw_y = to_local_coords(refpoint, pos.coords)
                        if not (draw_x, draw_y) in con:
                            continue
                        con.draw_char(draw_x, draw_y,
                                      renderinfo.char, renderinfo.color)
                    except NonexistentComponentTypeForEntity as err:
                        print('Entity %s has no %s; skipping...'
                              % (repr(entity), str(err)))
                    except TDLError as err:
                        print('Got TDLError %s, skipping...' % str(err))
        untdl.flush()
