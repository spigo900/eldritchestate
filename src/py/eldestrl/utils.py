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


def to_local_coords(ref_coords, localized):
    '''Takes two coordinate tuples and returns a new coordinate tuple which
    represents the difference between ref_coords and localized (used to get
    coords relative to view, for example).
    '''
    from operator import sub
    return tuple(map(sub, localized, ref_coords))


def adjacent(coords_a, coords_b):
    '''Takes a pair of coordinates and returns whether or not they're adjacent.
    Does not take into account whether the tiles are passable or even exist
    within the map -- or in any map, for that matter. Remember to check that
    they do exist and, optionally, are passable as necessary.
    '''

    ax, ay = coords_a
    bx, by = coords_b
    return -1 <= ax - bx <= 1 and -1 <= ay - by <= 1


def orthogonal(coords_a, coords_b):
    '''Returns true if the given coordinates are either in the same row or the same
    column.
    '''
    ax, ay = coords_a
    bx, by = coords_b
    return ax == bx or ay == by


def ortho_adjacent(coords_a, coords_b):
    '''Works like adjacent, but returns true only if the tiles are orthogonally
    adjacent.
    '''
    ax, ay = coords_a
    bx, by = coords_b
    return (-1 <= ax - bx <= 1 and ay == by) or \
        (-1 <= ay - by <= 1 and ax == bx)
    # return adjacent(coords_a, coords_b) and orthogonal(coords_a, coords_b)


def manhattan_dist(x1, y1, x2, y2):
    return abs((x2 - x1) + (y2 - y1))


def subtract_iterables(iter_a, iter_b):
    '''Takes two iterables a and b and return a new iterable whose value is a -
    b for each member of a and each member of b.'''
    from operator import sub
    return map(sub, iter_a, iter_b)


def center_offset(size_a, size_b):
    '''Takes the size of two objects a and b along one dimension (i.event. both
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


def constantly(value):
    '''Return a function which accepts any number of arguments whose return is
    always `value` (i.event. a constant function.).

    '''
    return lambda *_s, **_kws: value


def first_helper(iter_, err):
    try:
        return next(iter_)
    except StopIteration:
        raise err


def has_component(ent_mgr, ent, component):
    from ecs.exceptions import NonexistentComponentTypeForEntity
    try:
        ent_mgr.component_for_entity(ent, component)
        return True
    except NonexistentComponentTypeForEntity:
        return False


def multiply_colors(a, b):
    """Take two colors a and b and return their product."""
    return tuple(map((lambda x, y: (x * y) // 255), a, b))


def to_grayscale(color):
    return (sum(color) // 3,) * 3


PARCHMENT_RATIO = (51, 45, 31)


def gray_to_parchment(color):
    denominator = max(PARCHMENT_RATIO)
    return tuple(int(x * n // denominator)
                 for x in color
                 for n in PARCHMENT_RATIO)


def color_to_parchment_tone(color):
    return gray_to_parchment(to_grayscale(color))


def valid_identifier(s):
    """Returns true if the given string is a valid Python identifier."""
    from keyword import iskeyword
    import re
    return re.match("[_A-Za-z][_a-zA-Z0-9]*$", s) and not iskeyword(s)


def get_event_key(event):
    """Returns the key for an UnTDL key event."""
    return event.keychar if event.key == 'CHAR' else event.key
