from game.core.interactable import Interactable, InteractableState


class Pickable(Interactable):
    """An object that attaches to the player's camera when interacted with."""

    def __init__(self, node, prompt="Pick up"):
        super().__init__(node, prompt)
        self._original_parent = node.getParent()
        self._original_pos = node.getPos()
        self._original_scale = node.getScale()

    def on_interact(self, player):
        self.state = InteractableState.ACTIVE
        self.node.wrtReparentTo(player.camera)
        self.node.setPos(0, 1.2, -0.3)
        self.node.setScale(self._original_scale * 0.5)

    def drop(self, render):
        """Optional: put it back in the world (not wired to a key yet)."""
        self.state = InteractableState.IDLE
        self.node.wrtReparentTo(render)
        self.node.setScale(self._original_scale)


class StaticInteractable(Interactable):
    """Non-pickable — examine-only props, levers, doors, etc."""

    def __init__(self, node, prompt="Examine"):
        super().__init__(node, prompt)

    def on_interact(self, player):
        print(f"Examining {self.node.getName()}")
