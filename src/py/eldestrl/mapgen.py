from collections import namedtuple
import random
from eldestrl.map import Map
import eldestrl.qtree as qtree
from eldestrl.utils import Rect, in_rect, rects_intersect, \
    rect_area, count_in_rect

################
# OLD MAP CODE #
################

_MapInfo = namedtuple('MapInfo', 'width, height,'
                      'min_rooms, max_rooms,'
                      'room_width_min, room_width_max,'
                      'room_height_min, room_height_max,'
                      'default_floor, default_wall,'
                      'default_door')


def map_info(width, height,
             min_rooms=1, max_rooms=3,
             room_width_min=3, room_width_max=10,
             room_height_min=5, room_height_max=8,
             default_floor='floor', default_wall='wall',
             default_door='wooden_door'):
    return _MapInfo(width, height,
                    min_rooms, max_rooms,
                    room_width_min, room_width_max,
                    room_height_min, room_height_max,
                    default_floor, default_wall,
                    default_door)


# DEFAULT_MAP_SEED = 4359
DEFAULT_MAP_SEED = 88
DEFAULT_MAP_INFO = map_info(80, 80,
                            min_rooms=10, max_rooms=50,
                            room_width_min=2, room_height_min=2)


def make_room(map_, floortype, walltype, x, y, width, height):
    for x_cur in range(width):
        for y_cur in range(height):
            if x_cur == 0 or x_cur == (width - 1) \
               or y_cur == 0 or y_cur == (height - 1):
                map_[x + x_cur, y + y_cur] = walltype
            else:
                map_[x + x_cur, y + y_cur] = floortype


def get_horizontal_center(map_height):
    return map_height // 2


def distance_from_horiz_center(map_height, y):
    return abs(y - get_horizontal_center(map_height))


def furthest_from_center(map_height, a, b):
    """Return the point that's further from the center of the map."""
    dist_a = distance_from_horiz_center(map_height, a[1])
    dist_b = distance_from_horiz_center(map_height, b[1])
    return a if dist_a >= dist_b else b


def random_in_rect(rng, rect):
    return (rng.randint(rect.x, rect.x + rect.width - 1),
            rng.randint(rect.y, rect.y + rect.height - 1))


def in_wall(rect, x, y):
    return rect.x - 1 <= x <= rect.x + rect.width \
        and rect.y - 1 <= y <= rect.y + rect.height \
        and not in_rect(rect, x, y)


def random_connectpoints(rng, map_height, rooms, room_a, room_b):
    for _ in range(10):
        point_a = random_in_rect(rng, room_a)
        point_b = random_in_rect(rng, room_b)
        start = furthest_from_center(map_height, point_a, point_b)
        end = point_b if point_a == start else point_a
        corner = end[0], start[1]
        intersects_anything = \
            any(in_wall(room_a, x, y) or in_wall(room_b, x, y)  # or
                # in_rect(room, x, y)
                for x in range(start[0], corner[0] + 1)
                for y in range(corner[1], end[1] + 1)
                for room in rooms
                if room != room_a and room != room_b
                if x == corner[0] or y == corner[1])
        if not intersects_anything:
            return (point_a, point_b)


def _do_in_inclusive_range(n1, n2, fn):
    for n in range(min(n1, n2), max(n1, n2) + 1):
        fn(n)


def tunnel_h(map_, floortype, x1, x2, y):
    def change_tile(x):
        map_[x, y] = floortype
    _do_in_inclusive_range(x1, x2, change_tile)


def tunnel_v(map_, floortype, y1, y2, x):
    def change_tile(y):
        map_[x, y] = floortype
    _do_in_inclusive_range(y1, y2, change_tile)


def unordered_range(n1, n2, s=1):
    """Take two numbers and an optional step and return a range from the lower to
    the higher (inclusive).

    """
    return range(min(n1, n2), max(n1, n2) + 1, s)


def connect_rooms(map_, rng, map_info, rooms, progress_callback):
    start_points = [rng.choice(rooms)]
    unconnected = set(rooms)
    unconnected.remove(start_points[0])
    map_height = map_info.height
    while unconnected:
        start_room = rng.choice(tuple(start_points))
        end_room = rng.choice(tuple(unconnected))
        result = random_connectpoints(rng, map_height, rooms,
                                      start_room, end_room)
        if not result:
            continue
        start, end = result
        tunnel_h(map_, map_info.default_floor, start[0], end[0], start[1])
        tunnel_v(map_, map_info.default_floor, start[1], end[1], end[0])
        for pos in ((x, y)
                    for x in unordered_range(start[0], end[0])
                    for y in unordered_range(start[1], end[1])
                    if (x == end[0] or y == start[1]) and
                    (in_wall(start_room, x, y) or
                     in_wall(end_room, x, y))):
            map_[pos] = map_info.default_door
        start_points.append(end_room)
        unconnected.remove(end_room)
        progress_callback(map_)


