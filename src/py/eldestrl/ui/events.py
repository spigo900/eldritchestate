import untdl.event as ev


class DoneCurrentState(ev.Event):
    type = "DONECURSTATE"


class NewState(ev.Event):
    type = "NEWSTATE"

    def __init__(self, state):
        # state should be an instance of a state-like object, not a state
        # class; this makes it possible to pass parameters to the new state
        # created
        self.state = state


class EscapeState(ev.Event):
    type = "ESCAPESTATE"


class UIChoice(ev.Event):
    type = "CHOICE"

    def __init__(self, choice):
        # A more generic version of ItemChosen; should work for directions,
        # items, or pretty much anything, really.
        #
        # For item choices, choice should be an entity ID if items are entities
        # and an item representation if items are represented as items...
        # probably. It might be a list index instead. Actually, it'll probably
        # be a list index. That simplifies things and means that the item
        # choosing code is ignorant of the ECS, so I can change to objects
        # instead of ECS if I want... at least in theory.
        #
        # Yeah, just make it a list index for item choice screens.
        self.choice = choice
