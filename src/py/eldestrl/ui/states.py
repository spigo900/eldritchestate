import logging
from ecs.exceptions import NonexistentComponentTypeForEntity
import tdl.event as ev
import eldestrl.ui.events as eldevs
import eldestrl.components as comp
import eldestrl.input as eldinput


class UIState:
    def __init__(self, con):
        # con should be the Console object all states share and draw to in
        # succession
        self.con = con

    def handle_event(self, event):
        pass

    def draw(self):
        pass


class Play(UIState):
    def __init__(self, con, ent_mgr):
        self.ent_mgr = ent_mgr
        self.input_handlers = \
            {"do_action_tile": self.do_action_tile,
             "run_dir": self.run_dir,
             "quit": self.quit}

    def _do_move_tile_common(self, player_ent, move_diff, action_type):
        assert (-1, -1) <= move_diff <= (1, 1)
        actor = self.ent_mgr.component_for_entity(player_ent, comp.Actor)
        actor.queue.append((action_type, move_diff))

    def do_action_tile(self, player_ent, move_diff):
        self._do_move_tile_common(player_ent, move_diff, 'do_action_tile')

    def run_dir(self, player_ent, move_diff):
        self._do_move_tile_common(player_ent, move_diff, 'run_dir')

    def quit(self, *_):
        ev.push(eldevs.EscapeState())

    def handle_event(self, event):
        if event.type == "MOUSEMOTION" or \
           event.type == "MOUSEDOWN" or event.type == "MOUSEUP":
            return
        for (entity, _) in self.ent_mgr.pairs_for_type(comp.PlayerControlled):
            action, *params = eldinput.get_action(event)
            try:
                handler_fn = self.input_handlers[action]
                handler_fn(entity, *params)
            except KeyError:
                log = logging.getLogger(__name__)
                log.error("Don't know how to handle action {}!".format(action))
            except NonexistentComponentTypeForEntity as err:
                print('Player-controlled entity {}'
                      'has no component {}!'
                      .format(err.entity, err.component_type))

    def draw(self):
        # problem: how do I ensure I'm not accidentally drawing over the game
        # area?
        pass


class Look(UIState):
    def handle_event(self, event):
        # should move the point somehow; might need the ent. mgr. to do that.
        pass

    def draw(self):
        # should draw the display name of the tile under point
        pass


def get_index(char):
    keys = "abcdefgijklmnopqrstuvwxABCDEFGIJKLMNOPQRSTUVWX"
    return keys.find(char)


# there are no items yet; this should be more useful when there are.
class ChooseItem(UIState):
    def __init__(self, con, items):
        # items is a list of items to choose from; should be generic enough to
        # handle choosing from inventory *and* choosing from tiles
        self.con = con
        self.items = items

    def handle_event(self, event):
        key = event.keychar
        idx = get_index(key)
        if idx != -1 and idx < len(self.items) and key:
            # we're done; tell the event handler we're done and send the choice
            # back to the state below us in the stack
            ev.push(eldevs.DoneState())
            ev.push(eldevs.UIChoice(idx))
        elif event.key == "ESCAPE":
            ev.push(eldevs.EscapeState())

    def draw(self):
        pass


class ChooseDir(UIState):
    def handle_event(self, event):
        dir_ = eldinput.get_dir(event)
        if (-1, -1) <= dir_ <= (1, 1):
            ev.push(eldevs.DoneState())
            ev.push(eldevs.UIChoice(dir_))
