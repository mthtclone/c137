class AudioManager:
    def __init__(self, base):
        self.base = base

        self.sounds = {"grass": self.base.loader.loadSfx("game/assets/on_grass.wav")}

    def play_footstep(self, surface):
        sound = self.sounds.get(surface)

        if sound is None:
            return

        sound.stop()

        sound.play()
