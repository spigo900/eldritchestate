import eldestrl.components as components


def new_player(em, map_, coords):
    player = em.create_entity()
    em.add_component(player, components.Position(coords))
    em.add_component(player, components.World(map_))
    em.add_component(player, components.Char('@'))
    em.add_component(player, components.Actor())
    em.add_component(player, components.PlayerControlled())
    em.add_component(player, components.BlocksMove())
    em.add_component(player, components.Sight(7.5))
    em.add_component(player, components.LightSource({"radius": 3}))
    return player


def new_camera(em, map_, con, coords):
    camera = em.create_entity()
    em.add_component(camera, components.Position(coords))
    em.add_component(camera, components.World(map_))
    em.add_component(camera, components.Display(con))
    return camera


def new_tracking_camera(em, map_, con, tracked_entity):
    camera = new_camera(em, map_, con, (1, 1))
    em.add_component(camera, components.FollowsEntity(tracked_entity))
    return camera


def new_client(em, map_, coords):
    npc = em.create_entity()
    em.add_component(npc, components.Position(coords))
    em.add_component(npc, components.World(map_))
    em.add_component(npc, components.Char('@', (200, 120, 30)))
    em.add_component(npc, components.Actor())
    em.add_component(npc, components.Sight(7.5))
    em.add_component(npc, components.AI('client'))
    return npc


def new_monster(em, map_, coords):
    npc = em.create_entity()
    em.add_component(npc, components.Position(coords))
    em.add_component(npc, components.World(map_))
    em.add_component(npc, components.Char('&', (38, 38, 38)))
    em.add_component(npc, components.Actor())
    em.add_component(npc, components.Sight(4))
    em.add_component(npc, components.DeathRadius(1))
    em.add_component(npc, components.UnlightRadius(6))
    em.add_component(npc, components.AI('monster'))
    return npc


def new_torch(ent_mgr, map_, coords):
    torch = ent_mgr.create_entity()
    ent_mgr.add_component(torch, components.Position(coords))
    ent_mgr.add_component(torch, components.LightSource({"radius": 10}))
