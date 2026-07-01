class InputState:

    def __init__(self):

        self.forward = False
        self.backward = False
        self.left = False
        self.right = False

        self.shift = False

        self.crouch = False
        self.crouch_pressed = False

        self.interact = False

        self.look_x = 0.0
        self.look_y = 0.0

    def reset(self):
        self.look_x = 0.0
        self.look_y = 0.0