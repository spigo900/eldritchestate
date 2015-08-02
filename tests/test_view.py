#!/bin/env python3
import eldestrl.view as v
import pytest


@pytest.fixture
def view():
    return v.View(1, 1, 25, 25)


def test_view_edge(view):
    assert v.view_edge(view, 'left') == 0
    assert v.view_edge(view, 'right') == view.width
    assert v.view_edge(view, 'top') == 0
    assert v.view_edge(view, 'bottom') == view.height

    assert v.view_edge_abs(view, 'left') == view.x
    assert v.view_edge_abs(view, 'right') == view.x + view.width - 1
    assert v.view_edge_abs(view, 'top') == view.y
    assert v.view_edge_abs(view, 'bottom') == view.y + view.height - 1


def test_get_scroll(view):
    assert v.get_scroll_x(view, 0) == -v.View.SCROLL_EDGE_SIZE
    assert v.get_scroll_x(view, view.width - 1) == v.View.SCROLL_EDGE_SIZE
    assert v.get_scroll_y(view, 0) == -v.View.SCROLL_EDGE_SIZE
    assert v.get_scroll_y(view, view.height - 1) == v.View.SCROLL_EDGE_SIZE
    assert v.get_view_scroll(view, (0, 0)) == (v.get_scroll_x(view, 0),
                                               v.get_scroll_y(view, 0))
    assert v.get_view_scroll(view, (view.width, view.height)) == \
        (v.get_scroll_x(view, view.width), v.get_scroll_y(view, view.height))


def test_center_view(view):
    from eldestrl.utils import subtract_iterables
    coords = ((5, 5), (0, 5), (5, 0), (1, 1))
    for coord_pair in coords:
        current_view = v.center_view(view, coord_pair)
        assert current_view.coords == \
            tuple(subtract_iterables(coord_pair, (view.width // 2,
                                                  view.height // 2)))
        assert current_view.width == view.width
        assert current_view.height == view.height
