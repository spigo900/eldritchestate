# Game of Life, but w/ multiple states?
import tdl
import tdl.event
from tdl.event import App
from time import sleep
import random
import math
import gc


def main(argv=[]):
    tdl.set_font(FONT, greyscale=True, altLayout=True)
    main_con = tdl.init(MAP_SIZE, MAP_SIZE, TITLE)
    app = FogApp(main_con)
    app.run()
    del main_con
    gc.collect()

TITLE = "Fog Automaton Testing"
MAX_FOG = 15
MAP_SIZE = 16
FOG_RANGE = 12
FONT = "fonts/consolas12x12_gs_tc.png"


def adjacents(pair):
    """Get a list of all adjacent coordinates."""
    (x0, y0) = pair
    return [(x0 + x, y0 + y)
            for x in range(-1, 2)
            for y in range(-1, 2)
            if x != 0 or y != 0]


def in_map(coord_pair):
    (x, y) = coord_pair
    return x >= 0 and y >= 0 \
        and x < MAP_SIZE and y < MAP_SIZE


def multiply_colors(a, b):
    """Take two colors a and b and return their product."""
    from math import ceil
    return tuple(map((lambda x, y: ceil((x * y) / 255)), a, b))


def dist2(pos1, pos2):
    """Return the distance squared between pos1 and pos2."""
    x1, y1 = pos1
    x2, y2 = pos2
    return ((x1 - x2)**2 + (y1 - y2)**2)


def dist(pos1, pos2):
    """Return the distance between pos1 and pos2."""
    return math.sqrt(dist2(pos1, pos2))


def generate_fog_map(source_pos):
    """
    Take a fog source position and return a map giving the fog values at
    each position.
    """
    x0, y0 = source_pos
    return {
        (x0 + x, y0 + y): (
            1/(2*dist((x0, y0), (x0 + x, y0 + y)))
            if source_pos != (x0 + x, y0 + y) else 1.0
        )
        for x in range(-FOG_RANGE, FOG_RANGE+1)
        for y in range(-FOG_RANGE, FOG_RANGE+1)
        if in_map((x0 + x, y0 + y))
    }


class FogApp(App):
    def __init__(self, console):
        self.con = console

        self.width = console.width
        self.height = console.height

        sources_a = [
            (x, y)
            for x in range(MAP_SIZE)
            for y in range(MAP_SIZE)
            if random.random() < 0.03
        ]
        if len(sources_a) > 7:
            sources_a = sources_a[0:6]
        self._sources_a = set(sources_a)
        self._sources_b = set()

    def ev_QUIT(self, e):
        self.suspend()

    def key_ESCAPE(self, e):
        tdl.event.push(tdl.event.Quit)

    def update(self, _dt):
        for coord_pair in self._sources_a:
            filtered_adj = [(x, y) for (x, y) in adjacents(coord_pair)
                            if in_map((x, y))]
            pick = random.choice(filtered_adj)
            # confusing phrasing, but should be skipped when pick hasn't
            # already been 'picked' by/for another source.
            while pick in self._sources_b:
                pick = random.choice(filtered_adj)
            self._sources_b.add(pick)

        # now generate the fog maps
        maps = []
        final_map = {}
        for source in self._sources_b:
            maps.append(generate_fog_map(source))

        # resolve conflicting map values and merge
        for map_ in maps:
            conflicts = final_map.keys() & map_.keys()
            tmp_map = {}
            for key in conflicts:
                tmp_map[key] = max(map_[key], final_map[key])
            final_map.update(map_)
            final_map.update(tmp_map)

        # draw the fog map
        for coord_pair in final_map:
            (x, y) = coord_pair
            fog_val = final_map[coord_pair]
            self.con.draw_char(
                x, y, ' ', bg=3*(int(255.0*fog_val),))

        tdl.flush()

        self._sources_a = self._sources_b
        self._sources_b = set()
        sleep(0.25)

if __name__ == "__main__":
    main()
