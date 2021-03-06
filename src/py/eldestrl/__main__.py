import tdl
import tdl.event as event
import gc
import sys
import time
import random
from ecs.managers import EntityManager, SystemManager
import eldestrl.map as eldmap
import eldestrl.mapgen as eldmapgen
import eldestrl.ent_templates as ents
import eldestrl.systems as systems
import eldestrl.utils as utils
from eldestrl.menu import SimpleMenu

CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 25
TITLE = 'Eldritch Estate'

MAIN_MENU_OPTIONS = [('New Game', lambda con: game_loop(con)),
                     ('Options', lambda _: None),
                     ('Quit', lambda _: event.push(event.Quit()))]

MAX_CLIENTS = 3


# game logic
def game_loop(con):
    '''The main game loop.'''
    tdl.event.set_key_repeat(500, 100)
    game_map = eldmapgen.new_map()
    ent_mgr = EntityManager()

    player_coords = eldmap.random_unoccupied(ent_mgr, game_map,
                                             eldmapgen.DEFAULT_MAP_SEED)
    player = ents.new_player(ent_mgr, game_map, player_coords)
    torch_coords = eldmap.random_unoccupied(ent_mgr, game_map,
                                            eldmapgen.DEFAULT_MAP_SEED)
    client_list = []
    for _ in range(random.randint(1, MAX_CLIENTS)):
        for client_coords in utils.adjacent8(player_coords):
            if eldmap.passable(ent_mgr, game_map, client_coords):
                client_list.append(
                    (ents.new_client(ent_mgr, game_map, client_coords),
                     client_coords))
                break

    ents.new_torch(ent_mgr, game_map, torch_coords)
    # ents.new_client(ent_mgr, game_map, (8, 3))
    main_display = tdl.Window(con, 0, 0, 25, 15)
    ents.new_tracking_camera(ent_mgr, game_map, main_display, player)

    sys_mgr = SystemManager(ent_mgr)
    sys_mgr.add_system(systems.UpdateWorldSys())
    sys_mgr.add_system(systems.LightingSys(game_map))
    sys_mgr.add_system(systems.FOVSys())
    sys_mgr.add_system(systems.FOWSys())
    fog_sys = systems.FogSys((main_display.width, main_display.height))
    sys_mgr.add_system(fog_sys)

    event_sys = systems.EventSys(CONSOLE_WIDTH, CONSOLE_HEIGHT)
    sys_mgr.add_system(event_sys)
    sys_mgr.add_system(systems.AISys())
    sys_mgr.add_system(systems.ActorSys())
    sys_mgr.add_system(systems.FollowEntitySys())
    sys_mgr.add_system(systems.RenderDisplaySys(fog_sys.get_fogmap))
    start_time = utils.cur_time_ms()
    prev_time = start_time
    cur_time = prev_time
    while not event_sys.game_ended:
        cur_time = utils.cur_time_ms()
        sys_mgr.update(cur_time - prev_time)  # 0 is a placeholder value
        prev_time = cur_time

FONT = 'fonts/consolas12x12_gs_tc.png'


def main(argv=[]):
    tdl.set_font(FONT, greyscale=True, altLayout=True)
    main_con = tdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT, TITLE)
    app = SimpleMenu(main_con, TITLE, MAIN_MENU_OPTIONS)
    app.run()
    del main_con
    gc.collect()


if __name__ == '__main__':
    sys.exit(main())
