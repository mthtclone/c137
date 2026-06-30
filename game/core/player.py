from panda3d.core import Vec3


class Player:

    def __init__(self, node, camera):

        self.node = node
        self.camera = camera

        self.pitch = 0
        self.is_crouching = False

        camera.reparentTo(node)
        camera.setPos(0, 0, 1.7)

    # ---------------- MOVE ----------------
    def move(self, x, y, speed, dt):

        direction = Vec3(x, y, 0)

        if direction.length() > 0:
            direction.normalize()

        direction = self.node.getQuat().xform(direction)

        self.node.setPos(self.node.getPos() + direction * speed * dt)

    # ---------------- LOOK ----------------
    def look(self, dx, dy):

        sensitivity = 0.05

        self.node.setH(self.node.getH() - dx * sensitivity)

        self.pitch -= dy * sensitivity
        self.pitch = max(-85, min(85, self.pitch))

        self.camera.setP(self.pitch)

    # ---------------- CROUCH (SMOOTH TOGGLE STATE) ----------------
    def crouch(self, value):

        self.is_crouching = value

        target_z = 1.0 if value else 1.7

        current_z = self.camera.getZ()

        self.camera.setZ(
            current_z + (target_z - current_z) * 0.25
        )

    # ---------------- INTERACT ----------------
    def interact(self):
        print("Interact Triggered")