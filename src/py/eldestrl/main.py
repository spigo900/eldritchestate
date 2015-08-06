import untdl
import untdl.event as event
import gc
from ecs.managers import EntityManager, SystemManager
import eldestrl.view as view
import eldestrl.map as gmap
import eldestrl.ent_templates as ents
import eldestrl.systems as systems
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


# game logic
def game_loop(con):
    '''The main game loop.'''
    untdl.event.set_key_repeat(500, 100)
    game_map = gmap.new_map()
    ent_mgr = EntityManager()

    player_coords = gmap.get_player_start_pos(game_map)
    player = ents.new_player(ent_mgr, game_map, player_coords)
    main_display = untdl.Window(con, 0, 0, 25, 15)
    ents.new_tracking_camera(ent_mgr, game_map, main_display, player)

    sys_mgr = SystemManager(ent_mgr)
    sys_mgr.add_system(systems.UpdateWorldSys())

    event_sys = systems.EventSys()
    sys_mgr.add_system(event_sys)
    sys_mgr.add_system(systems.ActorSys())
    sys_mgr.add_system(systems.FollowEntitySys())
    sys_mgr.add_system(systems.RenderDisplaySys())
    # FONT_SIZE = (8, 8)
    while not event_sys.game_ended:
        # elif key.keychar == 'ESCAPE' or key.alt and 'F4' in key.key:
        #     game_ended = True
        sys_mgr.update(ent_mgr)


def main(argv=[]):
    main_con = untdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT, TITLE)
    app = SimpleMenu(main_con, TITLE, MAIN_MENU_OPTIONS)
    app.run()
    del main_con
    gc.collect()

if __name__ == '__main__':
    main()
