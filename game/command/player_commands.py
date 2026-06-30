class Command:
    def execute(self, player, dt):
        pass


class MoveCommand(Command):

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def execute(self, player, dt):
        player.move(self.x, self.y, self.speed, dt)


class LookCommand(Command):

    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy

    def execute(self, player, dt):
        player.look(self.dx, self.dy)


class CrouchCommand(Command):

    def __init__(self, value):
        self.value = value

    def execute(self, player, dt):
        player.crouch(self.value)


class InteractCommand(Command):

    def execute(self, player, dt):
        player.interact()