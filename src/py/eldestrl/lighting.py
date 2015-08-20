from math import abs, sqrt


def distance_squared(x1, y1, x2, y2):
    return (x2 - x1) ** 2 + (y2 - y1) ** 2


def distance(x1, y1, x2, y2):
    if x1 == x2:
        return abs(y2 - y1)
    elif y1 == y2:
        return abs(x2 - x1)
    else:
        return sqrt(distance_squared(x1, y1, x2, y2))


def lighting_const(i, _x1, _y1, _x2, _y2):
    """Calculate the lighting for a given tile using constant falloff.

    i is the light source's intensity, x1, y1 is the light source, and
    x2, y2 is the tile.
    """
    return i


def lighting_linear(i, x1, y1, x2, y2):
    """Calculate the lighting for a given tile using linear falloff.

    i is the light source's intensity, x1, y1 is the light source, and
    x2, y2 is the tile.
    """
    return i * 1/distance(x1, y1, x2, y2)


def _quadratic_helper(x1, y1, x2, y2):
    dist_sqr = distance_squared(x1, y1, x2, y2)
    return 1/dist_sqr


def lighting_quadratic(i, x1, y1, x2, y2):
    """Calculate the lighting for a given tile using quadratic falloff.

    i is the light source's intensity, x1, y1 is the light source, and
    x2, y2 is the tile.
    """
    return i * _quadratic_helper(x1, y1, x2, y2)


def lighting_quadratic_spec(i, x1, y1, x2, y2):
    """Calculate the lighting for a given tile using quadratic falloff times a
    multiplier.

    i is the light source's intensity, x1, y1 is the light source, and
    x2, y2 is the tile.

    """
    inv = _quadratic_helper(x1, y1, x2, y2)
    multiplier = 1/(inv * 2)
    return i * inv * multiplier
