from collections import UserDict
from ecs.exceptions import NonexistentComponentTypeForEntity
import eldestrl.components as components
from eldestrl.utils import clamp


TILES = {'floor': {'char': '.',
                   'passable': True},
         'wall': {'char': '+',
                  'passable': False}}

MAP = {(x, y): ('wall' if x == 1 or x == 25 or
                y == 1 or y == 15 else 'floor')
       for x in range(1, 26) for y in range(1, 16)}


class NoneInMapError(Exception):
    pass


class Map(UserDict):
    def __init__(self, map_tiles=MAP):
        self.data = map_tiles
        self.ents = {}


# map functions
def min_map(map_):
    '''Returns the lowest coordinates in the map (upper-left corner).'''
    return min(map_.keys())


def max_map(map_):
    '''Returns the highest coordinates in the map (lower-right corner).'''
    return max(map_.keys())


def in_map(map_, x, y):
    '''Returns true if the coordinates are present in the map.'''
    return (x, y) in map_


def _entlist_passable(ent_mgr, ents):
    for ent in ents:
        try:
            ent_mgr.component_for_entity(ent, components.BlocksMove)
            return False
        except NonexistentComponentTypeForEntity:
            return True


def passable(ent_mgr, map_, coords):
    '''Returns true if the given coordinate is passable.
    '''
    if coords not in map_ and coords not in map_.ents:
        return False
    tiletype = get_tile_type(map_[coords])
    passable = tiletype['passable']
    ents = map_.ents[coords]
    return passable and _entlist_passable(ent_mgr, ents)


def clamp_coord(map_, x, y):
    '''Takes a pair of coordinates and returns a new pair which is guranteed to
    be within the map\'s boundaries.
    '''
    newx = clamp(x, min_map(map_)[0], max_map(map_)[0])
    newy = clamp(y, min_map(map_)[1], max_map(map_)[1])
    return (newx, newy)


def map_coords(map_):
    '''Takes a map and returns an iterator over all coordinates in the map.'''
    return sorted(map_.keys())


def map_tiles(map_):
    '''Takes a map and returns an iterator over the map's tiles.'''
    return sorted(map_.items())


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
    try:
        return next(all_matching(map_, pred))
    except StopIteration:
        raise NoneInMapError("No tiles in map match predicate!")


def all_matching_ents(ent_mgr, map_, pred):
    '''Takes a map and a predicate and returns a generator for all tiles in the
    map whose entity lists satisfy the predicate.

    pred should take the map and the coordinates and return a boolean value.
    '''
    return (coords for coords in map_.ents.keys()
            if pred(ent_mgr, map_, coords))


def first_matching_ents(ent_mgr, map_, pred):
    '''Takes a map and a predicate and returns the first tile in the map
    (starting from the upper right and cycling x first, y second) whose entity
    list satisfies the given predicate.

    pred should take the map and the coordinates and return a boolean value.

    '''
    try:
        return next(all_matching_ents(ent_mgr, map_, pred))
    except StopIteration:
        raise NoneInMapError("No tiles in map match predicate!")


def first_unoccupied(ent_mgr, map_):
    '''Takes the map and returns a valid starting tile for the player.'''
    return first_matching_ents(ent_mgr, map_, passable)


def new_tile_type(name, char, color, bgcolor=(0, 0, 0),
                  passable=True, blocks_sight=False):
    '''Define a new tile type.

    Name is the ID by which the tiletype should be accessed, and which should
    be passed when creating a new tile via the entity template for tiles. If
    the given tile type already exists, this function throws an error rather
    than mutate it.

    _Note that this mutates the map dictionary._ Use with care.

    '''
    assert name not in TILES
    TILES['name'] = {'char': char,
                     'fg': color,
                     'bg': bgcolor,
                     'passable': passable,
                     'blocks_sight': blocks_sight}


def get_tile_type(name):
    '''Takes a tile type name and returns the corresponding tile definition.'''
    return TILES[name]


def new_map():
    '''Return a new map.'''
    from copy import deepcopy
    return Map(deepcopy(MAP))
