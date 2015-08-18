import untdl
import eldestrl.map as emap
import eldestrl.render as r
from time import sleep
from imp import reload


con = untdl.init(160, 90, 'test!')
my_map = None


def rel():
    reload(untdl)
    reload(emap)
    reload(r)


def render(map_):
    r.render_map(con, map_, (1, 1))
    untdl.flush()


def fixed_render():
    render(my_map)


def mapgen_callback(map_):
    r.render_map(con, map_, (1, 1))
    untdl.flush()
    sleep(3)


def new_map():
    return emap.map_gen(emap.DEFAULT_MAP_SEED, emap.DEFAULT_MAP_INFO,
                        mapgen_callback)


def remap():
    global my_map
    my_map = new_map()

sleep(0.1)
remap()
untdl.flush()
sleep(15)
