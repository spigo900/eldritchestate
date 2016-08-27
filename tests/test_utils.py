#!/bin/env python3
import eldestrl.utils as ut


def test_clamp():
    assert ut.clamp(-50, 3, 10) == 3
    assert ut.clamp(5, 3, 10) == 5
    assert ut.clamp(50, 3, 10) == 10


def test_in_range():
    assert ut.in_range(5, 3, 10)
    assert not ut.in_range(-50, 3, 10)
    assert not ut.in_range(50, 3, 10)


def test_in_rect():
    rect = ut.Rect(2, 3, 4, 5)
    assert ut.in_rect(rect, 2, 3)
    assert ut.in_rect(rect, 5, 3)
    assert ut.in_rect(rect, 2, 7)
    assert ut.in_rect(rect, 5, 7)
    assert not ut.in_rect(rect, 1, 3)
    assert not ut.in_rect(rect, 2, 2)
    assert not ut.in_rect(rect, 6, 7)
    assert not ut.in_rect(rect, 5, 8)


def test_rects_intersect():
    rect_a = ut.Rect(1, 1, 5, 5)
    rect_b = ut.Rect(2, 3, 4, 5)
    rect_c = ut.Rect(4, 6, 7, 7)
    assert ut.rects_intersect(rect_a, rect_b)
    assert ut.rects_intersect(rect_b, rect_c)
    assert not ut.rects_intersect(rect_a, rect_c)


def test_to_local_coords():
    assert ut.to_local_coords((1, 1), (5, 5)) == (4, 4)
    assert ut.to_local_coords((2, 10), (5, 5)) == (3, -5)
    assert ut.to_local_coords((10, 2), (5, 5)) == (-5, 3)
    assert ut.to_local_coords((10, 10), (5, 5)) == (-5, -5)
    assert ut.to_local_coords((-10, -10), (5, 5)) == (15, 15)


def test_adjecent():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)

    # should be associative
    assert ut.adjacent(a, b) == ut.adjacent(b, a)

    # coords should be adjacent to themselves... probably
    assert ut.adjacent(a, a)
    assert ut.adjacent(c, c)
    assert ut.adjacent(d, d)

    # testing usual cases
    assert ut.adjacent(a, b)
    assert ut.adjacent(a, c)
    assert ut.adjacent(a, d)
    assert ut.adjacent(b, d)
    assert ut.adjacent(b, e)
    assert ut.adjacent(d, f)

    # negative cases
    assert not ut.adjacent(a, f)
    assert not ut.adjacent(b, c)
    assert not ut.adjacent(b, f)
    assert not ut.adjacent(c, d)
    assert not ut.adjacent(c, e)
    assert not ut.adjacent(c, f)
    assert not ut.adjacent(d, e)


def test_orthogonal():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)

    # should be associative
    assert ut.orthogonal(a, b) == ut.orthogonal(b, a)

    # coords should also be ut.orthogonal to themselves... probably
    assert ut.orthogonal(a, a)
    assert ut.orthogonal(c, c)
    assert ut.orthogonal(d, d)

    # testing usual cases
    assert ut.orthogonal(a, b)
    assert not ut.orthogonal(a, c)
    assert not ut.orthogonal(a, d)
    assert ut.orthogonal(b, d)
    assert ut.orthogonal(b, e)
    assert not ut.orthogonal(d, f)

    # more usual cases
    assert not ut.orthogonal(a, f)
    assert not ut.orthogonal(b, c)
    assert not ut.orthogonal(b, f)
    assert not ut.orthogonal(c, d)
    assert ut.orthogonal(c, e)
    assert not ut.orthogonal(c, f)
    assert ut.orthogonal(d, e)


