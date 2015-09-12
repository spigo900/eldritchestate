from enum import Enum


def new_leaf(val):
    return [val, [], [], [], []]


def tree_value(tree):
    return tree[0]


def tree_children(tree):
    return (child for child in tree[1:] if child)


def reduce(f, acc, tree):
    if not tree:
        return acc
    stack = [tree]
    while stack:
        cur = stack.pop()
        acc = f(acc, tree_value(cur))
        children = list(tree_children(cur))
        stack.extend(children)
    return acc


def qmap(tree, f):
    """Return the result of applying f to all nodes in the tree."""
    first = [f(tree[0])] if tree[0] is not None else []
    return first + map(qmap, tree[1:])


class TreeDirs(Enum):
    QI = 1
    QII = 2
    QIII = 3
    QIV = 4


def qmapi(f, tree):
    if not tree:
        return tree
    root_val = tree_value(tree)
    # new_tree = new_leaf(f(root_val))
    new_tree = new_leaf(root_val)
    stack = [(new_tree, None, None)]
    while stack:
        (cur, parent, dir_) = stack.pop()
        val = f(tree_value(cur))
        if parent and dir_:
            parent[dir_] = new_leaf(val)
        children = list(tree_children(cur))
        for direction in TreeDirs:
            cur_child = children[direction]
            if cur_child:
                stack.append((cur, cur_child, direction))
    return new_tree

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
        return any(v != [] for v in node[1:])
    except IndexError:
        return False


def is_leaf(node):
    return node[0] is not None and \
        not is_branch(node)
