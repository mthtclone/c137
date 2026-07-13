class TestScene:
    def __init__(self, base):
        self.base = base

        self.nodes = []

    def build(self):
        self.create_ground()

        self.create_door()

        self.create_tree()

    def create_ground(self):
        ground = self.base.loader.loadModel("models/box")

        ground.setScale(10, 10, 0.1)

        ground.setPos(0, 0, -1)

        ground.setTag("surface", "grass")

        ground.reparentTo(self.base.render)

        self.nodes.append(ground)

    def create_door(self):
        door = self.base.loader.loadModel("models/box")

        door.setScale(1, 0.2, 2)

        door.setPos(0, 5, 1)

        door.setTag("metadata", "old_door_01")

        door.reparentTo(self.base.render)

        self.nodes.append(door)

    def create_tree(self):
        tree = self.base.loader.loadModel("models/box")

        tree.setScale(0.5, 0.5, 3)

        tree.setPos(-4, 3, 2)

        tree.setTag("metadata", "tree_01")

        tree.reparentTo(self.base.render)

        self.nodes.append(tree)
