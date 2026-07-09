class Command:

    def execute(self, player, dt):
        pass



class MoveCommand(Command):

    def __init__(self, x, y, speed, sprint=False):

        self.x = x
        self.y = y
        self.speed = speed
        self.sprint = sprint


    def execute(self, player, dt):

        player.move(
            self.x,
            self.y,
            self.speed,
            dt,
            self.sprint
        )



class LookCommand(Command):

    def __init__(self, dx, dy):

        self.dx = dx
        self.dy = dy


    def execute(self, player, dt):

        player.look(
            self.dx,
            self.dy
        )



class CrouchCommand(Command):

    def __init__(self, value):

        self.value = value


    def execute(self, player, dt):

        player.crouch(
            self.value
        )



class InteractCommand(Command):

    def execute(self, player, dt):

        player.interact()