def map_gen(seed, map_info, progress_callback):
    rng = random.Random(seed)
    map_ = {}
    rooms = []
    num_rooms = 0
    to_gen = 11
    while num_rooms < to_gen:
        room_width = rng.randint(map_info.room_width_min + 2,
                                 map_info.room_width_max + 2)
        room_height = rng.randint(map_info.room_height_min + 2,
                                  map_info.room_height_max + 2)
        for _ in range(20):
            room_x = rng.randint(1, map_info.width - room_width)
            room_y = rng.randint(1, map_info.height - room_height)
            room_rect = Rect(room_x + 1, room_y + 1,
                             room_width - 2, room_height - 2)
            cant_place = False
            for rect in rooms:
                if rects_intersect(room_rect, rect):
                    cant_place = True
            if cant_place:
                continue
            make_room(map_, map_info.default_floor, map_info.default_wall,
                      room_x, room_y,
                      room_width, room_height)
            rooms.append(room_rect)
            num_rooms += 1
            break
        print("number of rooms: {}".format(num_rooms))
        progress_callback(map_)
    print("done base mapgen; connecting rooms")
    connect_rooms(map_, rng, map_info, rooms, progress_callback)
    return map_


def new_map(seed=DEFAULT_MAP_SEED, map_info=DEFAULT_MAP_INFO):
    '''Return a new map.'''
    return Map(map_gen(seed, map_info, lambda *_: None))


################
# NEW MAP CODE #
################

# DEFAULT_SEED = 4359
# DEFAULT_SEED = 22
DEFAULT_SEED = 88
MAX_DEPTH = 4


def subdivide_rect(rect, x, y):
    """Split a rect into a quad tree along the lines intersecting rect.width * x,
    rect.height * y.

    x and y should be floats between 0.0 and 1.0.
    """
    split_x = rect.x + rect.width * x
    split_y = rect.y + rect.height * y
    nw = Rect(rect.x, rect.y, rect.width * x, rect.height * y)
    ne = Rect(split_x, rect.y, round(rect.width * (1 - x)), rect.heght * y)
    sw = Rect(rect.x, split_y, rect.width * x, round(rect.height * (1 - y)))
    se = Rect(split_x, split_y,
              round(rect.width * (1 - x)),
              round(rect.height * (1 - y)))
    return [rect, ne, nw, sw, se]


def subdivide_rect_int(rect, split_x, split_y):
    """Split a rect into a quad tree along the lines intersecting x, y.
    """
    rects = [Rect(rect.x + split_x, rect.y,
                  rect.width - split_x, split_y),
             Rect(rect.x, rect.y, split_x, split_y),
             Rect(rect.x, rect.y + split_y,
                  split_x, rect.height - split_y),
             Rect(rect.x + split_x, rect.y + split_y,
                  rect.width - split_x, rect.height - split_y)]
    return [rect] + list(map(qtree.new_leaf, rects))


def fits_ratio(rect):
    LOWER_BOUND = 0.7
    UPPER_BOUND = 3.6
    return \
        LOWER_BOUND <= rect.width / rect.height <= UPPER_BOUND or \
        LOWER_BOUND <= rect.width / rect.height <= UPPER_BOUND


def subdivide_leaf_rand(rng, leaf):
    """Take a leaf containing a rectangle and pseudorandomly subdivide the rect
    into leaves."""
    rect = leaf[0]
    for _ in range(5):
        split_x = rng.randint(1, rect.width - 2)
        split_y = rng.randint(1, rect.height - 2)
        rects = subdivide_rect_int(rect, split_x, split_y)
        if qtree.qall_match(rects, fits_ratio):
            return rects
    return leaf


def subdivide_tree_rand(rng, tree):
    """Take a tree and subdivide its leaves randomly.

    This is a destructive operation (i.e. it mutates its argument).
    """
    stack = [tree]
    while stack:
        cur = stack.pop()
        children = list(qtree.tree_children(cur))
        stack.extend(children)
        if qtree.is_leaf(cur):
            cur[:] = subdivide_leaf_rand(rng, cur)

OUTSIDE_THRESH = 0.7


def outside(rect, cell_map):
    return rect_area(rect)/count_in_rect(rect, cell_map) >= OUTSIDE_THRESH


def tree_outside(tree, cell_map):
    # Implementation is somewhat suboptimal; ideally, I would want to apply
    # count_in_rect only to the leaves and then compute the branch's value as
    # the sum of its childrens' values. That way, each tile only has to be
    # checked once. For now, though, this will do.
    def outside_(r):
        return outside(r, cell_map)
    counted = qtree.qmapi(count_in_rect, tree)
    return qtree.qmapi(outside_, counted)


def gen_quadtree(rng, width, height, depth=MAX_DEPTH):
    tree = qtree.new_leaf(Rect(0, 0, width, height))
    for _ in range(depth):
        subdivide_tree_rand(rng, tree)
    return tree


def gen_map(width, height, seed=DEFAULT_SEED):
    rng = random.Random(seed)
    space_tree = gen_quadtree(rng, width, height, MAX_DEPTH)
    return space_tree


def _get_leaves_directional(tree, dirs):
    edge_leaves = []
    stack = [tree]
    while stack:
        cur = stack.pop()
        if qtree.is_leaf(cur):
            edge_leaves.append(qtree.tree_value(cur))
            continue
        children = list(qtree.tree_children(cur))
        for i in (x - 1 for x in dirs):
            stack.append(children[i])
    return edge_leaves

EDGES_TO_DIRS = {'n': (qtree.TreeDirs.QI, qtree.TreeDirs.QII),
                 'e': (qtree.TreeDirs.QI, qtree.TreeDirs.QIV),
                 's': (qtree.TreeDirs.QIII, qtree.TreeDirs.QIV),
                 'w': (qtree.TreeDirs.QII, qtree.TreeDirs.QIII)}


def edge(tree, edge):
    return _get_leaves_directional(tree, EDGES_TO_DIRS[edge])
