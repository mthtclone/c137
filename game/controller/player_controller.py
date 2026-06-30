from game.command.player_commands import (
    MoveCommand,
    LookCommand,
    CrouchCommand,
    InteractCommand
)


class PlayerController:

    def __init__(self, state):

        self.state = state
        self.walk_speed = 8
        self.sprint_speed = 15

    def build_commands(self):

        commands = []

        x = 0
        y = 0

        if self.state.forward:
            y += 1
        if self.state.backward:
            y -= 1
        if self.state.left:
            x -= 1
        if self.state.right:
            x += 1

        if x != 0 or y != 0:

            speed = self.walk_speed

            if self.state.crouch:
                speed *= 0.4

            elif self.state.sprint:
                speed = self.sprint_speed

            commands.append(MoveCommand(x, y, speed))

        # ---------------- LOOK ----------------
        if self.state.look_x != 0 or self.state.look_y != 0:
            commands.append(LookCommand(self.state.look_x, self.state.look_y))

        # ---------------- CROUCH TOGGLE ----------------
        if self.state.crouch_pressed:
            self.state.crouch = not self.state.crouch
            self.state.crouch_pressed = False

        commands.append(CrouchCommand(self.state.crouch))

        # ---------------- INTERACT ----------------
        if self.state.interact:
            commands.append(InteractCommand())
            self.state.interact = False

        return commands