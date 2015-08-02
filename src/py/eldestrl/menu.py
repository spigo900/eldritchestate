import untdl
import untdl.event as event
from untdl.event import App


class SimpleMenu(App):

    def __init__(self, console, header, opts):
        self.header = header
        self.console = console
        self.opts = opts
        self._idx = 0

    @property
    def idx(self):
        return self._idx

    @idx.setter
    def idx(self, val):
        num_opts = len(self.opts)
        new_idx = val
        while not 0 <= new_idx < num_opts:
            if new_idx < 0:
                new_idx = num_opts + val
            elif new_idx >= num_opts:
                new_idx = new_idx - num_opts
        self._idx = new_idx

    def move_cursor(self, delta):
        self.idx += delta

    def set_cursor(self, idx):
        self.idx = idx

    def cursor_up(self):
        self.idx -= 1

    def cursor_down(self):
        self.idx += 1

    def key_CHAR(self, e):
        if e.char == 'j':
            self.cursor_down()
        elif e.char == 'k':
            self.cursor_up()

    def key_UP(self, e):
        self.cursor_up()

    def key_DOWN(self, e):
        self.cursor_down()

    def key_ENTER(self, e):
        option = self.opts[self.idx][1]
        self.console.clear()
        option(self.console)

    def key_ESCAPE(self, e):
        event.push(event.Quit())

    def ev_MOUSEMOTION(self, e):
        # TODO: mouse handling code
        pass

    def ev_QUIT(self, e):
        self.suspend()

    def write_centered_string(self, str_, y, *args, **kwargs):
        str_length = len(str_)
        con_width = self.console.width
        self.console.draw_str(con_width // 2 - str_length // 2, y,
                              str_, *args, **kwargs)

    def write_option(self, idx, y, *args, **kwargs):
        if idx == self.idx and not args and 'bgcolor' not in kwargs:
            kwargs['bgcolor'] = (80, 80, 80)
        self.write_centered_string(self.opts[idx][0], y, *args, **kwargs)

    def update(self, time_delta):
        self.console.clear()
        num_opts = len(self.opts)
        # _, height = self.console.get_size()
        height = self.console.height
        self.write_centered_string(self.header, 3)
        for i, (option, _) in enumerate(self.opts):
            self.write_option(i, height // 2 - num_opts + i)
        untdl.flush()
