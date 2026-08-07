class AudioManager:
    def __init__(self, base):
        self.base = base

        self.master_volume = 1.0
        self.music_volume = 1.0
        self.sfx_volume = 1.0

        self.sounds = {"grass": self.base.loader.loadSfx("game/assets/on_grass.wav")}

        self.music = None

    def play_footstep(self, surface):
        sound = self.sounds.get(surface)

        if sound is None:
            return

        sound.stop()

        sound.setVolume(self.master_volume * self.sfx_volume)

        sound.play()

    def set_master_volume(self, value):
        self.master_volume = value

        for sound in self.sounds.values():
            sound.setVolume(self.master_volume * self.sfx_volume)

    def set_sfx_volume(self, value):
        self.sfx_volume = value

        for sound in self.sounds.values():
            sound.setVolume(self.master_volume * self.sfx_volume)

    def set_music_volume(self, value):
        self.music_volume = value

        if self.music:
            self.music.setVolume(self.master_volume * self.music_volume)
