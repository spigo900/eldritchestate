import pytest
import eldestrl.qtree as qtree
from eldestrl.qtree import qmapi


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
