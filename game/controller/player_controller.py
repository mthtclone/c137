from game.command.player_commands import (
    CrouchCommand,
    InteractCommand,
    LookCommand,
    MoveCommand,
)


class PlayerController:

    def __init__(self, state):
        self.state = state
        self.walk_speed = 7
        self.sprint_speed = 11

    def build_commands(self):

        commands = []

        x = 0
        y = 0

        # movement input
        if self.state.forward:
            y += 1
        if self.state.backward:
            y -= 1
        if self.state.left:
            x -= 1
        if self.state.right:
            x += 1

        speed = self.walk_speed

        is_forward_only = self.state.forward and not self.state.backward

        if self.state.shift and is_forward_only:
            speed = self.sprint_speed

        if self.state.crouch:
            speed *= 0.4

        if x != 0 or y != 0:
            commands.append(MoveCommand(x, y, speed))

        if self.state.look_x != 0 or self.state.look_y != 0:
            commands.append(LookCommand(self.state.look_x, self.state.look_y))

        if self.state.crouch_pressed:
            self.state.crouch = not self.state.crouch
            self.state.crouch_pressed = False

        commands.append(CrouchCommand(self.state.crouch))

        if self.state.interact:
            commands.append(InteractCommand("E"))
            self.state.interact = False

        if self.state.interact_x:
            commands.append(InteractCommand("X"))
            self.state.interact_x = False

        return commands
