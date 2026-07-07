from panda3d.core import Vec3


class Player:

    def __init__(self, node, camera, interaction_manager=None):

        self.node = node
        self.camera = camera
        self.interaction_manager = interaction_manager
        self.held_pickable = None

        self.pitch = 0
        self.is_crouching = False

        camera.reparentTo(node)
        camera.setPos(0, 0, 1.7)

    def move(self, x, y, speed, dt):

        forward = self.node.getQuat().getForward()
        right = self.node.getQuat().getRight()

        direction = forward * y + right * x

        if direction.lengthSquared() > 0:
            direction.normalize()

        self.node.setPos(self.node.getPos() + direction * speed * dt)

    def look(self, dx, dy):

        sensitivity = 0.08

        self.node.setH(self.node.getH() - dx * sensitivity)

        self.pitch -= dy * sensitivity
        self.pitch = max(-85, min(85, self.pitch))

        self.camera.setP(self.pitch)

    # ---------------- CROUCH ----------------
    def crouch(self, value):

        self.is_crouching = value

        target_z = 1.0 if value else 1.7
        current_z = self.camera.getZ()

        self.camera.setZ(current_z + (target_z - current_z) * 0.25)

    # ---------------- INTERACT ----------------
    def interact(self, interaction_key="E"):
        if self.interaction_manager:
            self.interaction_manager.try_interact(self, interaction_key)
