from panda3d.core import BitMask32

from game.core.interactable import Interactable, InteractableState


class Pickable(Interactable):
    """An item the player can pick up and drop with E."""

    def __init__(self, node, collision_node, prompt="Pick up"):
        super().__init__(node, prompt, interaction_key="E")
        self.collision_node = collision_node

    def on_interact(self, player):
        if self.state == InteractableState.ACTIVE:
            return

        # Only one item is shown in the left hand at a time.
        if player.held_pickable:
            player.held_pickable.drop(player)

        self.pick_up(player)

    def pick_up(self, player):
        self.on_blur()
        self.state = InteractableState.ACTIVE
        self.collision_node.node().setIntoCollideMask(BitMask32.allOff())
        self.node.reparentTo(player.camera)
        self.node.setPos(-0.65, 1.2, -0.35)
        self.node.setHpr(-12, 0, 8)
        self.node.setScale(0.35)
        self.node.setDepthTest(False)
        self.node.setDepthWrite(False)
        player.held_pickable = self
        print(f"Picked up {self.node.getName()}")

    def drop(self, player):
        self.node.reparentTo(player.node.getParent())
        forward = player.node.getQuat().getForward()
        forward.normalize()
        self.node.setPos(player.node.getPos() + forward * 2.0)
        self.node.setZ(0.75)
        self.node.setHpr(0, 0, 0)
        self.node.setScale(self.default_scale)
        self.node.setDepthTest(True)
        self.node.setDepthWrite(True)
        self.node.setColor(self.default_color)
        self.collision_node.node().setIntoCollideMask(BitMask32.bit(1))
        self.state = InteractableState.IDLE

        if player.held_pickable is self:
            player.held_pickable = None

        print(f"Dropped {self.node.getName()}")


class StaticInteractable(Interactable):
    """Non-pickable: doors, levers, examine-only props."""

    def __init__(self, node, prompt="Examine", interaction_key="X"):
        super().__init__(node, prompt, interaction_key=interaction_key)

    def on_interact(self, player):
        print(f"Examining {self.node.getName()}")


class DoorInteractable(StaticInteractable):
    """A simple open/close door controlled with X."""

    def __init__(self, node):
        super().__init__(node, prompt="Open Door", interaction_key="X")
        self.is_open = False

    def on_interact(self, player):
        self.is_open = not self.is_open
        self.state = (
            InteractableState.ACTIVE
            if self.is_open
            else InteractableState.IDLE
        )
        self.prompt = "Close Door" if self.is_open else "Open Door"
        self.node.setH(70 if self.is_open else 0)
        print("Door opened" if self.is_open else "Door closed")
