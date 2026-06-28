from panda3d.core import WindowProperties
from direct.task import Task


class FirstPersonCamera:

    def __init__(self, game, player):

        self.game = game
        self.player = player

        self.pitch = 0
        self.sensitivity = 0.15

        game.camera.reparentTo(player)
        game.camera.setPos(0, 0, 1.7)

        props = WindowProperties()
        props.setCursorHidden(True)
        game.win.requestProperties(props)

        game.taskMgr.add(self.update, "CameraTask")

    def update(self, task):

        if self.game.mouseWatcherNode.hasMouse():

            win_x = self.game.win.getXSize()
            win_y = self.game.win.getYSize()

            center_x = win_x // 2
            center_y = win_y // 2

            mouse = self.game.mouseWatcherNode

            x = mouse.getMouseX()
            y = mouse.getMouseY()

            dx = x * win_x
            dy = y * win_y

            # rotate player (left/right)
            self.player.setH(
                self.player.getH() - dx * self.sensitivity
            )

            # rotate camera (up/down)
            self.pitch += dy * self.sensitivity
            self.pitch = max(-85, min(85, self.pitch))

            self.game.camera.setP(self.pitch)

            # reset mouse to center
            self.game.win.movePointer(
                0,
                center_x,
                center_y
            )

        return Task.cont