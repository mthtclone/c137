from enum import Enum, auto


class InteractableState(Enum):
    IDLE = auto()
    HIGHLIGHTED = auto()
    ACTIVE = auto()
    DISABLED = auto()


class Interactable:
    """Base class for anything a player can interact with."""

    def __init__(self, node, prompt="Interact"):
        self.node = node
        self.prompt = prompt
        self.state = InteractableState.IDLE

    def can_interact(self):
        return self.state != InteractableState.DISABLED

    def on_focus(self):
        """Called once when the player's look-ray lands on this object."""
        if self.state == InteractableState.IDLE:
            self.state = InteractableState.HIGHLIGHTED

    def on_blur(self):
        """Called once when the player looks away."""
        if self.state == InteractableState.HIGHLIGHTED:
            self.state = InteractableState.IDLE

    def on_interact(self, player):
        """Subclasses define what actually happens on interact."""
        raise NotImplementedError
