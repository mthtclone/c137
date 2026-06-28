from panda3d.core import (
    AmbientLight,
    CollisionNode,
    CollisionBox,
    Point3
)


class TestWorld:

    def __init__(self):

        # LIGHT
        ambient = AmbientLight("ambient")
        ambient.setColor((1, 1, 1, 1))
        ambient_np = render.attachNewNode(ambient)
        render.setLight(ambient_np)

        # GROUND (no collision yet)
        ground = loader.loadModel("models/box")
        ground.reparentTo(render)
        ground.setScale(50, 50, 0.1)
        ground.setPos(0, 20, -1)

        # BLOCKS
        self.blocks = []

        positions = [
            (5, 20, 0),
            (-5, 15, 0),
            (0, 30, 0),
            (10, 40, 2),
            (-10, 35, 0),
        ]

        for pos in positions:

            # -------------------------
            # VISUAL BLOCK
            # -------------------------
            block = loader.loadModel("models/box")
            block.reparentTo(render)
            block.setScale(2)
            block.setPos(*pos)

            # -------------------------
            # COLLISION BLOCK (SOLID)
            # -------------------------
            cnode = CollisionNode("block")

            # half-size = 1 because scale = 2
            cnode.addSolid(CollisionBox(Point3(0, 0, 0), 1, 1, 1))

            cnode_path = block.attachNewNode(cnode)

            # OPTIONAL: show collision box for debugging
            # cnode_path.show()

            self.blocks.append(block)