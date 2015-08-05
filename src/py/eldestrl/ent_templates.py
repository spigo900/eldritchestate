import eldestrl.components as components


def new_player(dt, map_, coords):
    player = dt.create_entity()
    dt.add_component(player, components.Position(coords))
    dt.add_component(player, components.World(map_))
    dt.add_component(player, components.Char('@'))
    dt.add_component(player, components.Actor())
    dt.add_component(player, components.PlayerControlled())
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
