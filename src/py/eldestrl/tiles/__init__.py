from . import mixins, behaviors  # noqa
from eldestrl.utils import valid_identifier
import logging
import json


# change this at some point so it instead gets the "running directory"
# possibly, the base path should be calculated and stored in another namespace,
# though which I'm not yet sure.
PATH = ""
JSON_PATH = PATH + "data/types/tiles.json"


def process_mixins(type_def):
    """Process mixins for the given tile type definition."""
    processed_def = [type_def]
    for mixin in type_def.get('mixins', []):
            args = mixin[1:]
            mixin = mixin[0]
            try:
                mixin_fn = getattr(mixins, mixin)
                processed_def = mixin_fn(processed_def, *args)
            except AttributeError:
                log = logging.getLogger(__name__)
                log.error("In definition for type {}:\n"
                          "No such mixin {}!"
                          .format(type_def['type'], mixin))
    return processed_def


def process_args(args):
    """Process a JSON-read arglist.

    args should be a list, where each item is a value. JSON objects should map
    valid Python identifiers to values to be used as keyword arguments."""
    new_args = []
    kwargs = {}
    for arg in args:
        try:
            assert all(valid_identifier(k) for k in arg.keys())
            kwargs.update(arg)
        except AttributeError:
            new_args.append(arg)
    return new_args, kwargs


def process_behaviors(type_def):
    processed_def = type_def.copy()
    behaviors_ = processed_def.setdefault('behaviors', {})
    for k, behavior in behaviors_.items():
        first, *rest = behavior
        try:
            getattr(behaviors, first)
        except AttributeError:
            log = logging.getLogger(__name__)
            log.error("In definition for type {}:\n"
                      "No such behavior {}!"
                      .format(type_def['type'], first))
        else:
            args, kwargs = process_args(rest)
            behaviors_[k] = (first, args, kwargs)
    return processed_def


def get_behavior(type_def, behavior_name):
    return type_def.get('behaviors', {}).get(behavior_name, None)


def do_action(ent_mgr, ent, map_, pos, action):
    args, kwargs = action[1:]
    action = action[0]
    action_fn = getattr(behaviors, action)
    action_fn(ent_mgr, ent, map_, pos, *args, **kwargs)


def maybe_do_action(ent_mgr, ent, map_, pos, action):
    if action:
        do_action(ent_mgr, ent, map_, pos, action)


def load_json():
    with open(JSON_PATH) as f:
        content = json.load(f)
    tmp = {}
    for ttype in content:
        assert 'char' in ttype
        assert len(ttype['char']) == 1
        ttype.setdefault('color', (255, 255, 255))
        ttype.setdefault('blocks', False)
        ttype.setdefault('blocks_sight', False)
        type_name = ttype['type']
        assert type_name not in tmp
        tmp[type_name] = ttype
        processed = process_mixins(ttype)
        for proc_ttype in processed:
            proc_ttype.update(process_behaviors(proc_ttype))
            type_name = proc_ttype['type']
            del proc_ttype['type']
            tmp.setdefault(type_name, {}).update(proc_ttype)
    return tmp


def reset_types(types):
    types.clear()
    types.update(load_json())


def get_tile_def(types, typename):
    return types[typename]
