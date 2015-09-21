import eldestrl.components as components


def new_player(dt, map_, coords):
    player = dt.create_entity()
    dt.add_component(player, components.Position(coords))
    dt.add_component(player, components.World(map_))
    dt.add_component(player, components.Char('@'))
    dt.add_component(player, components.Actor())
    dt.add_component(player, components.PlayerControlled())
    dt.add_component(player, components.BlocksMove())
    dt.add_component(player, components.Sight(7.5))
    return player


def new_camera(dt, map_, con, coords):
    camera = dt.create_entity()
    dt.add_component(camera, components.Position(coords))
    dt.add_component(camera, components.World(map_))
    dt.add_component(camera, components.Display(con))
    return camera


def new_tracking_camera(dt, map_, con, tracked_entity):
    camera = new_camera(dt, map_, con, (1, 1))
    dt.add_component(camera, components.FollowsEntity(tracked_entity))
    return camera


def new_client(dt, map_, coords):
    npc = dt.create_entity()
    dt.add_component(npc, components.Position(coords))
    dt.add_component(npc, components.World(map_))
    dt.add_component(npc, components.Char('@', (200, 120, 30)))
    dt.add_component(npc, components.Actor())
    dt.add_component(npc, components.Sight(7.5))
    dt.add_component(npc, components.AI('client'))
    return npc


def new_monster(dt, map_, coords):
    npc = dt.create_entity()
    dt.add_component(npc, components.Position(coords))
    dt.add_component(npc, components.World(map_))
    dt.add_component(npc, components.Char('&', (38, 38, 38)))
    dt.add_component(npc, components.Actor())
    dt.add_component(npc, components.Sight(4))
    dt.add_component(npc, components.DeathRadius(1))
    dt.add_component(npc, components.UnlightRadius(6))
    dt.add_component(npc, components.AI('monster'))
    return npc


def new_torch(ent_mgr, map_, coords):
    torch = ent_mgr.create_entity()
    ent_mgr.add_component(torch, components.Position(coords))
    ent_mgr.add_component(torch, components.LightSource({"radius": 10}))
