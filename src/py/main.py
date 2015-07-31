import untdl
import gc
import view
import game.map as gmap
from errors import NoneInMapError
from utils import clamp
# from pprint import pprint

CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 25

MOVE_CONTROLS_MAP = {'h': (-1, 0),
                     'j': (0, 1),
                     'k': (0, -1),
                     'l': (1, 0),
                     'y': (-1, -1),
                     'u': (1, -1),
                     'b': (-1, 1),
                     'n': (1, 1)}


def scroll_view_clamped_map(view_, diff_coords, map_):
    '''Take a view, a pair of diff coordinates and a map and return a new view
    scrolled such that it does not fall more than SCROLL_VIEW_CLAMP_AMOUNT
    units outside the bounds of the map.'''
    SCROLL_VIEW_CLAMP_AMOUNT = 5
    map_min = gmap.min_map(map_)
    map_max = gmap.max_map(map_)
    clamp_min = (map_min[0] - SCROLL_VIEW_CLAMP_AMOUNT,
                 map_min[1] - SCROLL_VIEW_CLAMP_AMOUNT)
    clamp_max = (map_max[0] - SCROLL_VIEW_CLAMP_AMOUNT,
                 map_max[1] - SCROLL_VIEW_CLAMP_AMOUNT)
    return view.scroll_view_clamped(view_, diff_coords,
                                    clamp_min, clamp_max)


# rendering
def render_tile(con, tile, x, y):
    '''Take a tile type name and render it on con at the given coordinates.'''
    tile_def = gmap.get_tile_type(tile)
    fg = tile_def.get('color', (255, 255, 255))
    bg = tile_def.get('bg', (0, 0, 0))
    char = tile_def['char']
    con.draw_char(x, y, char, fg, bg)


def render_view(con, map_, player_coords, view):
    '''Take a view, map and player coordinates and render the map and player to
    the view.'''
    for i in range(0, view.width):
        for j in range(0, view.height):
            try:
                tile = map_[(view.x+i, view.y+j)]
                render_tile(con, tile, i, j)
            except KeyError:
                pass
    con.draw_char(player_coords[0] - view.x, player_coords[1] - view.y, '@')


# player functions
def player_move_coords(map_, player_coords, diff_x, diff_y):
    '''Take a map, the player's current coordinates and the diff coordinates
    (which represent the direction the player wants to move in) and return the
    new coordinates.'''
    player_x = player_coords[0]
    player_y = player_coords[1]
    new_x = player_x + diff_x
    new_y = player_y + diff_y
    return (new_x, new_y) if gmap.passable(map_, new_x, new_y) \
        else player_coords


# game logic
def game_loop():
    '''The main game loop.'''
    # TODO: Split this into separate input, output and render loops.
    con = untdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT, title='testme')
    untdl.event.set_key_repeat(500, 100)
    game_ended = False
    game_map = gmap.new_map()
    coords = gmap.get_player_start_pos(game_map)
    view_ = view.center_view(view.View(-2, -2, 10, 10), coords)
    # FONT_SIZE = (8, 8)
    render_view(con, game_map, coords, view_)
    try:
        while not game_ended:
            untdl.flush()
            key = untdl.event.key_wait()
            if key.char in MOVE_CONTROLS_MAP:
                diff_x, diff_y = MOVE_CONTROLS_MAP[key.char]
                new_coords = player_move_coords(game_map, coords,
                                                diff_x, diff_y)
                if new_coords != coords:
                    coords = new_coords
                    view_ = view.scroll_view(view_,
                                             (diff_x, diff_y))
                assert(coords in game_map)
            elif key.keychar == 'ESCAPE' or key.alt and 'F4' in key.key:
                game_ended = True
            con.clear()
            render_view(con, game_map, coords, view_)
    finally:
        del con
        gc.collect()

if __name__ == '__main__':
    game_loop()
