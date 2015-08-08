MOVE_CONTROLS_MAP = {'h': ('do_action_tile', (-1, 0)),
                     'j': ('do_action_tile', (0, 1)),
                     'k': ('do_action_tile', (0, -1)),
                     'l': ('do_action_tile', (1, 0)),
                     'y': ('do_action_tile', (-1, -1)),
                     'u': ('do_action_tile', (1, -1)),
                     'b': ('do_action_tile', (-1, 1)),
                     'n': ('do_action_tile', (1, 1)),
                     '.': ('pass')}


def get_move_diff(key_event):
    return MOVE_CONTROLS_MAP.get(key_event.char.lower(), (0, 0))
