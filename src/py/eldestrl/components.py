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
        self.queue = deque()


class PlayerControlled(Component):
    def __init__(self):
        pass


class AI(Component):
    def __init__(self, type_):
        self.type = type_
        self.target = None


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
    def __init__(self, con):
        self.con = con


class LightSource(Component):
    def __init__(self, props):
        self.props = props


class Sight(Component):
    def __init__(self, radius, min_light=0.2):
        self.radius = radius
        self.min_light = min_light
        self.in_sight = set()


class DeathRadius(Component):
    def __init__(self, radius, counters):
        self.radius = radius
        self.counters = counters


class UnlightRadius(Component):
    def __init__(self, radius):
        self.radius = radius
