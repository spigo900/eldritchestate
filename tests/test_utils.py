#!/bin/env python3
from eldestrl.utils import *  # noqa


def test_clamp():
    assert clamp(-50, 3, 10) == 3
    assert clamp(5, 3, 10) == 5
    assert clamp(50, 3, 10) == 10


def test_in_range():
    assert in_range(5, 3, 10)
    assert not in_range(-50, 3, 10)
    assert not in_range(50, 3, 10)


def test_in_rect():
    rect = Rect(2, 3, 4, 5)
    assert in_rect(rect, 2, 3)
    assert in_rect(rect, 5, 3)
    assert in_rect(rect, 2, 7)
    assert in_rect(rect, 5, 7)
    assert not in_rect(rect, 1, 3)
    assert not in_rect(rect, 2, 2)
    assert not in_rect(rect, 6, 7)
    assert not in_rect(rect, 5, 8)


def test_rects_intersect():
    rect_a = Rect(1, 1, 5, 5)
    rect_b = Rect(2, 3, 4, 5)
    rect_c = Rect(4, 6, 7, 7)
    assert rects_intersect(rect_a, rect_b)
    assert rects_intersect(rect_b, rect_c)
    assert not rects_intersect(rect_a, rect_c)


def test_to_local_coords():
    assert to_local_coords((1, 1), (5, 5)) == (4, 4)
    assert to_local_coords((2, 10), (5, 5)) == (3, -5)
    assert to_local_coords((10, 2), (5, 5)) == (-5, 3)
    assert to_local_coords((10, 10), (5, 5)) == (-5, -5)
    assert to_local_coords((-10, -10), (5, 5)) == (15, 15)


def test_adjecent():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)

    # should be associative
    assert adjacent(a, b) == adjacent(b, a)

    # coords should be adjacent to themselves... probably
    assert adjacent(a, a)
    assert adjacent(c, c)
    assert adjacent(d, d)

    # testing usual cases
    assert adjacent(a, b)
    assert adjacent(a, c)
    assert adjacent(a, d)
    assert adjacent(b, d)
    assert adjacent(b, e)
    assert adjacent(d, f)

    # negative cases
    assert not adjacent(a, f)
    assert not adjacent(b, c)
    assert not adjacent(b, f)
    assert not adjacent(c, d)
    assert not adjacent(c, e)
    assert not adjacent(c, f)
    assert not adjacent(d, e)


def test_orthogonal():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)

    # should be associative
    assert orthogonal(a, b) == orthogonal(b, a)

    # coords should also be orthogonal to themselves... probably
    assert orthogonal(a, a)
    assert orthogonal(c, c)
    assert orthogonal(d, d)

    # testing usual cases
    assert orthogonal(a, b)
    assert not orthogonal(a, c)
    assert not orthogonal(a, d)
    assert orthogonal(b, d)
    assert orthogonal(b, e)
    assert not orthogonal(d, f)

    # more usual cases
    assert not orthogonal(a, f)
    assert not orthogonal(b, c)
    assert not orthogonal(b, f)
    assert not orthogonal(c, d)
    assert orthogonal(c, e)
    assert not orthogonal(c, f)
    assert orthogonal(d, e)


def test_ortho_adjacent():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)
    # should be associative
    assert ortho_adjacent(a, b) == ortho_adjacent(b, a)

    # should return the same as combining the plain functions does
    assert ortho_adjacent(a, a) == (orthogonal(a, a) and adjacent(a, a))
    assert ortho_adjacent(a, b) == (orthogonal(a, b) and adjacent(a, b))
    assert ortho_adjacent(a, c) == (orthogonal(a, c) and adjacent(a, c))
    assert ortho_adjacent(a, d) == (orthogonal(a, d) and adjacent(a, d))
    assert ortho_adjacent(a, e) == (orthogonal(a, e) and adjacent(a, e))
    assert ortho_adjacent(a, f) == (orthogonal(a, f) and adjacent(a, f))
    assert ortho_adjacent(b, c) == (orthogonal(b, c) and adjacent(b, c))
    assert ortho_adjacent(b, d) == (orthogonal(b, d) and adjacent(b, d))
    assert ortho_adjacent(b, e) == (orthogonal(b, e) and adjacent(b, e))
    assert ortho_adjacent(b, f) == (orthogonal(b, f) and adjacent(b, f))


def test_manhattan_dist():
    x1, y1 = 5, 5
    x2, y2 = 0, 5
    x3, y3 = 0, 0
    x4, y4 = 7, 7
    assert manhattan_dist(x1, y1, x2, y2) == 5
    assert manhattan_dist(x1, y1, x3, y3) == 10
    assert manhattan_dist(x1, y1, x4, y4) == 4
    assert manhattan_dist(x2, y2, x3, y3) == 5
    assert manhattan_dist(x2, y2, x4, y4) == 9
    assert manhattan_dist(x3, y3, x4, y4) == 14


def test_subtract_iterables():
    assert tuple(subtract_iterables((1, 1), (5, 5))) == (-4, -4)
    assert tuple(subtract_iterables((2, 10), (5, 5))) == (-3, 5)
    assert tuple(subtract_iterables((10, 2), (5, 5))) == (5, -3)
    assert tuple(subtract_iterables((10, 10), (5, 5))) == (5, 5)
    assert list(subtract_iterables((-10, -10), (5, 5))) == [-15, -15]
    assert tuple(subtract_iterables([1, 1], [5, 5])) == (-4, -4)
    assert list(subtract_iterables([2, 10], [5, 5])) == [-3, 5]
    assert list(subtract_iterables([10, 2], [5, 5])) == [5, -3]
    assert list(subtract_iterables([10, 10], [5, 5])) == [5, 5]
    assert tuple(subtract_iterables([-10, -10], [5, 5])) == (-15, -15)
    assert list(subtract_iterables([-10, -10], (5, 5))) == [-15, -15]


