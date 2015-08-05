from ecs.models import Component


class Position(Component):
    def __init__(self, coords):
        self.coords = coords


class Velocity(Component):
    def __init__(self):
        self.velocity_vector = (0, 0)


class Char(Component):
    def __init__(self, char, color=(255, 255, 255)):
        self.char = char
        self.color = color


class PlayerControlled(Component):
    def __init__(self):
        pass


class Blocks(Component):
    def __init__(self):
        pass
