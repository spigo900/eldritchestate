#!/bin/env python3


# utilities
def clamp(val, min_, max_):
    '''Ensure a value is within a given range. Return the upper or lower bound
    if val is out of bounds, depending on whether it\'s greater than max_ or
    less than min._'''
    return min(max(val, min_), max_)


def in_range(val, min_, max_):
    '''Takes a value, a minimum and a maximum and returns whether the value is
    within the range.'''
    return True if min_ <= val <= max_ else False


def to_local_coords(coords_a, coords_b):
    '''Takes two coordinate pairs and returns a new coordinate pair which
    represents the difference between coords_a and coords_b (used to get coords
    relative to view, for example).
    '''
    return (coords_b[0] - coords_a[0], coords_b[1] - coords_a[1])


def subtract_iterables(iter_a, iter_b):
    '''Takes two iterables a and b and return a new iterable whose value is a -
    b for each member of a and each member of b.'''
    from operator import sub
    return map(sub, iter_a, iter_b)


def draw_str_centered(con, str_, y, *args, **kwargs):
    str_length = len(str_)
    con_width = con.width
    con.draw_str(con_width // 2 - str_length // 2, y, str_, *args, **kwargs)
