from panda3d.core import (
    BitMask32,
    CollisionHandlerQueue,
    CollisionNode,
    CollisionRay,
    CollisionTraverser,
)


class GroundDetector:
    """
    Finds the closest collision surface directly below the player.

    Returns:
        (
            hit_point,
            hit_normal,
            collision_object_name
        )

    The collision object name is later resolved through
    the metadata system to determine surfaces such as
    grass, wood, stone, etc.
    """

    def __init__(self, base, player_node, mask=None, max_distance=4.0):
        self.base = base

        self.max_distance = max_distance

        self.last_surface = None

        if mask is None:
            mask = BitMask32.bit(1)

        #
        # Collision setup
        #

        self.traverser = CollisionTraverser("groundTraverser")

        self.queue = CollisionHandlerQueue()

        #
        # Downward ray
        #

        ray_node = CollisionNode("GroundRay")

        ray_node.setFromCollideMask(mask)

        ray_node.setIntoCollideMask(BitMask32.allOff())

        ray_node.addSolid(CollisionRay(0, 0, 2.0, 0, 0, -1))

        self.ray_node = player_node.attachNewNode(ray_node)

        self.traverser.addCollider(self.ray_node, self.queue)

        #
        # Debug
        #

        self.debug = False

    def get_ground(self):
        """
        Return the closest valid ground collision.

        Returns:

            (
                Point3,
                Vec3,
                str
            )

        or None
        """

        self.queue.clearEntries()

        self.traverser.traverse(self.base.render)

        self.queue.sortEntries()

        for index in range(self.queue.getNumEntries()):
            entry = self.queue.getEntry(index)

            point = entry.getSurfacePoint(self.base.render)

            distance = self.ray_node.getPos(self.base.render).z - point.z

            if 0 <= distance <= self.max_distance:
                #
                # Find the collision object
                #

                into_node = entry.getIntoNodePath()

                self.last_surface = self.find_collision_name(into_node)

                return (
                    point,
                    entry.getSurfaceNormal(self.base.render),
                    self.last_surface,
                )

        return None

    def find_collision_name(self, node):
        """
        Find the original collision object name.

        Collision nodes are generated under:

        COL_Object
            |
            GeomNode
                |
                CollisionNode

        so we walk upward until we find
        the COL_ node.
        """

        current = node

        while not current.isEmpty():
            name = current.getName()

            if name.startswith("COL_"):
                return name

            current = current.getParent()

        #
        # Fallback:
        #

        return node.getName()
