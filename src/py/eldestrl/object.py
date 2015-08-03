import weakref
from copy import deepcopy
from eldestrl.utils import adjacent, ortho_adjacent


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
                # gen = (str(x) for x in mcs.objs[type_name])
                # print('LOG: New set: %s' % ", ".join(gen))
                del_fn(self)
            return __del__

        def deepcopy_dec(deepcopy_fn):
            def __deepcopy__(self, memodict):
                new_obj = deepcopy_fn(self, memodict)
                mcs.objs[type_name].add(new_obj)
                # gen = (str(x) for x in mcs.objs[type_name])
                # print('LOG: New set: %s' % ", ".join(gen))
                return new_obj
            return __deepcopy__

        if '__del__' not in attrs:
            attrs['__del__'] = lambda _: None
        attrs['__del__'] = del_dec(attrs['__del__'])

        # if '__deepcopy__' not in attrs:
        #     def default_deepcopy(self, memo):
        #         return deepcopy(self)
        #     # attrs['__deepcopy__'] = lambda self, dic: super(type(self), self)
        #     attrs['__deepcopy__'] = default_deepcopy
        #     # attrs['__deepcopy__'] = lambda x, dic: type(x)
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

    # def __deepcopy__(self, memo):
    #     self

    def move(self, map_, coords):
        from eldestrl.map import passable
        if self.coords and \
           adjacent(self.coords, coords) and passable(map_, *coords):
            self.coords = coords


# Duck typing: a drawable component is kept in the object's 'drawable'
# attribute. It should have a method, 'draw,' which takes a console, a cell
# coordinate, and a time delta and renders itself to the given coordinate and
# does nothing else.

def make_drawfn(char, fg=(255, 255, 255), bg=(0, 0, 0)):
    def drawfn(con, cell, _time_delta):
        x, y = cell
        con.draw_char(x, y, char)
    return drawfn


draw_player = make_drawfn('@')
draw_goblin = make_drawfn('g', (35, 80, 50))


def new_player(coords):
    player = GameObject(coords)
    player.displayname = 'you'
    player.draw = draw_player
    return player


def new_monster(coords, type, properties={}):
    monster = GameObject(coords)
    monster.displayname = properties['displayname']
    if 'fn' in properties['display']:
        monster.draw = properties['display']['fn']
    else:
        monster.draw = make_drawfn(**properties.display)
    return monster


def new_monster_type(properties):
    pass


def new_goblin(coords):
    return new_monster(coords, {
        'displayname': 'goblin',
        'display': {'fn': draw_goblin}
    })
