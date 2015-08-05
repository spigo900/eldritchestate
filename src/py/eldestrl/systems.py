from ecs.models import System
from ecs.exceptions import NonexistentComponentTypeForEntity


class UpdateWorldSys(System):
    def update(self, ent_mgr):
        from eldestrl.components import World, Position
        new_ents = {}
        for (entity, world) in ent_mgr.pairs_for_type(World):
            try:
                coords = ent_mgr.component_for_entity(entity, Position).coords
                new_ents[coords] = entity
            except NonexistentComponentTypeForEntity:
                print('Entity %s has world but no position! Skipping...'
                      % repr(entity))
        world.ents = new_ents


class FollowEntitySys(System):
    def update(self, ent_mgr):
        from eldestrl.components import Position, FollowsEntity
        for (entity, follower) in ent_mgr.pairs_for_type(FollowsEntity):
            pos = ent_mgr.component_for_entity(entity, Position)
            followed_pos = ent_mgr.component_for_entity(follower.followed,
                                                        Position)
            pos.coords = followed_pos.coords


class EventSys(System):
    def __init__(self):
        self.game_ended = False
        super(EventSys, self).__init__()

    def update(self, ent_mgr):
        import untdl.event as ev
        import eldestrl.input as eldinput
        from eldestrl.components import PlayerControlled, Actor
        events = ev.get()
        for event in events:
            if event.type == 'QUIT':
                self.game_ended = True
            for (entity, _) in ent_mgr.pairs_for_type(PlayerControlled):
                try:
                    move_diff = eldinput.get_move_diff(event)
                    if move_diff != (0, 0):
                        actor = ent_mgr.component_for_entity(entity, Actor)
                        actor.queue.push(('do_action_tile', move_diff))
                    elif event.keychar == 'ESCAPE' or \
                         event.alt and 'F4' in event.key:  # noqa
                        ev.push(ev.Quit())
                except AttributeError:
                    print('Got unknown event type %s!' % repr(event))
                except NonexistentComponentTypeForEntity as err:
                    print('Player-controlled entity %(entity)s'
                          'has no component %(component)s!'
                          % {'entity': str(err.entity),
                             'component': str(err.compoent_type)})


class ActorSys(System):
    def update(self, ent_mgr):
        from eldestrl.map import passable
        from eldestrl.components import Actor, World, Position, BlocksMove
        for (entity, actor) in ent_mgr.pairs_for_type(Actor):
            try:
                action = actor.queue.popleft()
                if action[0] == 'do_action_tile':
                    entity_position = ent_mgr.component_for_entity(entity,
                                                                   Position)
                    pos = entity_position.coords
                    new_pos = ((x1 + x2, y1 + y2)
                               for (x1, y1) in pos
                               for (x2, y2) in action[1])
                    world_map = ent_mgr.component_for_entity(entity, World) \
                                       .world
                    blocked = False
                    if not passable(world_map, new_pos[0], new_pos[1]):
                        blocked = True
                    else:
                        for other_ent in world_map.ents:
                            try:
                                ent_mgr.component_for_entity(entity,
                                                             BlocksMove)
                                blocked = True
                            except NonexistentComponentTypeForEntity:
                                pass
                    if not blocked:
                        entity_position.coords = new_pos
            except IndexError:
                print('Entity %s\'s action queue is empty, skipping...'
                      % repr(entity))
                continue
            except NonexistentComponentTypeForEntity:
                continue


class RenderDisplaySys(System):
    def update(self, ent_mgr):
        from eldestrl.utils import to_local_coords
        from eldestrl.render import render_map
        from eldestrl.components import Char, Position, World, Display
        import untdl
        from untdl import TDLError
        for (display_ent, display) in ent_mgr.pairs_for_type(Display):
            (display_x, display_y) = \
                ent_mgr.component_for_entity(display_ent, Position).coords
            refpoint = (display.con.width - display_x,
                        display.con.height - display_y)
            try:
                world_map = ent_mgr.component_for_entity(display_ent,
                                                         World).world
                con = display.con
                con.clear()
                render_map(con, world_map, refpoint)
            except NonexistentComponentTypeForEntity:
                print('Display entity %s has no associated world!'
                      % repr(display_ent))
            else:
                for (entity, renderinfo) in ent_mgr.pairs_for_type(Char):
                    try:
                        pos = ent_mgr.component_for_entity(entity, Position)
                        draw_x, draw_y = to_local_coords(refpoint, pos.coords)
                        con.draw_char(draw_x, draw_y,
                                      renderinfo.char, renderinfo.color)
                    except NonexistentComponentTypeForEntity as err:
                        print('Entity %s has no %s; skipping...'
                              % (repr(entity), str(err)))
                    except TDLError as err:
                        print('Got TDLError %s, skipping...' % str(err))
                untdl.flush()
