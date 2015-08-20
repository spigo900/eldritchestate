class LineChar:
    HORIZONTAL_THIN = b'\xC4'
    VERTICAL_THIN = b'\xB3'
    HORIZONTAL_THICK = b'\xCD'
    VERTICAL_THICK = b'\xBA'


def draw_horiz(con, x1, x2, y, char):
    for x in range(min(x1, x2), max(x1, x2) + 1):
        con.draw_char(x, y, char)


def draw_vert(con, y1, y2, x, char):
    for y in range(min(y1, y2), max(y1, y2) + 1):
        con.draw_char(x, y, char)


def draw_box(con, x, y, width, height, fg=(255, 255, 255), bg=None, fill=True):
    """Draw a box on the console."""
    # upper left corner
    con.draw_char(x, y, b'\xDA', fg, bg)
    # upper right corner
    con.draw_char(x + width - 1, y, b'\xBF', fg, bg)
    # lower left corner
    con.draw_char(x, y + height - 1, b'\xC0', fg, bg)
    # lower right corner
    con.draw_char(x + width - 1, y + height - 1, b'\xD9', fg, bg)
    horiz_start = x + 1
    for i in range(0, width - 2):
        con.draw_char(horiz_start + i, y, LineChar.HORIZONTAL_THIN, fg, bg)
        con.draw_char(horiz_start + i, y + height - 1,
                      LineChar.HORIZONTAL_THIN, fg, bg)

    vert_start = y + 1
    for i in range(0, height - 2):
        con.draw_char(x, vert_start + i, LineChar.VERTICAL_THIN, fg, bg)
        con.draw_char(x + width - 1, vert_start + i,
                      LineChar.VERTICAL_THIN, fg, bg)

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
        con.draw_char(horiz_start + i, y, LineChar.HORIZONTAL_THICK, fg, bg)
        con.draw_char(horiz_start + i, y + height - 1,
                      LineChar.HORIZONTAL_THICK, fg, bg)

    vert_start = y + 1
    for i in range(0, height - 2):
        con.draw_char(x, vert_start + i, LineChar.VERTICAL_THICK, fg, bg)
        con.draw_char(x + width - 1, vert_start + i,
                      LineChar.VERTICAL_THICK, fg, bg)

    if fill:
        con.draw_rect(1, 1, width - 2, height - 2, ' ', bgcolor=bg)


def adjacents(x, y):
    """Get a list of all adjacent coordinates."""
    return [(x, y - 1),
            (x - 1, y),
            (x + 1, y),
            (x, y + 1)]
