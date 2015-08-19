from . import mixins  # noqa
import logging
import json


# change this at some point so it instead gets the "running directory"
# possibly, the base path should be calculated and stored in another namespace,
# though which I'm not yet sure.
PATH = ""
JSON_PATH = PATH + "data/types/tiles.json"
_tile_types = {}


def load_json():
    global _tile_types
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
        processed = [ttype]
        for mixin in ttype.get('mixins', []):
            args = mixin[1:]
            mixin = mixin[0]
            # replace this with safer, non-eval-using code later if possible
            assert not mixin.startswith('_')
            assert '()' not in mixin
            assert ';' not in mixin
            assert '\n' not in mixin
            try:
                mixin_fn = eval("mixins." + mixin)
                processed = mixin_fn(processed, *args)
            except NameError:
                log = logging.getLogger(__name__)
                log.error("In definition for type {0}:\n"
                          "No such function {0}!"
                          .format(ttype['type'], mixin))
                print("In No such function {0}! Skipping...")
        for proc_ttype in processed:
            type_name = proc_ttype['type']
            del proc_ttype['type']
            tmp.get(type_name, {}).update(proc_ttype)
    _tile_types.update(tmp)
    return tmp


def reset_types():
    global _tile_types
    _tile_types.clear()
    load_json()


def get_tile_def(typename):
    return _tile_types[typename]
