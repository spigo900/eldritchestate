import pytest
import operator as op
import functools as fn
import eldestrl.qtree as qtree
from eldestrl.qtree import qmapi, reduce


@pytest.fixture
def tree_fixt():
    my_tree = qtree.new_leaf(5)
    my_tree[1:5] = (qtree.new_leaf(4), qtree.new_leaf(3),
                    qtree.new_leaf(2), qtree.new_leaf(1))
    my_tree[4][3] = qtree.new_leaf(48)
    return my_tree


def test_qmapi(tree_fixt):
    identity = qmapi(lambda x: x, tree_fixt)
    pos = qmapi(lambda x: x + 5, tree_fixt)
    neg = qmapi(lambda x: x - 5, tree_fixt)
    assert identity == tree_fixt
    assert pos[0] == tree_fixt[0] + 5
    assert neg[0] == tree_fixt[0] - 5


def test_flatten_equiv(tree_fixt):
    def add5(x):
        return x + 5
    assert set(qtree.flatten(qtree.qmapi(add5, tree_fixt))) == \
        set(map(add5, qtree.flatten(tree_fixt)))
    assert fn.reduce(op.add, qtree.flatten(tree_fixt)) == \
        reduce(op.add, 0, tree_fixt)
    assert qtree.flatten(tree_fixt)[0] == tree_fixt[0]
