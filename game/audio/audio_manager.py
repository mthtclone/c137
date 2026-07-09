from panda3d.core import AudioSound


class AudioManager:

    def __init__(self, base):

        self.base = base

        self.grass_step = self.base.loader.loadSfx(
            "game/assets/on_grass.wav"
        )

        self.grass_step.setVolume(0.5)

    def play_footstep(self, surface):

        if surface != "grass":
            return

        # Restart sound if it's already playing
        self.grass_step.stop()
        self.grass_step.play()