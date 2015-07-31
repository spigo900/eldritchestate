#!/bin/env python3
# utilities
def clamp(val, min_, max_):
    return min(max(val, min_), max_)


def in_range(val, min_, max_):
    return True if min_ <= val <= max_ else False


def to_local_coords(coords_a, coords_b):
    '''
    Return a new coordinate pair which represents the difference between
    coords_a and coords_b (used to get coords relative to view, for example).
    '''
    return (coords_b[0] - coords_a[0], coords_b[1] - coords_a[1])
