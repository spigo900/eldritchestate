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
    return min_ <= val <= max_


def to_local_coords(coords_a, coords_b):
    '''Takes two coordinate pairs and returns a new coordinate pair which
    represents the difference between coords_a and coords_b (used to get coords
    relative to view, for example).
    '''
    return (coords_b[0] - coords_a[0], coords_b[1] - coords_a[1])


def adjacent(coords_a, coords_b):
    '''Takes a pair of coordinates and returns whether or not they're adjacent.
    Does not take into account whether the tiles are passable or even exist
    within the map -- or in any map, for that matter. Remember to check that
    they do exist and, optionally, are passable as necessary.
    '''

    ax, ay = coords_a
    bx, by = coords_b
    return -1 <= ax - bx <= 1 and -1 <= ay - by <= 1


def ortho_adjacent(coords_a, coords_b):
    '''Works like adjacent, but returns true only if the tiles are orthogonally
    adjacent.
    '''
    ax, ay = coords_a
    bx, by = coords_b
    return (-1 <= ax - bx <= 1 and ay == by) or \
        (-1 <= ay - by <= 1 and ax == bx)


def subtract_iterables(iter_a, iter_b):
    '''Takes two iterables a and b and return a new iterable whose value is a -
    b for each member of a and each member of b.'''
    from operator import sub
    return map(sub, iter_a, iter_b)


def center_offset(size_a, size_b):
    '''Takes the size of two objects a and b along one dimension (i.e. both
    parameters must be of the same dimension; a's width and b's width, for
    example) and returns the offset needed to place b perfectly centered within
    a along that dimension.
    '''
    return size_a // 2 - size_b // 2


def draw_str_centered(con, str_, y, *args, **kwargs):
    str_length = len(str_)
    con_width = con.width
    con.draw_str(center_offset(con_width, str_length), y, str_,
                 *args, **kwargs)
