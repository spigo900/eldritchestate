from ecs.models import Component


class Position(Component):
    def __init__(self, coords):
        self.coords = coords


class World(Component):
    def __init__(self, world):
        self.world = world  # world being a name for map


class Velocity(Component):
    def __init__(self):
        self.velocity_vector = (0, 0)


class Char(Component):
    def __init__(self, char, color=(255, 255, 255)):
        self.char = char
        self.color = color


class Actor(Component):
    def __init__(self):
        from collections import deque
        self.queue = deque


class PlayerControlled(Component):
    def __init__(self):
        pass


class FollowsEntity(Component):
    def __init__(self, ent):
        self.followed = ent


class BlocksMove(Component):
    def __init__(self):
        pass


class BlocksSight(Component):
    def __init__(self):
        pass


class Display(Component):
    def __init__(self, con, refpoint):
        self.con = con
