import random
import tdl.map
import eldestrl.map as eldmap
import eldestrl.components as comp
from eldestrl.utils import to_local_coords, has_component


def _flat_cost(pos, new_pos):
    x_diff, y_diff = tuple(a - b for (a, b) in zip(new_pos, pos))
    cost = sum(abs(x) for x in (x_diff, y_diff))
    if x_diff != 0 or y_diff != 0:
        return cost - min(x_diff, y_diff)
    else:
        return cost


def _client_choose_target(ent_mgr, ent):
    this_world = ent_mgr.component_for_entity(ent, comp.World).world

    # find player-controlled characters on the same map as us, the client
    def _valid(e):
        return has_component(ent_mgr, e[0], comp.World) and \
            has_component(ent_mgr, e[0], comp.PlayerControlled) and \
            ent_mgr.component_for_entity(e[0], comp.World).world == this_world

    ents = [target_ent
            for (target_ent, _) in filter(
                _valid, ent_mgr.pairs_for_type(comp.Position))]
    num_player_chars = len(ents)
    if num_player_chars < 1:
        return None
    elif num_player_chars == 1:
        return ents[0]
    elif num_player_chars > 1:
        chosen = random.randrange(0, num_player_chars)
        return ents[chosen]


def client(ent_mgr, ent):
    '''AI function for client NPCs.'''
    this_world = ent_mgr.component_for_entity(ent, comp.World).world
    this_pos = ent_mgr.component_for_entity(ent, comp.Position).coords
    actions = ent_mgr.component_for_entity(ent, comp.Actor).queue
    actions.clear()
    ai_comp = ent_mgr.component_for_entity(ent, comp.AI)
    target = ai_comp.target
    if not target:
        ai_comp.target = _client_choose_target(ent_mgr, ent)
        target = ai_comp.target

    def client_cost(new_x, new_y):
        return 1 if eldmap.passable(ent_mgr, this_world, (new_x, new_y)) else 0
    target_pos = ent_mgr.component_for_entity(target, comp.Position).coords
    target_x, target_y = target_pos
    distance = _flat_cost(this_pos, target_pos)
    if distance <= 5:
        actions.append(('do_action_tile', (random.randint(-1, 1),
                                           random.randint(-1, 1))))
        return
    pathfinder = tdl.map.AStar(eldmap.map_width(this_world),
                               eldmap.map_height(this_world),
                               client_cost, diagnalCost=1)
    path = pathfinder.get_path(this_pos[0], this_pos[1], target_x, target_y)
    if path:
        next_tile = to_local_coords(this_pos, path[0])
        actions.append(('do_action_tile', next_tile))


def _monster_choose_target(ent_mgr, ent):
    this_world = ent_mgr.component_for_entity(ent, comp.World).world
    sight = ent_mgr.component_for_entity(ent, comp.Sight)
    fov = sight.in_sight

    # find player-controlled characters on the same map as us, the monster
    def _valid(e):
        return has_component(ent_mgr, e[0], comp.World) and \
            has_component(ent_mgr, e[0], comp.PlayerControlled) and \
            ent_mgr.component_for_entity(e[0], comp.World).world == this_world

    ents = [target_ent
            for (target_ent, _) in filter(
                _valid, ent_mgr.pairs_for_type(comp.Position))
            if ent_mgr.component_for_entity(target_ent,
                                            comp.Position).coords
            in fov]
    num_player_chars = len(ents)
    if num_player_chars < 1:
        return None
    elif num_player_chars == 1:
        return ents[0]
    elif num_player_chars > 1:
        chosen = random.randrange(0, num_player_chars)
        return ents[chosen]


def monster(ent_mgr, ent):
    '''Generic AI function for monsters.'''
    this_world = ent_mgr.component_for_entity(ent, comp.World).world
    this_pos = ent_mgr.component_for_entity(ent, comp.Position).coords
    actions = ent_mgr.component_for_entity(ent, comp.Actor).queue
    actions.clear()
    ai_comp = ent_mgr.component_for_entity(ent, comp.AI)
    target = ai_comp.target
    if not target:
        ai_comp.target = _monster_choose_target(ent_mgr, ent)
        target = ai_comp.target
    if not target:
        return

    def move_cost(new_x, new_y):
        return 1 if eldmap.passable(ent_mgr, this_world, (new_x, new_y)) else 0
    target_pos = ent_mgr.component_for_entity(target, comp.Position).coords
    target_x, target_y = target_pos
    pathfinder = tdl.map.AStar(eldmap.map_width(this_world),
                               eldmap.map_height(this_world),
                               move_cost, digital_cost=1)
    path = pathfinder.get_path(this_pos[0], this_pos[1], target_x, target_y)
    if path:
        next_tile = to_local_coords(this_pos, path[0])
        actions.append(('do_action_tile', next_tile))
