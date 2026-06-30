from direct.showbase.DirectObject import DirectObject
from panda3d.core import WindowProperties


class KeyboardInput(DirectObject):

    def __init__(self, base, state):

        super().__init__()

        self.base = base
        self.state = state

        # HIDE CURSOR
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        # MOVEMENT KEYS
        self.accept("w", self.set, ["forward", True])
        self.accept("w-up", self.set, ["forward", False])

        self.accept("s", self.set, ["backward", True])
        self.accept("s-up", self.set, ["backward", False])

        self.accept("a", self.set, ["left", True])
        self.accept("a-up", self.set, ["left", False])

        self.accept("d", self.set, ["right", True])
        self.accept("d-up", self.set, ["right", False])

        self.accept("shift", self.set, ["sprint", True])
        self.accept("shift-up", self.set, ["sprint", False])

        # CROUCH TOGGLE
        self.accept("c", self.toggle_crouch)

        # INTERACT
        self.accept("e", self.set, ["interact", True])

        # ESCAPE EXIT GAME (FIXED)
        self.accept("escape", self.exit_game)

        # MOUSE CENTER
        self.center_x = base.win.getXSize() // 2
        self.center_y = base.win.getYSize() // 2

        base.win.movePointer(0, self.center_x, self.center_y)

        base.taskMgr.add(self.mouse_task, "MouseTask")

    def set(self, key, value):
        setattr(self.state, key, value)

    def toggle_crouch(self):
        self.state.crouch_pressed = True

    def exit_game(self):
        self.base.userExit()

    def mouse_task(self, task):

        if not self.base.mouseWatcherNode.hasMouse():
            return task.cont

        pointer = self.base.win.getPointer(0)

        dx = pointer.getX() - self.center_x
        dy = pointer.getY() - self.center_y

        self.state.look_x = dx
        self.state.look_y = dy

        self.base.win.movePointer(0, self.center_x, self.center_y)

        return task.cont