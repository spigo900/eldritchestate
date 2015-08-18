import random
from collections import UserDict, namedtuple
from ecs.exceptions import NonexistentComponentTypeForEntity
import eldestrl.components as components
from eldestrl.utils import first_helper


TILES = {'floor': {'char': '.',
                   'passable': True,
                   'blocks_sight': False},
         'wall': {'char': '+',
                  'passable': False,
                  'blocks_sight': True}}

MAP = {(x, y): ('wall' if x == 1 or x == 25 or
                y == 1 or y == 15 else 'floor')
       for x in range(1, 26) for y in range(1, 16)}

_MapInfo = namedtuple('MapInfo', 'width, height,'
                      'min_rooms, max_rooms,'
                      'room_width_min, room_width_max,'
                      'room_height_min, room_height_max')
Point = namedtuple('Point', 'x y')
Rect = namedtuple('Rect', 'x, y, width, height')


class NoneInMapError(Exception):
    pass


class Map(UserDict):
    def __init__(self, map_tiles=MAP):
        self.data = map_tiles
        self.ents = {}


# map functions
def map_width(map_):
    '''Return the map's width.'''
    return max(map_.keys())[0]


def map_height(map_):
    '''Return the map's height.'''
    return max(map_.keys())[1]


def _entlist_passable(ent_mgr, ents):
    for ent in ents:
        try:
            ent_mgr.component_for_entity(ent, components.BlocksMove)
            return False
        except NonexistentComponentTypeForEntity:
            return True
    return True


def passable(ent_mgr, map_, coords):
    '''Returns true if the given coordinate is passable.
    '''
    if coords not in map_ and coords not in map_.ents:
        return False
    tiletype = get_tile_type(map_[coords])
    passable = tiletype['passable']
    ents = map_.ents.get(coords, [])
    return passable and _entlist_passable(ent_mgr, ents)


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


def map_info(width, height,
             min_rooms=1, max_rooms=3,
             room_width_min=3, room_width_max=10,
             room_height_min=5, room_height_max=8):
    return _MapInfo(width, height,
                    min_rooms, max_rooms,
                    room_width_min, room_width_max,
                    room_height_min, room_height_max)


# DEFAULT_MAP_SEED = 4359
DEFAULT_MAP_SEED = 88
DEFAULT_MAP_INFO = map_info(80, 80)


def make_room(map_, x, y, width, height):
    for x_cur in range(width):
        for y_cur in range(height):
            if x_cur == 0 or x_cur == (width - 1) \
               or y_cur == 0 or y_cur == (height - 1):
                map_[x + x_cur, y + y_cur] = 'wall'
            else:
                map_[x + x_cur, y + y_cur] = 'floor'


def rects_intersect(a, b):
    # Could probably be simplified by application of the de Morgan law.
    # not (a and b) = (not a) or (not b)?
    #
    # wait, that doesn't make sense -- there's no negation going on here.
    #
    # Could I simplify it via negation, though?
    return ((a.x + a.width) < b.x or
            (b.x + b.width) < a.x) and \
           ((a.y + a.height) < b.y or
            (b.y + b.height) < a.y)


def get_horizontal_center(map_height):
    return map_height // 2


def distance_from_horiz_center(map_height, y):
    return abs(y - get_horizontal_center(map_height))


def furthest_from_center(map_height, a, b):
    """
    Return the point
    """
    dist_a = distance_from_horiz_center(map_height, a[1])
    dist_b = distance_from_horiz_center(map_height, b[1])
    return a if dist_a >= dist_b else b


def random_in_rect(rng, rect):
    return (rng.randint(rect.x, rect.x + rect.width),
            rng.randint(rect.y, rect.y + rect.height))


def tunnel_h(map_, x1, x2, y):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        map_[x, y] = 'floor'


def tunnel_v(map_, y1, y2, x):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        map_[x, y] = 'floor'


def connect_rooms(map_, rng, map_info, rooms, progress_callback):
    connections = []
    unconnected = rooms
    map_height = map_info.height
    while unconnected:
        for room in unconnected:
            other_room = rng.choice(rooms)
            if (room, other_room) in connections \
               or room == other_room:
                continue
            point_a = random_in_rect(rng, room)
            point_b = random_in_rect(rng, other_room)
            start = furthest_from_center(map_height, point_a, point_b)
            end = point_b if start == point_a else point_a
            tunnel_h(map_, start[0], end[0], start[1])
            tunnel_v(map_, start[1], end[1], end[0])
            connections.append((room, other_room))
            unconnected.remove(room)
            unconnected.remove(other_room)
            progress_callback(map_)


def map_gen(seed, map_info, progress_callback):
    rng = random.Random(seed)
    # map_ = {(x, y): 'wall'
    #         for x in range(1, map_info.width + 1)
    #         for y in range(1, map_info.height + 1)}
    map_ = {}
    rooms = []
    num_rooms = 0
    to_gen = rng.randint(map_info.min_rooms, map_info.max_rooms)
    while num_rooms < to_gen:
        room_width = rng.randint(map_info.room_width_min + 2,
                                 map_info.room_width_max + 2)
        room_height = rng.randint(map_info.room_height_min + 2,
                                  map_info.room_height_max + 2)
        for _ in range(20):
            room_pos = Point(rng.randint(1, map_info.width),
                             rng.randint(1, map_info.height))
            room_rect = Rect(room_pos.x + 1, room_pos.y + 1,
                             room_width - 2, room_height - 2)
            cant_place = False
            for rect in rooms:
                if rects_intersect(room_rect, rect):
                    cant_place = True
            if cant_place:
                continue
            make_room(map_, room_pos.x, room_pos.y,
                      room_width, room_height)
            rooms.append(room_rect)
            num_rooms += 1
            break
        progress_callback(map_)
    connect_rooms(map_, rng, map_info, rooms, progress_callback)
    return map_


def new_map(seed=DEFAULT_MAP_SEED, map_info=DEFAULT_MAP_INFO):
    '''Return a new map.'''
    return Map(map_gen(seed, map_info, lambda *_: None))
