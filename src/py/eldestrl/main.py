import untdl
import untdl.event as event
import gc
from ecs.managers import EntityManager, SystemManager
import eldestrl.map as eldmap
import eldestrl.ent_templates as ents
import eldestrl.systems as systems
from eldestrl.menu import SimpleMenu

CONSOLE_WIDTH = 80
CONSOLE_HEIGHT = 25
TITLE = 'Eldritch Estate'

MAIN_MENU_OPTIONS = [('New Game', lambda con: game_loop(con)),
                     ('Options', lambda _: None),
                     ('Quit', lambda _: event.push(event.Quit()))]


# game logic
def game_loop(con):
    '''The main game loop.'''
    untdl.event.set_key_repeat(500, 100)
    game_map = eldmap.new_map()
    ent_mgr = EntityManager()

    player_coords = eldmap.first_unoccupied(ent_mgr, game_map)
    player = ents.new_player(ent_mgr, game_map, player_coords)
    # ents.new_client(ent_mgr, game_map, (8, 3))
    main_display = untdl.Window(con, 0, 0, 25, 15)
    ents.new_tracking_camera(ent_mgr, game_map, main_display, player)

    sys_mgr = SystemManager(ent_mgr)
    sys_mgr.add_system(systems.UpdateWorldSys())

    event_sys = systems.EventSys()
    sys_mgr.add_system(event_sys)
    sys_mgr.add_system(systems.AISys())
    sys_mgr.add_system(systems.ActorSys())
    sys_mgr.add_system(systems.FollowEntitySys())
    sys_mgr.add_system(systems.RenderDisplaySys())
    while not event_sys.game_ended:
        sys_mgr.update(0)  # 0 is a placeholder value


def main(argv=[]):
    main_con = untdl.init(CONSOLE_WIDTH, CONSOLE_HEIGHT, TITLE)
    app = SimpleMenu(main_con, TITLE, MAIN_MENU_OPTIONS)
    app.run()
    del main_con
    gc.collect()

if __name__ == '__main__':
    main()
