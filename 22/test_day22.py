import pytest
from day22 import read_input, Point


grid = [['.' if x == '#' else x for x in line] for line in read_input()[0]]


@pytest.mark.parametrize('point, face, expect, newface', [
    (Point(99, 10), '>', Point(100, 10), '>'),
    (Point(60, 49), 'v', Point(60, 50), 'v'),
    (Point(60, 0), '^', Point(0, 160), '>'),
    (Point(50, 10), '<', Point(0, 139), '>'),

    (Point(149, 10), '>', Point(99, 139), '<'),
    (Point(110, 49), 'v', Point(99, 60), '<'),
    (Point(110, 0), '^', Point(10, 199), '^'),
    (Point(100, 10), '<', Point(99, 10), '<'),

    (Point(99, 60), '>', Point(110, 49), '^'),
    (Point(60, 99), 'v', Point(60, 100), 'v'),
    (Point(60, 50), '^', Point(60, 49), '^'),
    (Point(50, 60), '<', Point(10, 100), 'v'),

    (Point(99, 110), '>', Point(149, 39), '<'),
    (Point(60, 149), 'v', Point(49, 160), '<'),
    (Point(60, 100), '^', Point(60, 99), '^'),
    (Point(50, 110), '<', Point(49, 110), '<'),

    (Point(49, 110), '>', Point(50, 110), '>'),
    (Point(10, 149), 'v', Point(10, 150), 'v'),
    (Point(10, 100), '^', Point(50, 60), '>'),
    (Point(0, 110), '<', Point(50, 39), '>'),

    (Point(49, 160), '>', Point(60, 149), '^'),
    (Point(10, 199), 'v', Point(110, 0), 'v'),
    (Point(10, 150), '^', Point(10, 149), '^'),
    (Point(0, 160), '<', Point(60, 0), 'v'),
])
def test_move2(point, face, expect, newface):
    assert grid[point.y][point.x] == '.'
    assert point.move2(face, grid) == (expect, newface)
