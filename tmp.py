def draw_box(con, x, y, width, height, fg=(255, 255, 255), bg=None, fill=True):
    """Draw a box on the console."""
    con.draw_char(x, y, b'\xDA', fg, bg)  # upper left corner
    con.draw_char(x + width - 1, y, b'\xBF', fg, bg)  # upper right corner
    con.draw_char(x, y + height - 1, b'\xC0', fg, bg)  # lower left corner
    con.draw_char(x + width - 1, y + height - 1, b'\xD9', fg, bg)  # lower right corner
    horiz_start = x + 1
    for i in range(0, width - 2):
        con.draw_char(horiz_start + i, y, b'\xC4', fg, bg)  # horizontal sections
        con.draw_char(horiz_start + i, y + height - 1, b'\xC4', fg, bg)

    vert_start = y + 1
    for i in range(0, height - 2):
        con.draw_char(x, vert_start + i, b'\xB3', fg, bg)  # vertical sections
        con.draw_char(x + width - 1, vert_start + i, b'\xB3', fg, bg)

    if fill:
        con.draw_rect(1, 1, width - 2, height - 2, ' ', bgcolor=bg)


def draw_box_thick(con, x, y, width, height,
                   fg=(255, 255, 255), bg=None, fill=True):
    """Draw a wall-style box on the console."""
    con.draw_char(x, y, b'\xC9', fg, bg)
    con.draw_char(x + width - 1, y, b'\xBB', fg, bg)
    con.draw_char(x, y + height - 1, b'\xC8', fg, bg)
    con.draw_char(x + width - 1, y + height - 1, b'\xBC', fg, bg)
    horiz_start = x + 1
    for i in range(0, width - 2):
        con.draw_char(horiz_start + i, y, b'\xCD', fg, bg)
        con.draw_char(horiz_start + i, y + height - 1, b'\xCD', fg, bg)

    vert_start = y + 1
    for i in range(0, height - 2):
        con.draw_char(x, vert_start + i, b'\xBA', fg, bg)
        con.draw_char(x + width - 1, vert_start + i, b'\xBA', fg, bg)

    if fill:
        con.draw_rect(1, 1, width - 2, height - 2, ' ', bgcolor=bg)


def adjacents(x, y):
    """Get a list of all adjacent coordinates."""
    return [(x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)]