def test_center_offset():
    assert center_offset(50, 50) == 0
    assert center_offset(50, 10) == 20
    assert center_offset(50, 8) == 21
    assert center_offset(20, 4) == 8
    assert center_offset(40, 6) == 17
    assert center_offset(10, 12) == -1


def test_constantly():
    fn = constantly(88)
    assert fn(51, 3, 99, dog="ted", firetruck=(5, 9, 86)) == 88
    assert fn(38) == 88
    assert fn(92) == 88


def test_first_helper():
    assert first_helper(iter(range(100)), "Nothing.") == 0
    assert first_helper(iter(range(50, 100)), "Nothing.") == 50
    try:
        first_helper(iter(range(50, 0)), StopIteration())
    except StopIteration:
        pass
    try:
        first_helper(iter([]), StopIteration())
    except StopIteration:
        pass

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR1 = (100, 147, 100)
COLOR2 = (127, 127, 127)
PARCHMENT = (255, 225, 165)


def test_multiply_colors():
    assert multiply_colors(COLOR1, WHITE) == COLOR1
    assert multiply_colors(WHITE, COLOR1) == COLOR1
    assert multiply_colors(COLOR1, BLACK) == BLACK
    assert multiply_colors(BLACK, COLOR1) == BLACK
    assert multiply_colors(COLOR1, COLOR2) == (50, 74, 50)
    assert multiply_colors(COLOR2, COLOR1) == (50, 74, 50)


def test_to_grayscale():
    assert to_grayscale(WHITE) == WHITE
    assert to_grayscale(BLACK) == BLACK
    assert to_grayscale((100, 100, 100)) == (100, 100, 100)
    assert to_grayscale((80, 100, 120)) == (100, 100, 100)
    assert to_grayscale((120, 100, 80)) == (100, 100, 100)


def test_gray_to_parchment():
    assert gray_to_parchment(WHITE) == PARCHMENT
    assert gray_to_parchment(BLACK) == BLACK


def test_color_to_parchment_tone():
    assert color_to_parchment_tone(BLACK) == BLACK
    assert color_to_parchment_tone(BLACK) == gray_to_parchment(BLACK)
    assert color_to_parchment_tone(WHITE) == PARCHMENT
    assert color_to_parchment_tone(WHITE) == gray_to_parchment(WHITE)


def test_valid_identifier():
    assert not valid_identifier("55cantdrive")
    assert not valid_identifier("it'smine")
    assert not valid_identifier("$$bills")
    assert valid_identifier("doghouse")
    assert valid_identifier("dogs_house")
    assert valid_identifier("_dogs_house")
    assert not valid_identifier("im@dogshouse")
    assert not valid_identifier("42")
    assert not valid_identifier("38steves")
    assert valid_identifier("my_goddamn_murderous_pony")


def test_sign():
    assert sign(-32) == -1
    assert sign(0) == 0
    assert sign(85) == 1


def test_bresenham_line():
    origin_x, origin_y = 0, 0
    points = ((5, 0),
              (0, 5),
              (-5, 0),
              (0, -5),
              (-5, -5),
              (5, 5))
    lines = [bresenham_line(origin_x, origin_y, x, y)
             for x, y in points]
    results_processed = []
    for item in lines:
        results_processed.append(remove_duplicates(item))
    assert results_processed[0] == [(0, 0), (1, 0), (2, 0),
                                    (3, 0), (4, 0), (5, 0)]
    assert results_processed[1] == [(0, 0), (0, 1), (0, 2),
                                    (0, 3), (0, 4), (0, 5)]
    assert results_processed[2] == [(0, 0), (-1, 0), (-2, 0),
                                    (-3, 0), (-4, 0), (-5, 0)]
    assert results_processed[3] == [(0, 0), (0, -1), (0, -2),
                                    (0, -3), (0, -4), (0, -5)]
    assert results_processed[4] == [(0, 0), (-1, -1), (-2, -2),
                                    (-3, -3), (-4, -4), (-5, -5)]
    assert results_processed[5] == [(0, 0), (1, 1), (2, 2),
                                    (3, 3), (4, 4), (5, 5)]


def test_partition():
    list1 = [1, 2, 3, 4, 5]
    list2 = [9, 88, 88, 36, 42, 5]
    assert partition(list1) == [[1], [2], [3], [4], [5]]
    assert list1 == [1, 2, 3, 4, 5]
    assert partition(list2) == [[9], [88, 88], [36], [42], [5]]
    assert list2 == [9, 88, 88, 36, 42, 5]


def test_remove_duplicates():
    list1 = [1, 2, 3, 4, 5]
    list2 = [9, 88, 88, 36, 42, 5]
    list3 = [9, 1, 1, 1, 1, 8]
    assert remove_duplicates(list1) == list1
    assert remove_duplicates(list2) == [9, 88, 36, 42, 5]
    assert remove_duplicates(list3) == [9, 1, 8]


def test_hollow_box():
    x1, y1 = 5, 5
    x2, y2 = 10, 10
    width, height = x2 - x1, y2 - y1
    inside_rect = Rect(x1 + 1, y1 + 1, width - 2, height - 2)
    assert all(not in_rect(inside_rect, x, y)
               for (x, y) in hollow_box(x1, y1, x2, y2))
