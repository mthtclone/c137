from ui.widgets.button import Button
from ui.widgets.checkbox import Checkbox
from ui.widgets.label import Label
from ui.widgets.panel import Panel
from ui.widgets.slider import Slider


class OptionsScreen:
    def __init__(self, parent, on_back=None):
        self.parent = parent
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

        self.panel.add_group_title(
            Label(parent=self.panel.content, text="Audio")
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Master Volume"),
            Slider(parent=self.panel.content),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Music Volume"),
            Slider(parent=self.panel.content),
        )

        # -------- Added --------
        self.panel.add_row(
            Label(parent=self.panel.content, text="SFX Volume"),
            Slider(parent=self.panel.content),
        )

        self.panel.add_spacing(0.5)

        # =========================
        # Video
        # =========================

        self.panel.add_group_title(
            Label(parent=self.panel.content, text="Video")
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="Fullscreen"),
            Checkbox(parent=self.panel.content),
        )

        # -------- Added --------
        self.panel.add_row(
            Label(parent=self.panel.content, text="Brightness"),
            Slider(parent=self.panel.content),
        )

        self.panel.add_row(
            Label(parent=self.panel.content, text="UI Scale"),
            Slider(parent=self.panel.content),
        )

        self.panel.add_spacing(0.5)

        # Controls

        self.panel.add_group_title(
            Label(parent=self.panel.content, text="Controls")
        )

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