def test_ortho_adjacent():
    a = (0, 0)
    b = (0, 1)
    c = (-1, -1)
    d = (1, 1)
    e = (-1, 1)
    f = (2, 2)
    # should be associative
    assert ut.ortho_adjacent(a, b) == ut.ortho_adjacent(b, a)

    # should return the same as combining the plain functions does
    assert ut.ortho_adjacent(a, a) \
        == (ut.orthogonal(a, a) and ut.adjacent(a, a))
    assert ut.ortho_adjacent(a, b) \
        == (ut.orthogonal(a, b) and ut.adjacent(a, b))
    assert ut.ortho_adjacent(a, c) \
        == (ut.orthogonal(a, c) and ut.adjacent(a, c))
    assert ut.ortho_adjacent(a, d) \
        == (ut.orthogonal(a, d) and ut.adjacent(a, d))
    assert ut.ortho_adjacent(a, e) \
        == (ut.orthogonal(a, e) and ut.adjacent(a, e))
    assert ut.ortho_adjacent(a, f) \
        == (ut.orthogonal(a, f) and ut.adjacent(a, f))
    assert ut.ortho_adjacent(b, c) \
        == (ut.orthogonal(b, c) and ut.adjacent(b, c))
    assert ut.ortho_adjacent(b, d) \
        == (ut.orthogonal(b, d) and ut.adjacent(b, d))
    assert ut.ortho_adjacent(b, e) \
        == (ut.orthogonal(b, e) and ut.adjacent(b, e))
    assert ut.ortho_adjacent(b, f) \
        == (ut.orthogonal(b, f) and ut.adjacent(b, f))


def test_manhattan_dist():
    x1, y1 = 5, 5
    x2, y2 = 0, 5
    x3, y3 = 0, 0
    x4, y4 = 7, 7
    assert ut.manhattan_dist(x1, y1, x2, y2) == 5
    assert ut.manhattan_dist(x1, y1, x3, y3) == 10
    assert ut.manhattan_dist(x1, y1, x4, y4) == 4
    assert ut.manhattan_dist(x2, y2, x3, y3) == 5
    assert ut.manhattan_dist(x2, y2, x4, y4) == 9
    assert ut.manhattan_dist(x3, y3, x4, y4) == 14


def test_subtract_iterables():
    assert tuple(ut.subtract_iterables((1, 1), (5, 5))) == (-4, -4)
    assert tuple(ut.subtract_iterables((2, 10), (5, 5))) == (-3, 5)
    assert tuple(ut.subtract_iterables((10, 2), (5, 5))) == (5, -3)
    assert tuple(ut.subtract_iterables((10, 10), (5, 5))) == (5, 5)
    assert list(ut.subtract_iterables((-10, -10), (5, 5))) == [-15, -15]
    assert tuple(ut.subtract_iterables([1, 1], [5, 5])) == (-4, -4)
    assert list(ut.subtract_iterables([2, 10], [5, 5])) == [-3, 5]
    assert list(ut.subtract_iterables([10, 2], [5, 5])) == [5, -3]
    assert list(ut.subtract_iterables([10, 10], [5, 5])) == [5, 5]
    assert tuple(ut.subtract_iterables([-10, -10], [5, 5])) == (-15, -15)
    assert list(ut.subtract_iterables([-10, -10], (5, 5))) == [-15, -15]


def test_center_offset():
    assert ut.center_offset(50, 50) == 0
    assert ut.center_offset(50, 10) == 20
    assert ut.center_offset(50, 8) == 21
    assert ut.center_offset(20, 4) == 8
    assert ut.center_offset(40, 6) == 17
    assert ut.center_offset(10, 12) == -1


def test_constantly():
    fn = ut.constantly(88)
    assert fn(51, 3, 99, dog="ted", firetruck=(5, 9, 86)) == 88
    assert fn(38) == 88
    assert fn(92) == 88


def test_first_helper():
    assert ut.first_helper(iter(range(100)), "Nothing.") == 0
    assert ut.first_helper(iter(range(50, 100)), "Nothing.") == 50
    try:
        ut.first_helper(iter(range(50, 0)), StopIteration())
    except StopIteration:
        pass
    try:
        ut.first_helper(iter([]), StopIteration())
    except StopIteration:
        pass

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
COLOR1 = (100, 147, 100)
COLOR2 = (127, 127, 127)
PARCHMENT = (255, 225, 165)


