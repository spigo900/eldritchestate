import untdl
import untdl.event as event
import gc
import ecs.models as ecs
import eldestrl.view as view
import eldestrl.map as gmap
from eldestrl.menu import SimpleMenu
# from pprint import pprint

CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 25
TITLE = 'Eldritch Estate'

MAIN_MENU_OPTIONS = [('New Game', lambda con: game_loop(con)),
                     ('Options', lambda _: None),
                     ('Quit', lambda _: event.push(event.Quit()))]


def scroll_view_clamped_map(view_, diff_coords, map_):
    '''Takes a view, a pair of diff coordinates and a map and returns a new
    view scrolled such that it does not fall more than SCROLL_VIEW_CLAMP_AMOUNT
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
    '''Takes a tile type name and renders it on con at the given
    coordinates.'''
    tile_def = gmap.get_tile_type(tile)
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
                render_tile(con, tile, i, j)
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


# player functions
def player_move_coords(map_, player_coords, diff_x, diff_y):
    '''Takes a map, the player's current coordinates and the diff coordinates
    (which represent the direction the player wants to move in) and returns the
    new coordinates.'''
    player_x = player_coords[0]
    player_y = player_coords[1]
    new_x = player_x + diff_x
    new_y = player_y + diff_y
    return (new_x, new_y) if gmap.passable(map_, new_x, new_y) \
        else player_coords


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
            print('Object %s not in map; skipping...' % repr(obj))


# game logic
def game_loop(con):
    '''The main game loop.'''
    # TODO: Split this into separate input, output and render loops.
    untdl.event.set_key_repeat(500, 100)
    game_ended = False
    game_map = gmap.new_map()
    coords = gmap.get_player_start_pos(game_map)
    view_ = view.center_view(view.View(-2, -2, 25, 15), coords)
    # FONT_SIZE = (8, 8)
    render_view(con, game_map, coords, view_)
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


def main(argv=[]):
    main_con = untdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT, TITLE)
    app = SimpleMenu(main_con, TITLE, MAIN_MENU_OPTIONS)
    app.run()
    del main_con
    gc.collect()

if __name__ == '__main__':
    main()
