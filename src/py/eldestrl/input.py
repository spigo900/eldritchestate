from eldestrl.utils import get_event_key


MOVE_CONTROLS_MAP = {'h': ('do_action_tile', (-1, 0)),
                     'j': ('do_action_tile', (0, 1)),
                     'k': ('do_action_tile', (0, -1)),
                     'l': ('do_action_tile', (1, 0)),
                     'y': ('do_action_tile', (-1, -1)),
                     'u': ('do_action_tile', (1, -1)),
                     'b': ('do_action_tile', (-1, 1)),
                     'n': ('do_action_tile', (1, 1)),
                     'H': ('run_dir', (-1, 0)),
                     'J': ('run_dir', (0, 1)),
                     'K': ('run_dir', (0, -1)),
                     'L': ('run_dir', (1, 0)),
                     'Y': ('run_dir', (-1, -1)),
                     'U': ('run_dir', (1, -1)),
                     'B': ('run_dir', (-1, 1)),
                     'N': ('run_dir', (1, 1))}


def get_action_key(key_event):
    '''Get the action tuple for a given key.'''
    print("Got key event structure!: {}".format(key_event))
    key = get_event_key(key_event)
    return MOVE_CONTROLS_MAP.get(key, (None,))


def get_action(event):
    '''Get an action tuple for a given event.

    Should handle both keyboard events and, eventually, mouse events.
    '''
    return get_action_key(event)
