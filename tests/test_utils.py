#!/bin/env python3
from eldestrl.utils import *  # noqa


def test_clamp():
    assert clamp(-50, 3, 10) == 3
    assert clamp(5, 3, 10) == 5
    assert clamp(50, 3, 10) == 10


def test_in_range():
    assert in_range(5, 3, 10)
    assert not in_range(-50, 3, 10)
    assert not in_range(50, 3, 10)


def test_in_rect():
    rect = Rect(2, 3, 4, 5)
    assert in_rect(rect, 2, 3)
    assert in_rect(rect, 5, 3)
    assert in_rect(rect, 2, 7)
    assert in_rect(rect, 5, 7)
    assert not in_rect(rect, 1, 3)
    assert not in_rect(rect, 2, 2)
    assert not in_rect(rect, 6, 7)
    assert not in_rect(rect, 5, 8)


def test_rects_intersect():
    rect_a = Rect(1, 1, 5, 5)
    rect_b = Rect(2, 3, 4, 5)
    rect_c = Rect(4, 6, 7, 7)
    assert rects_intersect(rect_a, rect_b)
    assert rects_intersect(rect_b, rect_c)
    assert not rects_intersect(rect_a, rect_c)


def test_adjecent():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)

    # should be associative
    assert adjacent(a, b) == adjacent(b, a)

    # coords should be adjacent to themselves... probably
    assert adjacent(a, a)
    assert adjacent(c, c)
    assert adjacent(d, d)

    # testing usual cases
    assert adjacent(a, b)
    assert adjacent(a, c)
    assert adjacent(a, d)
    assert adjacent(b, d)
    assert adjacent(b, e)
    assert adjacent(d, f)

    # negative cases
    assert not adjacent(a, f)
    assert not adjacent(b, c)
    assert not adjacent(b, f)
    assert not adjacent(c, d)
    assert not adjacent(c, e)
    assert not adjacent(c, f)
    assert not adjacent(d, e)


def test_orthogonal():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)

    # should be associative
    assert orthogonal(a, b) == orthogonal(b, a)

    # coords should also be orthogonal to themselves... probably
    assert orthogonal(a, a)
    assert orthogonal(c, c)
    assert orthogonal(d, d)

    # testing usual cases
    assert orthogonal(a, b)
    assert not orthogonal(a, c)
    assert not orthogonal(a, d)
    assert orthogonal(b, d)
    assert orthogonal(b, e)
    assert not orthogonal(d, f)

    # more usual cases
    assert not orthogonal(a, f)
    assert not orthogonal(b, c)
    assert not orthogonal(b, f)
    assert not orthogonal(c, d)
    assert orthogonal(c, e)
    assert not orthogonal(c, f)
    assert orthogonal(d, e)


def test_ortho_adjacent():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)
    # should be associative
    assert ortho_adjacent(a, b) == ortho_adjacent(b, a)

    # should return the same as combining the plain functions does
    assert ortho_adjacent(a, a) == (orthogonal(a, a) and adjacent(a, a))
    assert ortho_adjacent(a, b) == (orthogonal(a, b) and adjacent(a, b))
    assert ortho_adjacent(a, c) == (orthogonal(a, c) and adjacent(a, c))
    assert ortho_adjacent(a, d) == (orthogonal(a, d) and adjacent(a, d))
    assert ortho_adjacent(a, e) == (orthogonal(a, e) and adjacent(a, e))
    assert ortho_adjacent(a, f) == (orthogonal(a, f) and adjacent(a, f))
    assert ortho_adjacent(b, c) == (orthogonal(b, c) and adjacent(b, c))
    assert ortho_adjacent(b, d) == (orthogonal(b, d) and adjacent(b, d))
    assert ortho_adjacent(b, e) == (orthogonal(b, e) and adjacent(b, e))
    assert ortho_adjacent(b, f) == (orthogonal(b, f) and adjacent(b, f))


def test_to_local_coords():
    assert to_local_coords((1, 1), (5, 5)) == (4, 4)
    assert to_local_coords((2, 10), (5, 5)) == (3, -5)
    assert to_local_coords((10, 2), (5, 5)) == (-5, 3)
    assert to_local_coords((10, 10), (5, 5)) == (-5, -5)
    assert to_local_coords((-10, -10), (5, 5)) == (15, 15)


def test_subtract_iterables():
    assert tuple(subtract_iterables((1, 1), (5, 5))) == (-4, -4)
    assert tuple(subtract_iterables((2, 10), (5, 5))) == (-3, 5)
    assert tuple(subtract_iterables((10, 2), (5, 5))) == (5, -3)
    assert tuple(subtract_iterables((10, 10), (5, 5))) == (5, 5)
    assert list(subtract_iterables((-10, -10), (5, 5))) == [-15, -15]
    assert tuple(subtract_iterables([1, 1], [5, 5])) == (-4, -4)
    assert list(subtract_iterables([2, 10], [5, 5])) == [-3, 5]
    assert list(subtract_iterables([10, 2], [5, 5])) == [5, -3]
    assert list(subtract_iterables([10, 10], [5, 5])) == [5, 5]
    assert tuple(subtract_iterables([-10, -10], [5, 5])) == (-15, -15)
    assert list(subtract_iterables([-10, -10], (5, 5))) == [-15, -15]
