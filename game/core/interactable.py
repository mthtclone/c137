from enum import Enum, auto


class InteractableState(Enum):
    IDLE = auto()
    HIGHLIGHTED = auto()
    ACTIVE = auto()
    DISABLED = auto()


class Interactable:
    """Base class for objects the player can use."""

    def __init__(self, node, prompt="Interact"):
        self.node = node
        self.prompt = prompt
        self.state = InteractableState.IDLE

    def can_interact(self):
        return self.state is not InteractableState.DISABLED

    def on_focus(self):
        if self.state is InteractableState.IDLE:
            self.state = InteractableState.HIGHLIGHTED

    def on_blur(self):
        if self.state is InteractableState.HIGHLIGHTED:
            self.state = InteractableState.IDLE

    # def on_interact(self, player):
    #     raise NotImplementedError


class Door(Interactable):
    """A door that toggles between closed and open."""

    def __init__(self, node, open_angle=90):
        super().__init__(node, "Open")
        self.closed_heading = node.getH()
        self.open_angle = open_angle
        self.is_open = False

    def on_interact(self, player):
        self.is_open = not self.is_open
        self.node.setH(self.closed_heading + (self.open_angle if self.is_open else 0))
        self.prompt = "Close" if self.is_open else "Open"
