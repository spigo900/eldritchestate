from eldestrl.utils import clamp


TILES = {'floor': {'char': '.',
                   'passable': True},
         'wall': {'char': '+',
                  'passable': False}}

MAP = {(x, y): ('wall' if x == 1 or x == 25 or
                y == 1 or y == 15 else 'floor')
       for x in range(1, 26) for y in range(1, 16)}


class NoneInMapError(Exception):
    # def __init__(self, message):
    #     super(NoneInMapError, self).__init__(message)
    #     self.message = message
    pass


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


def passable(map_, x, y):
    '''Returns true if the given coordinate is present in the map and contains
    a passable tile.
    '''
    if not in_map(map_, x, y):
        return False
    tile = map_[x, y]
    return get_tile_type(tile)['passable']


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


def first_matching(map_, pred):
    '''Takes a map and a predicate and returns the first tile in the map
    (starting from the upper right and cycling x first, y second) which matches
    the given predicate.

    pred should take the map and the coordinates and return a boolean value.
    '''
    for (x, y), _ in sorted(map_.items()):
        if pred(map_, x, y):
            return (x, y)
    raise NoneInMapError("No tiles in map match predicate!")


def all_matching(map_, pred):
    '''Takes a map and a predicate and returns a generator for all tiles in the
    map which satisfy the predicate.

    pred should take the map and the coordinates and return a boolean value.
    '''
    for (x, y), _ in sorted(map.items()):
        if pred(map_, x, y):
            yield (x, y)
    raise StopIteration()


def get_player_start_pos(map_):
    '''Takes the map and returns a valid starting tile for the player.'''
    return first_matching(map_, passable)


def get_tile_type(name):
    '''Takes a type type name and returns the corresponding tile definition.'''
    return TILES[name]


def new_map():
    '''Return a new map.'''
    from copy import deepcopy
    return deepcopy(MAP)
