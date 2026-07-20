class SurfaceDetector:
    def __init__(self, metadata):
        self.metadata = metadata

    def get_surface(self, player):
        collision_name = player.ground_detector.last_surface

        print("[Surface Resolved]", collision_name)

        if collision_name is None:
            return "default"

        #
        # Remove Collision- prefix
        #

        collision_name = collision_name.replace("Collision-", "")

        return self.metadata.get_collision_surface(collision_name) or "default"
