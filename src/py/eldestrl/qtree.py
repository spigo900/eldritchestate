from enum import IntEnum


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


class TreeDirs(IntEnum):
    QI = 1
    QII = 2
    QIII = 3
    QIV = 4


def qmapi(f, tree):
    if not tree:
        return tree
    root_val = tree_value(tree)
    new_tree = new_leaf(f(root_val))
    stack = [(child, new_tree, dir_) for (child, dir_)
             in zip(tree_children(tree), TreeDirs)]
    while stack:
        (cur, parent, dir_) = stack.pop()
        val = f(tree_value(cur))
        if parent and dir_:
            parent[dir_] = new_leaf(val)
        children = list(tree_children(cur))
        for (i, cur_child) in enumerate(children):
            direction = TreeDirs(i + 1)
            if cur_child:
                stack.append((cur_child, parent[dir_], direction))
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


def is_branch(node):
    try:
        node[1]
        return any(v != [] for v in node[1:])
    except IndexError:
        return False


def is_leaf(node):
    return node[0] is not None and \
        not is_branch(node)
