from utils import to_local_coords, clamp


# View should look like this:
class View:
    SCROLL_EDGE_SIZE = 2

    def __init__(self, x, y, width, height):
        assert(type(x) is int and type(y) is int and
               type(width) is int and type(height) is int)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    @property
    def coords(self):
        return self.x, self.y

    @coords.setter
    def coords(self, value):
        self.x = value[0]
        self.y = value[1]


class Bounds:
    def __init__(self, left, right, upper, lower):
        self.left = left
        self.right = right
        self.upper = upper
        self.lower = lower


# map-relative
def view_edge(view, k):
    if k == 'left' or k == 'top':
        return 0
    elif k == 'right':
        return view.width
    elif k == 'bottom':
        return view.height
    raise AttributeError('Invalid edge ' + k)


def view_edge_abs(view, k):
    if k == 'left':
        return view.x
    elif k == 'right':
        return view.x + view.width - 1
    elif k == 'top':
        return view.y
    elif k == 'bottom':
        return view.y + view.height - 1
    raise AttributeError('Invalid edge ' + k)


def _scroll_edge_helper(view, k, view_edge_fn):
    edge_val = view_edge_fn(view, k)
    if k == 'left' or k == 'top':
        return edge_val + View.SCROLL_EDGE_SIZE
    else:
        return edge_val - View.SCROLL_EDGE_SIZE


def view_scroll_edge(view, k):
    return _scroll_edge_helper(view, k, view_edge)


def view_scroll_edge_abs(view, k):
    return _scroll_edge_helper(view, k, view_edge_abs)


def get_scroll_x(view, x):
    diff_x = 0
    if x < view_scroll_edge(view, 'left'):
        diff_x = x - view_scroll_edge(view, 'left')
    elif x >= view_scroll_edge(view, 'right'):
        diff_x = x - view_scroll_edge(view, 'right') + 1
    return diff_x


def get_scroll_y(view, y):
    diff_y = 0
    if y < view_scroll_edge(view, 'top'):
        diff_y = y - view_scroll_edge(view, 'top')
    elif y >= view_scroll_edge(view, 'bottom'):
        diff_y = y - view_scroll_edge(view, 'bottom') + 1
    return diff_y


def get_view_scroll(view, coords):
    '''Get the amount by which to scroll the view based on view-local
    coordinates.'''
    x, y = coords[0], coords[1]
    return get_scroll_x(view, x), get_scroll_y(view, y)


def get_view_scroll_abs(view, abs_coords):
    '''Get the amount by which to scroll the view based on absolute map
    coordinates.'''
    return get_view_scroll(view, to_local_coords(view.coords, abs_coords))


def scroll_view(view, coords):
    return View(view.x + coords[0], view.y + coords[1],
                view.width, view.height)


def scroll_view_clamped(view, diff_coords, min_coords, max_coords):
    temp_view = scroll_view(view, diff_coords)
    temp_view.coords = clamp(temp_view.coords, min_coords, max_coords)
    return temp_view


def _in_view_subarea_helper(view, coords, bounds, view_edge_fn):
    left = view_edge_fn(view, 'left') + bounds.left
    right = view_edge_fn(view, 'right') + bounds.right
    upper = view_edge_fn(view, 'top') + bounds.upper
    lower = view_edge_fn(view, 'bottom') + bounds.lower
    return True if left < coords[0] < right \
        and upper < coords[1] < lower else False


def in_view_subarea(view, coords, bounds):
    return _in_view_subarea_helper(view, coords, bounds, view_edge)


def in_view_subarea_abs(view, coords, bounds):
    return _in_view_subarea_helper(view, coords, bounds, view_edge_abs)


def in_view(view, coords):
    '''Find if the given view-relative coordinates are in the view.'''
    return in_view_subarea(view, coords, Bounds(0, 0, 0, 0))


def in_view_abs(view, coords):
    '''Find if the given absolute map coordinates are in the view.'''
    return in_view_subarea_abs(view, coords, Bounds(0, 0, 0, 0))


def at_view_edge(view, coords):
    return get_view_scroll(view, coords) != (0, 0)


def at_view_edge_abs(view, coords):
    return get_view_scroll_abs(view, coords) != (0, 0)
