class Player:
    def __init__(self, node, camera, audio, surface_detector, ground_detector):
        self.node = node
        self.camera = camera

        self.audio = audio
        self.surface_detector = surface_detector
        self.ground_detector = ground_detector

        self.pitch = 0
        self.is_crouching = False

        self.eye_height = 1.0
        self.gravity = 25.0
        self.terminal_velocity = 55.0
        self.vertical_velocity = 0.0
        self.grounded = False
        self.max_slope_normal_z = 0.8
        self.max_step_up = 0.5
        self.ground_snap_distance = 0.35

        # Footstep system
        self.is_moving = False

        self.step_timer = 0
        self.walk_step_delay = 0.5
        self.sprint_step_delay = 0.25

        camera.reparentTo(node)
        camera.setPos(0, 0, self.eye_height)

    # ---------------- MOVEMENT ----------------

    def move(self, x, y, speed, dt, sprint=False):
        forward = self.node.getQuat().getForward()
        right = self.node.getQuat().getRight()

        direction = forward * y + right * x

        self.is_moving = False

        if direction.lengthSquared() > 0:
            direction.normalize()

            self.node.setPos(self.node.getPos() + direction * speed * dt)

            self.is_moving = True

        self.check_footstep(dt, sprint)

    # ---------------- GROUND PHYSICS ----------------

    def update_physics(self, dt):
        """Apply gravity and keep a grounded player aligned to gentle slopes."""
        ground = self.ground_detector.get_ground()

        if ground:
            point, normal, collision_name = ground
            ground_z = point.z
            player_z = self.node.getZ()
            distance_to_ground = player_z - ground_z
            walkable = normal.z >= self.max_slope_normal_z

            if walkable:
                can_step_up = distance_to_ground >= -self.max_step_up
                can_snap_down = distance_to_ground <= self.ground_snap_distance

                if can_step_up and can_snap_down:
                    self.node.setZ(ground_z)
                    self.vertical_velocity = 0.0
                    self.grounded = True
                    return

                next_velocity = max(
                    self.vertical_velocity - self.gravity * dt,
                    -self.terminal_velocity,
                )
                next_z = player_z + next_velocity * dt

                if self.vertical_velocity <= 0 and next_z <= ground_z:
                    self.node.setZ(ground_z)
                    self.vertical_velocity = 0.0
                    self.grounded = True
                    return

        self.vertical_velocity = max(
            self.vertical_velocity - self.gravity * dt,
            -self.terminal_velocity,
        )
        self.node.setZ(self.node.getZ() + self.vertical_velocity * dt)
        self.grounded = False

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

        self.node.setH(self.node.getH() - dx * sensitivity)

        self.pitch -= dy * sensitivity

        self.pitch = max(-85, min(85, self.pitch))

        self.camera.setP(self.pitch)

    # ---------------- CROUCH ----------------

    def crouch(self, value):
        self.is_crouching = value

        target_z = 0.65 if value else self.eye_height

        current_z = self.camera.getZ()

        self.camera.setZ(current_z + (target_z - current_z) * 0.25)

    # ---------------- INTERACT ----------------

    def interact(self):
        print("Interact Triggered")
