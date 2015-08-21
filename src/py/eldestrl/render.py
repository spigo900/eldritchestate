import eldestrl.map as gmap


def lit_color(color, lighting):
    """Return the color as modified by the lighting.

    color should be any tuple of 3 ints.
    lighting should be whatever values are stored in light_map as values.
    """
    light_mult = (lighting,) * 3
    return tuple(int(n * k)
                 for n, k in zip(color, light_mult))


# rendering
def render_msgs(con, coords, msgs, n=5):
    '''Takes a console, a coordinate pair, a sliceable collection of messages
    and optionally a number of messages, and render the messages to the
    console.'''
    x, y = coords
    for i in range(1, n+1):
        con.draw_str(x, y + i, msgs[:-i])


def render_map(con, map_, refpoint, fov):
    from untdl import TDLError
    for (coord, tile_type) in map_.items():
        draw_coords = (coord[0] - refpoint[0],
                       coord[1] - refpoint[1])
        if draw_coords in con and coord in fov:
            try:
                tile_lighting = map_.light_map[coord]
                tile_info = gmap.get_tile_type(map_, tile_type)
                tile_char = tile_info['char']
                tile_fg = tile_info.get('color', (255, 255, 255))
                tile_bg = tile_info.get('bg_color', None)
                tile_bg_final = lit_color(tile_bg, tile_lighting) \
                    if tile_bg else tile_bg
                con.draw_char(draw_coords[0], draw_coords[1],
                              tile_char,
                              lit_color(tile_fg, tile_lighting),
                              tile_bg_final)
            except AttributeError:
                print('ERROR! Tile type %s does not exist'
                      'or has no display character defined!'
                      % repr(tile_type))
            except TDLError:
                print('Tile at %s not in view; skipping...' % repr(coord))
