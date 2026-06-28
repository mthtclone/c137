from direct.showbase.DirectObject import DirectObject
from direct.task import Task


class PlayerMovement(DirectObject):

    def __init__(self, game, player):

        self.game = game
        self.player = player

        self.speed = 8
        self.sprint_speed = 15

        self.velocity_z = 0
        self.gravity = -25
        self.jump_strength = 10
        self.on_ground = True

        self.keys = {
            "w": False,
            "a": False,
            "s": False,
            "d": False,
            "shift": False
        }

        for key in ["w", "a", "s", "d", "shift"]:
            self.accept(key, self.setKey, [key, True])
            self.accept(key + "-up", self.setKey, [key, False])

        self.accept("space", self.jump)
        self.accept("c", self.toggle_crouch)

        game.taskMgr.add(self.update, "Movement")

    def setKey(self, key, value):
        self.keys[key] = value

    def jump(self):
        if self.on_ground:
            self.velocity_z = self.jump_strength
            self.on_ground = False

    def toggle_crouch(self):
        if self.game.camera.getZ() > 1.0:
            self.game.camera.setZ(1.0)
        else:
            self.game.camera.setZ(1.7)

    def update(self, task):

        dt = globalClock.getDt()

        speed = self.sprint_speed if self.keys["shift"] else self.speed

        if self.keys["w"]:
            self.player.setY(self.player, speed * dt)

        if self.keys["s"]:
            self.player.setY(self.player, -speed * dt)

        if self.keys["a"]:
            self.player.setX(self.player, -speed * dt)

        if self.keys["d"]:
            self.player.setX(self.player, speed * dt)

        self.velocity_z += self.gravity * dt
        self.player.setZ(self.player.getZ() + self.velocity_z * dt)

        if self.player.getZ() <= 0:
            self.player.setZ(0)
            self.velocity_z = 0
            self.on_ground = True

        return Task.cont