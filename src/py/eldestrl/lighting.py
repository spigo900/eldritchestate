from math import sqrt
from eldestrl.utils import manhattan_distance


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


def lighting_manhattan_linear(i, x1, y1, x2, y2):
    return i * 1/manhattan_distance(x1, y1, x2, y2)


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


def light_line(i, line, light_fn, attenuation_fn):
    """Calculate the lighting for a series of points.

    i should be the intensity of the light source.

    line should be an iterable of points of the form (x, y), with the first
    being the origin of the light.

    light_fn should be a function which takes the intensity, the source point
    (as two numbers) and the point under consideration (as two numbers) and
    returns the lighting for the tile.

    attenuation_fn should be a function which takes the tile coordinates as two
    numbers and returns the light attenuation value for the tile.

    Return a list where each member is the lighting value for the corresponding
    point.
    """
    x_origin, y_origin = line[0]
    light_vals = []
    att = 0.0
    for (x, y) in line:
        if att >= 1.0:
            light_vals.append(0.0)
            continue
        att += attenuation_fn(x, y)
        light_base = light_fn(i, x_origin, y_origin, x, y)
        light_vals.append(light_base - att)
    return light_vals
