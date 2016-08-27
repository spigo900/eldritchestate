import random
from collections import UserDict
from ecs.exceptions import NonexistentComponentTypeForEntity
import eldestrl.components as components
import eldestrl.tiles as tiles
from eldestrl.utils import first_helper


class NoneInMapError(Exception):
    pass


class Map(UserDict):
    def __init__(self, map_tiles, tiletypes=tiles.load_json()):
        self.data = map_tiles
        self.ents = {}
        self.light_map = {}
        self.seen = set()
        self.tiletypes = tiletypes


# map functions
def map_width(map_):
    '''Return the map's width.'''
    return max(map_.keys())[0]


def map_height(map_):
    '''Return the map's height.'''
    return max(map_.keys())[1]


def _entlist_passable(ent_mgr, ents):
    '''Return true if any of ents is passable, else return false.'''
    for ent in ents:
        try:
            ent_mgr.component_for_entity(ent, components.BlocksMove)
            return False
        except NonexistentComponentTypeForEntity:
            return True
    return True


def passable(ent_mgr, map_, coords):
    '''Returns true if the given coordinate is passable.'''
    if coords not in map_ and coords not in map_.ents:
        return False
    tiletype = get_tile_type(map_, map_[coords])
    blocks = tiletype['blocks']
    ents = map_.ents.get(coords, [])
    return (not blocks) and _entlist_passable(ent_mgr, ents)


def blocks_sight(map_, x, y):
    # Slightly hacky; I should define a default tiletype eventually.
    # Or something like that.
    ttype = map_.get((x, y), None)
    if ttype:
        type_def = get_tile_type(map_, ttype)
        return type_def['blocks_sight']
    else:
        return True


def light_attenuation(map_, x, y):
    '''Returns the light attenuation value for the given cell.'''
    ttype = get_tile_type(map_, map_[x, y])
    return ttype.get("light_attenuation", 0.0)


def map_coords(map_):
    '''Takes a map and returns an iterator over all coordinates in the map.'''
    return sorted(map_.keys())


def all_matching(map_, pred):
    '''Takes a map and a predicate and returns a generator for all tiles in the
    map which satisfy the predicate.

    pred should take the map and the coordinates and return a boolean value.
    '''
    return ((x, y) for (x, y) in map_coords(map_) if pred(map_, x, y))


def first_matching(map_, pred):
    '''Takes a map and a predicate and returns the first tile in the map
    (starting from the upper right and cycling x first, y second) which matches
    the given predicate.

    pred should take the map and the coordinates and return a boolean value.
    '''
    return first_helper(all_matching(map_, pred),
                        NoneInMapError("No tiles in map match predicate!"))


def all_matching_ents(ent_mgr, map_, pred):
    '''Takes a map and a predicate and returns a generator for all tiles in the
    map whose entity lists satisfy the predicate.

    pred should take the entity manager, the map and the coordinates and return
    a boolean value.

    '''
    return (coords for coords in map_.ents.keys()
            if pred(ent_mgr, map_, coords))


def first_matching_ents(ent_mgr, map_, pred):
    '''Takes a map and a predicate and returns the first tile in the map
    whose entity list satisfies the given predicate.

    pred should take the map and the coordinates and return a boolean value.

    '''
    return first_helper(all_matching_ents(ent_mgr, map_, pred),
                        NoneInMapError("No tiles in map match predicate!"))


def all_matching_map(ent_mgr, map_, pred):
    '''Takes a map and a predicate and returns a generator for the coordinates
    of all tiles in the map which satisfy the predicate.

    pred should take the entity manager, the map and the coordinates and return
    a boolean value.

    '''
    return (coords for coords in map_coords(map_)
            if pred(ent_mgr, map_, coords))


def first_matching_map(ent_mgr, map_, pred):
    '''Takes a map and a predicate and returns the first tile in the map
     whose entity
    list satisfies the given predicate.

    pred should take the map and the coordinates and return a boolean value.

    '''
    return first_helper(all_matching_map(ent_mgr, map_, pred),
                        NoneInMapError("No tiles in map match predicate!"))


def first_unoccupied(ent_mgr, map_):
    '''Takes the map and returns a valid starting tile for the player.'''
    return first_matching_map(ent_mgr, map_, passable)


def random_unoccupied(ent_mgr, map_, seed):
    rng = random.Random(seed)
    return rng.choice(list(all_matching_map(ent_mgr, map_, passable)))


def get_tile_type(map_, typename):
    '''Takes a tile type name and returns the corresponding tile definition.'''
    return tiles.get_tile_def(map_.tiletypes, typename)


def maybe_get_type(map_, typename):
    '''Takes a tile type name and returns the corresponding tile definition,
    if both are non-falsy (and so non-None).'''
    if map_.tiletypes and typename:
        return get_tile_type(map_, typename)
    return {}
