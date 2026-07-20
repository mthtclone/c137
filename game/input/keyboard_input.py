from direct.showbase.DirectObject import DirectObject
from panda3d.core import KeyboardButton, WindowProperties


class KeyboardInput(DirectObject):
    def __init__(self, base, state):
        super().__init__()

        self.base = base
        self.state = state

        # hide cursor
        props = WindowProperties()
        props.setCursorHidden(True)
        base.win.requestProperties(props)

        # actions
        self.accept("c", self.toggle_crouch)
        self.accept("e", self.set_interact)
        self.accept("escape", self.exit_game)

        # mouse center
        self.center_x = base.win.getXSize() // 2
        self.center_y = base.win.getYSize() // 2
        base.win.movePointer(0, self.center_x, self.center_y)

        base.taskMgr.add(self.mouse_task, "MouseTask")

    # ---------------- REAL-TIME KEY CHECK ----------------
    def is_down(self, key):
        return self.base.mouseWatcherNode.is_button_down(KeyboardButton.ascii_key(key))

    def is_shift_down(self):
        return self.base.mouseWatcherNode.is_button_down(KeyboardButton.shift())

    def update_keys(self):
        # movement (ORDER DOES NOT MATTER ANYMORE)
        self.state.forward = self.is_down("w")
        self.state.backward = self.is_down("s")
        self.state.left = self.is_down("a")
        self.state.right = self.is_down("d")

        # shift sprint input
        self.state.shift = self.is_shift_down()

    def set_interact(self):
        self.state.interact = True

    def toggle_crouch(self):
        self.state.crouch_pressed = True

    def exit_game(self):
        self.base.userExit()

    def mouse_task(self, task):
        if self.base.mouseWatcherNode.hasMouse():
            pointer = self.base.win.getPointer(0)

            dx = pointer.getX() - self.center_x
            dy = pointer.getY() - self.center_y

            self.state.look_x = dx
            self.state.look_y = dy

            self.base.win.movePointer(0, self.center_x, self.center_y)

        return task.cont
