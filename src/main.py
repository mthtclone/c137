from direct.showbase.ShowBase import ShowBase
from direct.task import Task


class Prototype(ShowBase):
    def __init__(self):
        super().__init__()

        # Load a built-in Panda3D model
        self.model = self.loader.loadModel("models/environment")
        self.model.reparentTo(self.render)
        self.model.setScale(0.1)
        self.model.setPos(-8, 42, 0)

        # Camera position
        self.camera.setPos(0, -20, 5)
        self.camera.lookAt(0, 0, 0)

        # Rotate the world
        self.taskMgr.add(self.spin_world, "spin_world")

    def spin_world(self, task):
        self.model.setH(task.time * 10)
        return Task.cont


app = Prototype()
app.run()
