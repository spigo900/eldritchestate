#!/bin/env python3


TILES = {'floor': {'char': '.',
                   'passable': True},
         'wall': {'char': '+',
                  'passable': False}}

MAP = {(x, y): ('wall' if x == 1 or x == 25 or
                y == 1 or y == 15 else 'floor')
       for x in range(1, 26) for y in range(1, 16)}


# map functions
def min_map(map_):
    '''Return the lowest coordinates in the map (upper-left corner).'''
    return min(map_.keys())


def max_map(map_):
    '''Return the highest coordinates in the map (lower-right corner).'''
    return max(map_.keys())


def in_map(map_, x, y):
    '''Return true if the coordinates are present in the map.'''
    return True if (x, y) in map_ else False


def passable(map_, x, y):
    '''Return true if the given coordinate is present in the map and contains
    a passable tile.'''
    if not in_map(map_, x, y):
        return False
    tile = map_[x, y]
    return get_tile_type(tile)['passable']


def clamp_coord(map_, x, y):
    '''Take a pair of coordinates and return a new pair which is guranteed to be
    within the map\'s boundaries.'''
    newx = clamp(x, min_map(map_)[0], max_map(map_)[0])
    newy = clamp(y, min_map(map_)[1], max_map(map_)[1])
    return (newx, newy)


def first_matching(map_, pred):
    '''Take a map and a predicate. Return the first tile in the map (starting
    from the upper right and cycling x first, y second) which matches the given
    predicate.

    pred should take the map and the coordinates and return a boolean value.'''
    for (x, y), _ in sorted(map_.items()):
        if pred(map_, x, y):
            return (x, y)
    raise NoneInMapError("No tiles in map match predicate!")


def all_matching(map_, pred):
    '''Take a map and a predicate. Return a generator for all tiles in the map
    which satisfy the predicate.

    pred should take the map and the coordinates and return a boolean value.'''
    for (x, y), _ in sorted(map.items()):
        if pred(map_, x, y):
            yield (x, y)
    raise StopIteration()


def get_player_start_pos(map_):
    '''Take the map and return a valid starting tile for the player.'''
    return first_matching(map_, passable)


def get_tile_type(name):
    '''Take a type type name and return the corresponding tile definition.'''
    return TILES[name]


def new_map():
    '''Return a new map.'''
    from copy import deepcopy
    return deepcopy(MAP)
