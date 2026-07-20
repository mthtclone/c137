from panda3d.core import (
    BitMask32,
    CollisionHandlerQueue,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
    CollisionTraverser,
)


class InteractionManager:
    """Casts a ray from the camera each frame to find what the player is
    looking at, and dispatches interact calls to the registered Interactable.
    """

    INTERACT_MASK = BitMask32.bit(1)

    def __init__(self, base, camera, max_distance=3.0, ground_z=0.0):
        self.base = base
        self.camera = camera
        self.max_distance = max_distance
        self.ground_z = ground_z
        self.current_target = None
        self.registry = {}  # NodePath -> Interactable

        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        ray_node = CollisionNode("interact_ray")
        ray_node.setFromCollideMask(self.INTERACT_MASK)
        ray_node.setIntoCollideMask(BitMask32.allOff())

        self.ray = CollisionRay()
        ray_node.addSolid(self.ray)

        self.ray_np = camera.attachNewNode(ray_node)
        self.traverser.addCollider(self.ray_np, self.queue)

    def register(self, node, interactable):
        """
        `node` is the visible model (a GeomNode) — it has no CollisionSolid
        of its own, so we attach a CollisionSphere sized to its bounds and
        register that instead. This is what the ray will actually hit.

        IMPORTANT: node.getBounds() returns the bounds already expressed in
        the coordinate space of node's *parent* (i.e. it already bakes in
        node's own position). Since we then attach the CollisionSphere as a
        CHILD of `node`, using that value here double-applies node's
        transform and the sphere ends up nowhere near the visible model.
        We need the bounds in node's own local space instead, which is what
        getTightBounds(node) gives us.
        """
        mn, mx = node.getTightBounds(node)
        center = (mn + mx) / 2.0
        radius = max((mx - mn).length() / 2.0, 0.1)

        col_node = CollisionNode(f"col_{node.getName()}")
        col_node.addSolid(CollisionSphere(center, radius))
        col_node.setIntoCollideMask(self.INTERACT_MASK)
        col_node.setFromCollideMask(BitMask32.allOff())

        col_np = node.attachNewNode(col_node)
        # col_np.show()  # uncomment to visualize the collision sphere while debugging

        self.registry[col_np] = interactable

    def unregister(self, col_np):
        self.registry.pop(col_np, None)
        col_np.removeNode()

    def update(self):
        # ray points straight out from the camera
        self.ray.setOrigin(0, 0, 0)
        self.ray.setDirection(0, 1, 0)

        self.traverser.traverse(self.base.render)
        self.queue.sortEntries()

        new_target = None

        if self.queue.getNumEntries() > 0:
            entry = self.queue.getEntry(0)
            hit_node = entry.getIntoNodePath()
            distance = entry.getSurfacePoint(self.camera).length()

            if distance <= self.max_distance:
                interactable = self.registry.get(hit_node)
                if interactable and interactable.can_interact():
                    new_target = interactable

        if new_target is not self.current_target:
            if self.current_target:
                self.current_target.on_blur()
            if new_target:
                new_target.on_focus()
            self.current_target = new_target

    def try_interact(self, player):
        if self.current_target:
            self.current_target.on_interact(player)

    def update_physics(self, dt):
        """Advances anything currently falling (dropped Pickables). Uses
        duck typing so StaticInteractables (which have no update_physics)
        are simply skipped."""
        for interactable in self.registry.values():
            update_fn = getattr(interactable, "update_physics", None)
            if update_fn:
                update_fn(dt, self.ground_z)

    def get_prompt(self):
        """Returns the prompt text for the current target, or None."""
        if self.current_target:
            return self.current_target.prompt
        return None
