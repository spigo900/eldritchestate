import weakref
from copy import deepcopy
from eldestrl.utils import adjacent
from collections import deque


# Thought: Maybe I should make a metaclass here. I could have it register the
# objects with a global registry and object types with another. Or... no, maybe
# I should make a metaclass for object types and leave the object creation code
# alone. That probably makes more sense.
#
# Or does it? Do I really need a new class for every object type? Seems a bit
# excessive. Although... nah, it wouldn't be. Because I'm really defining the
# classes for object kinds, not exact types. Kinds being things like 'player,'
# and 'NPC,' and 'monster,' and 'client.' So it should be fine.

# TODO: add proper docstrings and comments for this monster.

class ObjectType(type):
    '''Metaclass for object types, which handles registering new types and
    registering/deregistering objects.

    '''
    types = {}
    objs = {}

    def __new__(mcs, clsname, bases, attrs):
        type_name = clsname.lower()
        print('LOG: Created new object type %(type_name)s.' % locals())
        if type_name not in ObjectType.types:
            mcs.types[type_name] = {}
            mcs.objs[type_name] = weakref.WeakSet()
        else:
            raise ValueError('Cannot have two object types'
                             'named %(type_name)s!' % locals())

        def del_dec(del_fn):
            def __del__(self):
                mcs.objs[type_name].remove(self)
                del_fn(self)
            return __del__

        def deepcopy_dec(deepcopy_fn):
            def __deepcopy__(self, memodict):
                new_obj = deepcopy_fn(self, memodict)
                mcs.objs[type_name].add(new_obj)
                return new_obj
            return __deepcopy__

        if '__del__' not in attrs:
            attrs['__del__'] = lambda _: None
        attrs['__del__'] = del_dec(attrs['__del__'])

        if '__deepcopy__' not in attrs:
            def tricky_copy(self, memo):
                try:
                    self.__deepcopy__ = None
                    new = deepcopy(self)
                finally:
                    self.__copy__ = tricky_copy
                return new
            attrs['__deepcopy__'] = tricky_copy
        attrs['__deepcopy__'] = deepcopy_dec(attrs['__deepcopy__'])

        return super(ObjectType, mcs).__new__(mcs, clsname, bases, attrs)

    def __call__(cls, *args, **kwargs):
        type_name = cls.__name__.lower()
        print('LOG: Creating new object of type %(type_name)s.' % locals())
        new_obj = type.__call__(cls, *args, **kwargs)
        type(cls).objs[type_name].add(new_obj)
        return new_obj


class GameObject(metaclass=ObjectType):
    def __init__(self, coords):
        self.coords = coords

    def move(self, map_, coords):
        from eldestrl.map import passable
        # I should really probably remove these checks... maybe move the
        # passability logic into a component or something. I mean, these are
        # eldritch abominations. What if I end up wanting one that can walk
        # through walls or something?
        if self.coords and \
           adjacent(self.coords, coords) and passable(map_, *coords):
            self.coords = coords


# Duck typing: a drawable component is kept in the object's 'drawable'
# attribute. It should have a method, 'draw,' which takes a console, a cell
# coordinate, and a time delta and renders itself to the given coordinate and
# does nothing else.

def new_player(coords):
    player = GameObject(coords)
    player.displayname = 'you'
    player.draw = DrawChar('@')
    return player


# TODO: figure out how to implement monster types properly. Will probably
# involve (chain) mappings and the global object type registry somehow.

# def new_monster(coords, type_, properties={}):
#     monster = GameObject(coords)
#     monster.displayname = properties['displayname']
#     if 'fn' in properties['display']:
#         monster.draw = properties['display']['fn']
#     else:
#         monster.draw = make_drawfn(**properties['display'])
#     return monster


# def new_monster_type(properties):
#     pass


def new_goblin(coords):
    goblin = GameObject(coords)
    goblin.displayname = 'goblin'
    goblin.draw = DrawChar('g', (35, 80, 50))
    return goblin
#     return new_monster(coords, {
#         'displayname': 'goblin',
#         'display': {'fn': DrawChar('g', (35, 80, 50))}
#     })


class MetaComponent(type):
    '''Metaclass for component types, which handles automatic registering of new
    types.

    '''
    types = {}

    def __new__(mcs, clsname, bases, attrs):
        type_name = clsname.lower()
        print('LOG: Creating new component type %(type_name)s.' % locals())
        if type_name not in MetaComponent.types:
            new_class = super(MetaComponent, mcs) \
                        .__new__(mcs, clsname, bases, attrs)
            mcs.types[type_name] = {}
        else:
            raise ValueError('Multiple component types %(type_name)s!'
                             % locals())

        return new_class

    def __call__(cls, *args, **kwargs):
        type_name = cls.__name__.lower()
        print('LOG: Creating new component of type %(type_name)s.' % locals())
        return type.__call__(cls, *args, **kwargs)


class DrawChar(metaclass=MetaComponent):
    '''A simple drawing component. Renders a single character to the given
    console.

    '''
    def __init__(self, char, fgcolor=(255, 255, 255), bgcolor=None):
        self._char = char
        self._fg = fgcolor
        self._bg = bgcolor

    def __call__(self, con, cell, time_delta):
        x, y = cell
        con.draw_char(x, y, self._char, self._fg, self._bg)


class InputActor(metaclass=MetaComponent):
    '''An actor component. This one is meant to by used by the player object and to
    get its actions from the input code.

    '''
    def __init__(self):
        self.actions = deque()

    def update(self, actor):
        for (x, y) in self.actions:
            try:
                actor.travel((x, y))
            except:
                print('Actor %s couldn\'t move to coords (%d, %d).'
                      % (actor, x, y))
