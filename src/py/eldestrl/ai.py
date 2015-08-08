import random
import untdl.map
import eldestrl.components as comp
import eldestrl.map as eldmap
from eldestrl.utils import has_component, to_local_coords


def _manhattan_cost(pos, new_pos):
    coord_diff = tuple(a - b for b in pos for a in new_pos)
    return sum(abs(x) for x in coord_diff)


def _flat_cost(ent_mgr, pos, new_pos):
    x_diff, y_diff = tuple(a - b for b in pos for a in new_pos)
    cost = sum(abs(x) for x in (x_diff, y_diff))
    if x_diff != 0 or y_diff != 0:
        return cost - min(x_diff, y_diff)
    else:
        return cost


def _has_world(ent_mgr, e):
    return has_component(ent_mgr, e, comp.World)


def client_choose_target(ent_mgr, ent):
    # ents = [pair_pos[0] for (pair_pos, pair_world, pair_player)
    #         in zip(ent_mgr.components_for_type(comp.Position),
    #                ent_mgr.components_for_type(comp.World),
    #                ent_mgr.components_for_type(comp.PlayerControlled))
    #         if (pair_pos[0] == pair_world[0] == pair_player[0])
    #         and pair_world[1].world == this_world]
    this_world = ent_mgr.component_for_entity(ent, comp.World).world

    # find player-controlled characters on the same map as us, the client(s)
    def _valid(e):
        return has_component(ent_mgr, e[0], comp.World) and \
            has_component(ent_mgr, e[0], comp.PlayerControlled) and \
            ent_mgr.component_for_entity(e[0], comp.World).world == this_world

    ents = [target_ent
            for target_ent in filter(
                _valid, ent_mgr.components_for_type(comp.Position))]
    num_player_chars = len(ents)
    if num_player_chars < 1:
        return None
    elif num_player_chars == 1:
        return ents[0]
    elif num_player_chars > 1:
        chosen = random.randrange(0, num_player_chars)
        return ents[chosen]


def client_ai(ent_mgr, ent):
    '''AI function for client NPCs.'''
    def client_cost(new_pos):
        return 1 if eldmap.passable(ent_mgr, ent, new_pos) else 0
    this_world = ent_mgr.component_for_entity(ent, comp.World).world
    this_pos = ent_mgr.component_for_entity(ent, comp.Position).coords
    actions = ent_mgr.component_for_entity(ent, comp.Actor).queue
    ai_comp = ent_mgr.component_for_entity(ent, comp.AI)
    target = ai_comp.target
    if not target:
        ai_comp.target = client_choose_target(ent_mgr, ent)
    print('DEBUG: ai_comp.target is %s.' % str(ai_comp.target))
    target_pos = ent_mgr.component_for_entity(target, comp.Position)
    target_x, target_y = target_pos.coords
    distance = _flat_cost(to_local_coords(this_pos, target_pos))
    if distance <= 5:
        actions.append(('do_action_tile', (random.randint(-1, 1),
                                           random.randint(-1, 1))))
        return
    pathfinder = untdl.map.AStar(eldmap.map_width(this_world),
                                 eldmap.map_height(this_world),
                                 client_cost, digital_cost=1)
    path = pathfinder.get_path(this_pos[0], this_pos[1], target_x, target_y)
    if path:
        next_tile = to_local_coords(next(path), this_pos)
        actions.append(('do_action_tile', next_tile))


AI_TYPES = {'client': client_ai}
