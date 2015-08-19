import eldestrl.map as gmap


# rendering
def render_tile(con, map_, tile, x, y):
    '''Takes a tile type name and renders it on con at the given
    coordinates.'''
    tile_def = gmap.get_tile_type(map_, tile)
    fg = tile_def.get('color', (255, 255, 255))
    bg = tile_def.get('bg', (0, 0, 0))
    char = tile_def['char']
    con.draw_char(x, y, char, fg, bg)


def render_view(con, map_, player_coords, view):
    '''Takes a view, map and player coordinates and renders the map and player
    to the view.'''
    for i in range(0, view.width):
        for j in range(0, view.height):
            try:
                tile = map_[(view.x+i, view.y+j)]
                render_tile(con, map_, tile, i, j)
            except KeyError:
                pass
    con.draw_char(player_coords[0] - view.x, player_coords[1] - view.y, '@')


def render_msgs(con, coords, msgs, n=5):
    '''Takes a console, a coordinate pair, a sliceable collection of messages
    and optionally a number of messages, and render the messages to the
    console.'''
    x, y = coords
    for i in range(1, n+1):
        con.draw_str(x, y + i, msgs[:-i])


def render_map(con, map_, refpoint):
    from untdl import TDLError
    for (coord, tile_type) in map_.items():
        draw_coords = (coord[0] - refpoint[0],
                       coord[1] - refpoint[1])
        if draw_coords in con:
            try:
                tile_info = gmap.get_tile_type(map_, tile_type)
                tile_char = tile_info['char']
                tile_fg = tile_info.get('color', (255, 255, 255))
                tile_bg = tile_info.get('bg_color', None)
                con.draw_char(draw_coords[0], draw_coords[1],
                              tile_char, tile_fg, tile_bg)
            except AttributeError:
                print('ERROR! Tile type %s does not exist'
                      'or has no display character defined!'
                      % repr(tile_type))
            except TDLError:
                print('Tile at %s not in view; skipping...' % repr(coord))


def render(con, objs, refpoint):
    '''Render the list of objects objs to the console or window con, localizing
    coordinates relative to refpoint.'''
    from untdl import TDLError
    for obj in objs:
        try:
            obj.draw(con, tuple((x1 - x2, y1 - y2)
                                for (x1, y1) in refpoint
                                for (x2, y2) in obj.coords), 0)
        except AttributeError:
            print('Object %s is not drawable; skipping...' % repr(obj))
        except TDLError:
            print('Object %s not in view; skipping...' % repr(obj))
