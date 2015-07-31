import untdl
import gc
import errors
from copy import deepcopy
from pprint import pprint

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

TILES = {'floor': {'char': '.',
                   'passable': True},
         'wall': {'char': '+',
                  'passable': False}}

MAP = {(x, y): ('wall' if x == 1 or x == 25 or
                y == 1 or y == 15 else 'floor')
       for x in range(1,26) for y in range (1,16)}

VIEW = {'x': 1,
        'y': 1,
        'width': 40,
        'height': 15}


# utilities
def clamp(val, min_, max_):
    return min(max(val, min_), max_)

# map functions
def min_map(map_):
    return min(map_.keys())

def max_map(map_):
    return max(map_.keys())

def in_map(map_, x, y):
    return True if (x, y) in map_ else False

def passable(map_, x, y):
    tile = map_[x, y]
    return TILES[tile]['passable']

def first_matching(map_, pred):
    for (x, y), _ in sorted(map_.items()):
        if pred(map_, x, y):
            return (x, y)
    raise NoneInMapError("No tiles in map match predicate!")

def first_in_map(map_):
    return first_matching(map_, in_map)

def first_passable(map_):
    return first_matching(map_, lambda map_, x, y: in_map(map_, x, y) and passable(map_, x, y))

# view functions
def render_view(con, map_, player_coords, view):
    x = view['x']
    y = view['y']
    width = view['width']
    height = view['height']
    for i in range(0, width+1):
        for j in range(0, height+1):
            try:
                tile = map_[(x+i, y+j)]
                render_tile(con, tile, i, j)
            except KeyError:
                pass
    con.draw_char(player_coords[0] - x, player_coords[1] - y, '@')

def clamp_coord(view, x, y, map_):
    newx = clamp(view['x'] + x, min_map(map_)[0] - 5, max_map[0] + 5)
    newy = clamp(view['y'] + y, min_map(map_)[1] - 5, max_map[1] + 5)
    return (newx, newy)

def shift_view(view, x, y, map_):
    coords = clamp_coord(view, x, y, map_)
    view['x'] += coords[0]
    view['y'] += coords[1]

# rendering
def render_tile(con, tile, x, y):
    tile_def = TILES[tile]
    fg = tile_def.get('color', (255, 255, 255))
    bg = tile_def.get('bg', (0, 0, 0))
    char = tile_def['char']
    con.draw_char(x, y, char, fg, bg)

# player functions
def player_move(map_, player_coords, diff_x, diff_y):
    player_x = player_coords[0]
    player_y = player_coords[1]
    new_x = player_x + diff_x
    new_y = player_y + diff_y
    return (new_x, new_y) if in_map(map_, new_x, new_y) \
        and passable(map_, new_x, new_y) else player_coords


# game logic
def game_loop():
    con = untdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT, title='testme')
    untdl.event.set_key_repeat(500, 100)
    game_ended = False
    coords = first_passable(MAP)
    # FONT_SIZE = (8, 8)
    render_view(con, MAP, coords, VIEW)
    try:
        while not game_ended:
            untdl.flush()
            key = untdl.event.key_wait()
            if key.char in MOVE_CONTROLS_MAP:
                diff_x, diff_y = MOVE_CONTROLS_MAP[key.char]
                coords = player_move(MAP, coords, diff_x, diff_y)
            elif key.keychar == 'ESCAPE' or key.alt and 'F4' in key.key:
                game_ended = True
            con.clear()
            render_view(con, MAP, coords, VIEW)
    finally:
        del con
        gc.collect()

game_loop()
