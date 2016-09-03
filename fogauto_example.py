# Game of Life, but w/ multiple states?
import tdl
import random

def main(argv=[]):
    tdl.set_font(FONT, greyscale=True, altLayout=True)
    main_con = tdl.init(MAP_SIZE, MAP_SIZE, TITLE)
    app = App(main_con)
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

class App:
    def __init__(self, console):
        self.running = True
        self.con = console

    def ev_QUIT(self, e):
        self.running = False

    def run(self):
        map_init = {(x, y): random.randint(0, MAX_VAL)
                    for x in range(MAP_SIZE)
                    for y in range(MAP_SIZE)}

        map_sources = set((x, y)
            for x in range(MAP_SIZE)
            for y in range(MAP_SIZE)
                          if random.random() < 0.05)

        map_a = map_init
        map_b = {}
        while self.running:
            map_b = map_a.copy()
            for coord_pair in map_sources:
                # if map_b[coord_pair] < 15:
                #     print(map_b[coord_pair])
                map_b[coord_pair] = min(MAX_VAL, map_a[coord_pair] + 1)
            for coord_pair in map_b:
                (x, y) = coord_pair
                map_b[coord_pair] = (max(0, map_b[coord_pair] - 2))
                filtered_adj = [pair for pair in adjacents(coord_pair)
                                if pair in map_b]
                rand_adj = random.choice(filtered_adj)
                # transfer_amt = random.randint(1, 2)
                transfer_amt = 1
                if rand_adj:
                    # map_b[coord_pair] -= (transfer_amt - 1)
                    map_b[rand_adj] = min(MAX_VAL, map_b[rand_adj] + transfer_amt)
            for coord_pair in map_b:
                (x, y) = coord_pair
                tile_val = map_b[coord_pair]
                self.con.draw_char(x, y,
                    ' ', bg=3*(int(255.0*(tile_val/MAX_VAL)),))

            tdl.flush()
            map_a = map_b

if __name__ == "__main__":
    main()
