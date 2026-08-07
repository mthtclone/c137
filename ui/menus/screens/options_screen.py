from panda3d.core import WindowProperties

from ui.widgets.button import Button
from ui.widgets.checkbox import Checkbox
from ui.widgets.label import Label
from ui.widgets.panel import Panel
from ui.widgets.slider import Slider


class OptionsScreen:
    def __init__(self, parent, game, on_back=None):
        self.parent = parent
        self.game = game
        self.on_back = on_back

        self.widgets = []
        self.visible = False

        self.build()

    def build(self):
        self.panel = Panel(parent=self.parent)
        self.widgets.append(self.panel)

        self.panel.add_title(
            Label(
                parent=self.panel.content,
                text="Options",
                pos=(0, 0, 0),
                scale=0.08,
            )
        )

        # =========================
        # Audio
        # =========================

        self.panel.add_group_title(Label(parent=self.panel.content, text="Audio"))

        self.master_volume_slider = Slider(
            parent=self.panel.content,
            value=self.game.audio.master_volume,
            command=self.set_master_volume,
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Master Volume"),
            self.master_volume_slider,
        )

        self.music_volume_slider = Slider(
            parent=self.panel.content,
            value=self.game.audio.music_volume,
            command=self.set_music_volume,
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Music Volume"),
            self.music_volume_slider,
        )

        self.sfx_volume_slider = Slider(
            parent=self.panel.content,
            value=self.game.audio.sfx_volume,
            command=self.set_sfx_volume,
        )

        # -------- Added --------
        self.panel.add_row(
            Label(parent=self.panel.content, text="SFX Volume"),
            self.sfx_volume_slider,
        )

        self.panel.add_spacing(0.5)

        # =========================
        # Video
        # =========================

        self.panel.add_group_title(Label(parent=self.panel.content, text="Video"))

        self.fullscreen_checkbox = Checkbox(
            parent=self.panel.content,
            checked=self.game.win.getProperties().getFullscreen(),
            command=self.toggle_fullscreen,
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Fullscreen"),
            self.fullscreen_checkbox,
        )

        self.panel.add_spacing(0.5)

        # Controls

        self.panel.add_group_title(Label(parent=self.panel.content, text="Controls"))

        # -------- Added --------

        self.panel.add_row(
            Label(parent=self.panel.content, text="Move Forward"),
            Label(parent=self.panel.content, text="W"),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Move Backward"),
            Label(parent=self.panel.content, text="S"),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Move Left"),
            Label(parent=self.panel.content, text="A"),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Move Right"),
            Label(parent=self.panel.content, text="D"),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Sprint"),
            Label(parent=self.panel.content, text="Shift"),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Interact"),
            Label(parent=self.panel.content, text="E"),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Pause"),
            Label(parent=self.panel.content, text="Esc"),
        )

        self.panel.add_spacing(1.0)

        back_btn = Button(
            parent=self.panel.content,
            text="Back",
            command=self.on_back,
            pos=(0, 0, self.panel.cursor_y),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text=""),
            back_btn,
        )

        self.widgets.append(self.panel)

    def show(self):
        for w in self.widgets:
            w.show()
        self.visible = True

    def hide(self):
        for w in self.widgets:
            w.hide()
        self.visible = False

    def destroy(self):
        for w in self.widgets:
            w.destroy()
        self.widgets.clear()

    def toggle_fullscreen(self, enabled):
        current = self.game.win.getProperties().getFullscreen()

        if current == enabled:
            return

        props = WindowProperties()
        props.setFullscreen(enabled)

        if not enabled:
            props.setSize(1280, 720)

        self.game.win.requestProperties(props)

    def set_master_volume(self, value):
        self.game.audio.set_master_volume(value)

    def set_music_volume(self, value):
        self.game.audio.set_music_volume(value)

    def set_sfx_volume(self, value):
        self.game.audio.set_sfx_volume(value)
