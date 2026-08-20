from game.core.interactable import Interactable, InteractableState


class Pickable(Interactable):
    """An object the player can hold."""

    HOLD_POSITION = (0, 1.2, -0.3)
    HOLD_SCALE = 0.5

    def __init__(self, node, prompt="Pick up"):
        super().__init__(node, prompt)
        self.scale = node.getScale()

    def can_interact(self):
        return super().can_interact() and self.state is not InteractableState.ACTIVE

    def on_interact(self, player):
        self.state = InteractableState.ACTIVE
        self.node.wrtReparentTo(player.camera)
        self.node.setPos(*self.HOLD_POSITION)
        self.node.setScale(self.scale * self.HOLD_SCALE)

    def drop(self, render):
        self.node.wrtReparentTo(render)
        self.node.setScale(self.scale)
        self.state = InteractableState.IDLE
