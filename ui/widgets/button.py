from direct.gui.DirectGui import DGG, DirectButton
from panda3d.core import TextNode


class Button:
    def __init__(
        self,
        parent,
        text,
        command=None,
        pos=(0, 0, 0),
        scale=0.08,
        frame_color=(0.18, 0.18, 0.18, 1.0),
        hover_color=(0.28, 0.28, 0.28, 1.0),
        press_color=(0.12, 0.12, 0.12, 1.0),
        text_color=(1, 1, 1, 1),
    ):
        self.command = command

        self.widget = DirectButton(
            parent=parent,
            text=text,
            command=self._on_click,
            pos=pos,
            scale=scale,
            frameSize=(-2.5, 2.5, -0.9, 0.9),
            relief=DGG.RAISED,
            frameColor=(
                frame_color,
                hover_color,
                press_color,
                frame_color,
            ),
            text_fg=text_color,
            text_scale=0.7,
            text_align=TextNode.ACenter,
            text_pos=(0, -0.15),
        )

    def _on_click(self):
        if self.command:
            self.command()

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def destroy(self):
        self.widget.destroy()
