from panda3d.core import (
    BitMask32,
    CollisionHandlerQueue,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
    CollisionTraverser,
)

from game.core.pickable import Pickable


class InteractionManager:
    """Finds interactable objects in the camera's line of sight."""

    INTERACT_MASK = BitMask32.bit(2)

    def __init__(self, base, camera, max_distance=3.0):
        self.base = base
        self.camera = camera
        self.max_distance = max_distance
        self.current_target = None
        self.registry = {}

        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        ray_node = CollisionNode("interact_ray")
        ray_node.setFromCollideMask(self.INTERACT_MASK)
        ray_node.setIntoCollideMask(BitMask32.allOff())

        ray_node.addSolid(CollisionRay(0, 0, 0, 0, 1, 0))
        self.ray_np = camera.attachNewNode(ray_node)
        self.traverser.addCollider(self.ray_np, self.queue)

    def register(self, node, interactable):
        mn, mx = node.getTightBounds(node)
        center = (mn + mx) / 2.0
        radius = max((mx - mn).length() / 2.0, 0.1)

        col_node = CollisionNode(f"col_{node.getName()}")
        col_node.addSolid(CollisionSphere(center, radius))
        col_node.setIntoCollideMask(self.INTERACT_MASK)
        col_node.setFromCollideMask(BitMask32.allOff())

        col_np = node.attachNewNode(col_node)
        self.registry[col_np] = interactable
        return col_np

    def unregister(self, col_np):
        self.registry.pop(col_np, None)
        col_np.removeNode()

    def update(self):
        self.traverser.traverse(self.base.render)
        self.queue.sortEntries()
        target = self._find_target()

        if target is self.current_target:
            return

        if self.current_target:
            self.current_target.on_blur()
        if target:
            target.on_focus()
        self.current_target = target

    def _find_target(self):
        for index in range(self.queue.getNumEntries()):
            entry = self.queue.getEntry(index)

            if entry.getSurfacePoint(self.camera).length() > self.max_distance:
                break

            target = self.registry.get(entry.getIntoNodePath())
            if target and target.can_interact():
                return target

        return None

    def try_interact(self, player):
        if self.current_target and not isinstance(self.current_target, Pickable):
            self.current_target.on_interact(player)

    def get_pickable(self):
        if isinstance(self.current_target, Pickable):
            return self.current_target
        return None

    def get_prompt(self):
        return self.current_target.prompt if self.current_target else None
