import eldestrl.map as gmap
from eldestrl.utils import to_grayscale


def lit_color(color, lighting):
    """Return the color as modified by the lighting.

    color should be any tuple of 3 ints.
    lighting should be whatever values are stored in light_map as values.
    """
    return tuple(int(lighting * n) for n in color)


def fog_color(color, fog):
    gray = to_grayscale(color)
    return lit_color(gray, fog * 0.25)


# rendering
def render_msgs(con, coords, msgs, n=5):
    '''Render a list of messages to a console.'''
    x, y = coords
    for i in range(1, n+1):
        con.draw_str(x, y + i, msgs[:-i])


def render_map(con, map_, refpoint, fov, fogmap, seen):
    from tdl import TDLError
    fogmap = dict(fogmap)
    for (coord, tile_type) in map_.items():
        draw_coords = (coord[0] - refpoint[0],
                       coord[1] - refpoint[1])
        draw_x, draw_y = draw_coords
        if draw_coords in con:
            try:
                tile_lighting = map_.light_map[coord]
                tile_info = gmap.get_tile_type(map_, tile_type)
                tile_char = tile_info['char']
                tile_fg = tile_info.get('color', (255, 255, 255))
                tile_bg = tile_info.get('bg_color', None)
                tile_bg_final = lit_color(tile_bg, tile_lighting) \
                    if tile_bg else tile_bg
                if coord in fov:
                    con.draw_char(draw_x, draw_y,
                                  tile_char,
                                  lit_color(tile_fg, tile_lighting),
                                  tile_bg_final)
                elif coord in seen:
                    fog = fogmap[draw_x, draw_y]
                    tile_bg_final = fog_color(tile_bg, tile_lighting) \
                        if tile_bg else tile_bg
                    con.draw_char(draw_x, draw_y,
                                  tile_char,
                                  fog_color(tile_fg, fog),
                                  tile_bg_final)
            except AttributeError:
                print('ERROR! Tile type %s does not exist'
                      'or has no display character defined!'
                      % repr(tile_type))
            except TDLError:
                print('Tile at %s not in view; skipping...' % repr(coord))
