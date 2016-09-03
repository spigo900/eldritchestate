# Game of Life, but w/ multiple states?
import tdl
import tdl.event
from tdl.event import App
import random
import gc

def main(argv=[]):
    tdl.set_font(FONT, greyscale=True, altLayout=True)
    main_con = tdl.init(MAP_SIZE, MAP_SIZE, TITLE)
    app = FogApp(main_con)
    app.run()
    del main_con
    gc.collect()

TITLE = "Fog Automaton Testing"
MAX_VAL = 15
MAP_SIZE = 16
FONT = "fonts/consolas12x12_gs_tc.png"

def adjacents(pair):
    """Get a list of all adjacent coordinates."""
    (x, y) = pair
    return [(x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)]

def multiply_colors(a, b):
    """Take two colors a and b and return their product."""
    from math import ceil
    return tuple(map((lambda x, y: ceil((x * y) / 255)), a, b))

class FogApp(App):
    def __init__(self, console):
        # self.running = True
        self.con = console
        map_init = {(x, y): random.randint(0, MAX_VAL)
                    for x in range(MAP_SIZE)
                    for y in range(MAP_SIZE)}

        self._sources = set((x, y)
            for x in range(MAP_SIZE)
            for y in range(MAP_SIZE)
                          if random.random() < 0.05)

        self.map_a = map_init
        self.map_b = self.map_a.copy()

    def ev_QUIT(self, e):
        # self.running = False
        self.suspend()

    def key_ESCAPE(self, e):
        tdl.event.push(tdl.event.Quit)

    def update(self, _dt):
        # while self.running:
        for coord_pair in self._sources:
            # if self.map_b[coord_pair] < 15:
            #     print(self.map_b[coord_pair])
            self.map_b[coord_pair] = min(MAX_VAL, self.map_a[coord_pair] + 1)
        for coord_pair in self.map_b:
            (x, y) = coord_pair
            self.map_b[coord_pair] = (max(0, self.map_a[coord_pair] - 2))
            filtered_adj = [pair for pair in adjacents(coord_pair)
                            if pair in self.map_b]
            rand_adj = random.choice(filtered_adj)
            # transfer_amt = random.randint(1, 2)
            transfer_amt = 1
            if rand_adj:
                # self.map_b[coord_pair] -= (transfer_amt - 1)
                self.map_b[rand_adj] = min(MAX_VAL, self.map_b[rand_adj] + transfer_amt)
        for coord_pair in self.map_b:
            (x, y) = coord_pair
            tile_val = self.map_b[coord_pair]
            self.con.draw_char(x, y,
                ' ', bg=3*(int(255.0*(tile_val/MAX_VAL)),))

        tdl.flush()
        tmp = self.map_a
        self.map_a = self.map_b
        self.map_b = tmp
        # self.map_a = self.map_b.copy()

if __name__ == "__main__":
    main()
