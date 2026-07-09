class Player:

    def __init__(self, node, camera, audio, surface_detector):

        self.node = node
        self.camera = camera

        self.audio = audio
        self.surface_detector = surface_detector

        self.pitch = 0
        self.is_crouching = False


        # Footstep system
        self.is_moving = False

        self.step_timer = 0
        self.walk_step_delay = 0.5
        self.sprint_step_delay = 0.25


        camera.reparentTo(node)
        camera.setPos(0, 0, 1.7)



    # ---------------- MOVEMENT ----------------

    def move(self, x, y, speed, dt, sprint=False):

        forward = self.node.getQuat().getForward()
        right = self.node.getQuat().getRight()

        direction = forward * y + right * x


        self.is_moving = False


        if direction.lengthSquared() > 0:

            direction.normalize()

            self.node.setPos(
                self.node.getPos() + direction * speed * dt
            )

            self.is_moving = True


        self.check_footstep(
            dt,
            sprint
        )



    # ---------------- FOOTSTEP ----------------

    def check_footstep(self, dt, sprint):

        if not self.is_moving:

            self.step_timer = 0

            return


        if sprint:

            delay = self.sprint_step_delay

        else:

            delay = self.walk_step_delay



        self.step_timer += dt


        if self.step_timer >= delay:

            surface = self.surface_detector.get_surface(self)

            self.audio.play_footstep(surface)

            self.step_timer = 0



    # ---------------- LOOK ----------------

    def look(self, dx, dy):

        sensitivity = 0.08

        self.node.setH(
            self.node.getH() - dx * sensitivity
        )


        self.pitch -= dy * sensitivity

        self.pitch = max(
            -85,
            min(
                85,
                self.pitch
            )
        )


        self.camera.setP(self.pitch)



    # ---------------- CROUCH ----------------

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