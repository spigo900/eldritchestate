# Game of Life, but w/ multiple states?
import tdl
import tdl.event
from tdl.event import App
from time import sleep
from pprint import pprint
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
    (x, y) = pair
    return [(x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)]


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
    print(source_pos)
    x0, y0 = source_pos
    out = {
        (x0 + x, y0 + y): (
            1/(2*dist((x0, y0), (x0 + x, y0 + y)))
            # if (x0 - x) != 0 and (y0 - y) != 0 else 1.0
            # if (x0 != x or y0 != y) and source_pos != (x0 + x, y0 + y) else 1.0
            if source_pos != (x0 + x, y0 + y) else 1.0
            # if x0 != x or y0 != y else 1.0
        )
        for x in range(-FOG_RANGE, FOG_RANGE+1)
        for y in range(-FOG_RANGE, FOG_RANGE+1)
        if in_map((x0 + x, y0 + y))
    }
    # pprint(out)
    if source_pos in out and out[source_pos] != 1.0:
        print("Source pos does not have the correct fog value in the fog map.")
    return out


class FogApp(App):
    def __init__(self, console):
        # self.running = True
        self.con = console
        # map_init = {(x, y): random.randint(0, MAX_FOG)
        #             for x in range(MAP_SIZE)
        #             for y in range(MAP_SIZE)}

        self.width = console.width
        self.height = console.height

        self._sources_a = set(
            (x, y)
            for x in range(MAP_SIZE)
            for y in range(MAP_SIZE)
            if random.random() < 0.03)
        # self._sources_a = set()
        # self._sources_a.add((8, 8))
        self._sources_b = set()

        # self.map_out = map_init
        # self.map_b = self.map_a.copy()

    def ev_QUIT(self, e):
        self.suspend()

    def key_ESCAPE(self, e):
        tdl.event.push(tdl.event.Quit)

    def update(self, _dt):
        for coord_pair in self._sources_a:
            # COMMENTED OUT UNTIL I GET THIS SHIT WORKING
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
        print("PRINTING!")
        # # print([(pair, round(val, 2)) for (pair, val) in final_map.items()
        # #        if val > 0.1])
        # # print("Sources: {}".format(self._sources_a))
        print("Sources:")
        pprint(self._sources_a)
        # # print("Maps: {}".format(maps))
        # print()
        # print("Maps:")
        # pprint(maps)
        print()
        print()

        # draw the fog map
        for coord_pair in final_map:
            (x, y) = coord_pair
            fog_val = final_map[coord_pair]
            # if fog_val >= 0.5:
            #     print("A THING HAPPENED AT {}!".format(coord_pair))
            self.con.draw_char(
                # x, y, ' ', bg=3*(int(255.0*(fog_val/MAX_FOG)),))
                x, y, ' ', bg=3*(int(255.0*fog_val),))

        # DEBUG: check final map for source value sanity.

        tdl.flush()
        sleep(2)

        self._sources_a = self._sources_b
        self._sources_b = set()

if __name__ == "__main__":
    main()
