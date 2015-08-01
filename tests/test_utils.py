#!/bin/env python3
import utils
# import src.py.utils as utils
# import ..eld.utils as utils
# from ..eld import utils
# print('utils: ', utils)


def test_clamp():
    assert utils.clamp(-50, 3, 10) == 3
    assert utils.clamp(5, 3, 10) == 5
    assert utils.clamp(50, 3, 10) == 10


def test_in_range():
    assert utils.in_range(5, 3, 10)
    assert not utils.in_range(-50, 3, 10)
    assert not utils.in_range(50, 3, 10)


def test_to_local_coords():
    assert utils.to_local_coords((1, 1), (5, 5)) == (4, 4)
    assert utils.to_local_coords((2, 10), (5, 5)) == (3, -5)
    assert utils.to_local_coords((10, 2), (5, 5)) == (-5, 3)
    assert utils.to_local_coords((10, 10), (5, 5)) == (-5, -5)
    assert utils.to_local_coords((-10, -10), (5, 5)) == (15, 15)


def test_subtract_iterables():
    assert tuple(utils.subtract_iterables((1, 1), (5, 5))) == (-4, -4)
    assert tuple(utils.subtract_iterables((2, 10), (5, 5))) == (-3, 5)
    assert tuple(utils.subtract_iterables((10, 2), (5, 5))) == (5, -3)
    assert tuple(utils.subtract_iterables((10, 10), (5, 5))) == (5, 5)
    assert list(utils.subtract_iterables((-10, -10), (5, 5))) == [-15, -15]
    assert tuple(utils.subtract_iterables([1, 1], [5, 5])) == (-4, -4)
    assert list(utils.subtract_iterables([2, 10], [5, 5])) == [-3, 5]
    assert list(utils.subtract_iterables([10, 2], [5, 5])) == [5, -3]
    assert list(utils.subtract_iterables([10, 10], [5, 5])) == [5, 5]
    assert tuple(utils.subtract_iterables([-10, -10], [5, 5])) == (-15, -15)
    assert list(utils.subtract_iterables([-10, -10], (5, 5))) == [-15, -15]
