import random
import eldestrl.qtree as qtree
from eldestrl.utils import Rect

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
    return [None, ne, nw, sw, se]


def subdivide_tree(tree, x, y):
    if qtree.is_leaf(tree):
        return subdivide_rect(tree[0], x, y)
    else:
        return qtree.qmapi(tree, lambda r: subdivide_rect(r, x, y))
        # stack = [tree]
        # while stack:
        #     cur = stack.pop()
        #     subdivide


def get_random(rng, lower, upper):
    ret = rng.random()
    while lower <= ret <= upper:
        ret = rng.random()
    return ret


def gen_quadtree(rng, width, height, depth):
    root_rect = Rect(1, 1, width, height)
    tmp = qtree.new_leaf(root_rect)
    for i in range(depth - 1):
        split_x, split_y = (get_random(rng, 0.25, 0.75),
                            get_random(rng, 0.25, 0.75))
        tmp = subdivide_tree(tmp, split_x, split_y)
    return tmp


def gen(width, height, seed=DEFAULT_SEED):
    rng = random.Random(seed)
    base_tree = gen_quadtree(rng, width, height, )


def edge(tree, edge):
    if qtree.is_leaf(tree):
        return tree
    if edge == 'n':
        return edge(tree.nw, edge)