def test_multiply_colors():
    assert ut.multiply_colors(COLOR1, WHITE) == COLOR1
    assert ut.multiply_colors(WHITE, COLOR1) == COLOR1
    assert ut.multiply_colors(COLOR1, BLACK) == BLACK
    assert ut.multiply_colors(BLACK, COLOR1) == BLACK
    assert ut.multiply_colors(COLOR1, COLOR2) == (50, 74, 50)
    assert ut.multiply_colors(COLOR2, COLOR1) == (50, 74, 50)


def test_to_grayscale():
    assert ut.to_grayscale(WHITE) == WHITE
    assert ut.to_grayscale(BLACK) == BLACK
    assert ut.to_grayscale((100, 100, 100)) == (100, 100, 100)
    assert ut.to_grayscale((80, 100, 120)) == (100, 100, 100)
    assert ut.to_grayscale((120, 100, 80)) == (100, 100, 100)


def test_gray_to_parchment():
    assert ut.gray_to_parchment(WHITE) == PARCHMENT
    assert ut.gray_to_parchment(BLACK) == BLACK


def test_color_to_parchment_tone():
    assert ut.color_to_parchment_tone(BLACK) == BLACK
    assert ut.color_to_parchment_tone(BLACK) == ut.gray_to_parchment(BLACK)
    assert ut.color_to_parchment_tone(WHITE) == PARCHMENT
    assert ut.color_to_parchment_tone(WHITE) == ut.gray_to_parchment(WHITE)


def test_valid_identifier():
    assert not ut.valid_identifier("55cantdrive")
    assert not ut.valid_identifier("it'smine")
    assert not ut.valid_identifier("$$bills")
    assert ut.valid_identifier("doghouse")
    assert ut.valid_identifier("dogs_house")
    assert ut.valid_identifier("_dogs_house")
    assert not ut.valid_identifier("im@dogshouse")
    assert not ut.valid_identifier("42")
    assert not ut.valid_identifier("38steves")
    assert ut.valid_identifier("my_goddamn_murderous_pony")


def test_sign():
    assert ut.sign(-32) == -1
    assert ut.sign(0) == 0
    assert ut.sign(85) == 1


def test_bresenham_line():
    origin_x, origin_y = 0, 0
    points = ((5, 0),
              (0, 5),
              (-5, 0),
              (0, -5),
              (-5, -5),
              (5, 5))
    lines = [ut.bresenham_line(origin_x, origin_y, x, y)
             for x, y in points]
    results_processed = []
    for item in lines:
        results_processed.append(ut.remove_duplicates(item))
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
    assert ut.partition(list1) == [[1], [2], [3], [4], [5]]
    assert list1 == [1, 2, 3, 4, 5]
    assert ut.partition(list2) == [[9], [88, 88], [36], [42], [5]]
    assert list2 == [9, 88, 88, 36, 42, 5]


def test_remove_duplicates():
    list1 = [1, 2, 3, 4, 5]
    list2 = [9, 88, 88, 36, 42, 5]
    list3 = [9, 1, 1, 1, 1, 8]
    assert ut.remove_duplicates(list1) == list1
    assert ut.remove_duplicates(list2) == [9, 88, 36, 42, 5]
    assert ut.remove_duplicates(list3) == [9, 1, 8]


def test_hollow_box():
    x1, y1 = 5, 5
    x2, y2 = 10, 10
    width, height = x2 - x1, y2 - y1
    inside_rect = ut.Rect(x1 + 1, y1 + 1, width - 2, height - 2)
    assert all(not ut.in_rect(inside_rect, x, y)
               for (x, y) in ut.hollow_box(x1, y1, x2, y2))
