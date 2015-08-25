import random
import copy
from eldestrl.utils import Rect

# DEFAULT_SEED = 4359
# DEFAULT_SEED = 22
DEFAULT_SEED = 88
MAX_DEPTH = 4


def new_leaf(val):
    return [val]


def qmap(tree, f):
    """Return the result of applying f to all nodes in the tree."""
    first = [f(tree[0])] if tree[0] is not None else []
    return first + map(qmap, tree[1:])


def qmapi(tree, f):
    """Iterative version of qmap."""
    # should return a tree of values, but currently returns a list; how do I
    # write that algorithm?
    vals = []
    # stack = tree[1:]
    # stack = tree[::-1]
    stack = tree
    # if tree[0] is not None:
    #     vals.append(f(tree[0]))
    while stack:
        cur = stack.pop()
        if cur[0] is not None:
            vals.append(f(cur[0]))
        # loop will not execute at all for leaf nodes, since they're just [val]
        # and nodes with None for all branches are also leaf nodes, and so
        # they'll be looped through to no effect
        #
        # I should probably stick with just using singleton lists as leaves
        # since that's simpler and in this case more efficient
        for item in cur[1:]:
            if item is not None:
                stack.append(item)
    return vals


def qmapi3(tree, f):
    """Iterative version of qmap."""
    treec = copy.deepcopy(tree)
    stack = []
    node = treec
    while stack and node:
        cur = stack.pop()
        if cur[0] is not None:
            vals.append(f(cur[0]))
        # loop will not execute at all for leaf nodes, since they're just [val]
        # and nodes with None for all branches are also leaf nodes, and so
        # they'll be looped through to no effect
        #
        # I should probably stick with just using singleton lists as leaves
        # since that's simpler and in this case more efficient
        for item in cur[1:]:
            if item is not None:
                stack.append(item)
    return vals

SENTINEL = None


def qreduce(tree, f, acc=SENTINEL):
    # see above
    if acc is SENTINEL:
        acc = [None]
    stack = tree[1:]
    if tree[0] is not None:
        acc = f(acc, tree[0])
    while stack:
        cur = stack.pop()
        if cur[0] is not None:
            acc = f(acc, cur[0])
        for item in cur[1:]:
            if item is not None:
                stack.append(item)
    return acc


def qmapi2(tree, f):
    return qreduce(tree, f, lambda acc, x: acc + f(x), [])


def is_branch(node):
    try:
        node[1]
        return any(True for v in node[1:] if v is not None)
    except IndexError:
        return False


def is_leaf(node):
    return node[0] is not None and \
        not is_branch(node)


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
    if is_leaf(tree):
        return subdivide_rect(tree[0], x, y)
    else:
        return qmapi(tree, lambda r: subdivide_rect(r, x, y))
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
    tmp = new_leaf(root_rect)
    for i in range(depth - 1):
        split_x, split_y = (get_random(rng, 0.25, 0.75),
                            get_random(rng, 0.25, 0.75))
        tmp = subdivide_tree(tmp, split_x, split_y)
    return tmp


def gen(width, height, seed=DEFAULT_SEED):
    rng = random.Random(seed)
    base_tree = gen_quadtree(rng, width, height, )


def edge(tree, edge):
    if is_leaf(tree):
        return tree
    if edge == 'n':
        return edge(tree.nw, edge)
