#!/bin/env python3
# import eldestrl.utils as utils
from eldestrl.utils import *  # noqa


def test_clamp():
    assert clamp(-50, 3, 10) == 3
    assert clamp(5, 3, 10) == 5
    assert clamp(50, 3, 10) == 10


def test_in_range():
    assert in_range(5, 3, 10)
    assert not in_range(-50, 3, 10)
    assert not in_range(50, 3, 10)


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
