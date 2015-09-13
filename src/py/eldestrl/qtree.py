from enum import IntEnum


def new_leaf(val):
    return [val, [], [], [], []]


def tree_value(tree):
    return tree[0]


def tree_children(tree):
    return (child for child in tree[1:] if child) \
        if isinstance(tree, list) and len(tree) == 5 else []


def tree_all_children(tree):
    return (child for child in tree[1:])


def qall(tree):
    """Returns true if all values in the tree are truthy."""
    return reduce(lambda acc, x: acc and x, True, tree)


def qall_match(tree, pred):
    """Returns true if all values in the tree match the given predicate."""
    return qall(qmapi(pred, tree))


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
        children = list(tree_all_children(cur))
        for (i, cur_child) in enumerate(children):
            direction = TreeDirs(i + 1)
            if cur_child:
                stack.append((cur_child, parent[dir_], direction))
    return new_tree


def flatten(tree):
    return reduce(lambda acc, x: acc + [x], [], tree)


def is_branch(node):
    try:
        node[1]
        return any(v != [] for v in node[1:])
    except IndexError:
        return False


def is_leaf(node):
    return node[0] is not None and \
        not is_branch(node)
