from enum import Enum, auto


class InteractableState(Enum):
    IDLE = auto()
    HIGHLIGHTED = auto()
    ACTIVE = auto()
    DISABLED = auto()


class Interactable:
    """Base class for anything a player can interact with."""

    def __init__(self, node, prompt="Interact", interaction_key="E"):
        self.node = node
        self.prompt = prompt
        self.interaction_key = interaction_key
        self.state = InteractableState.IDLE
        self.default_color = node.getColor()
        self.default_scale = node.getScale()

    def can_interact(self):
        return self.state != InteractableState.DISABLED

    def on_focus(self):
        """Called when the player looks at this object."""
        if self.state == InteractableState.IDLE:
            self.state = InteractableState.HIGHLIGHTED
            self.node.setColor(1.0, 0.86, 0.25, 1.0)
            self.node.setScale(self.default_scale * 1.08)

    def on_blur(self):
        """Called when the player stops looking at this object."""
        if self.state == InteractableState.HIGHLIGHTED:
            self.state = InteractableState.IDLE
            self.node.setColor(self.default_color)
            self.node.setScale(self.default_scale)

    def on_interact(self, player):
        """Override in subclasses."""
        raise NotImplementedError

