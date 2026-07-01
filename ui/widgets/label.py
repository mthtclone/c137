from direct.gui.DirectGui import DirectLabel
from panda3d.core import TextNode


class Label:
    def __init__(
        self,
        parent,
        text,
        pos=(0, 0, 0),
        scale=0.07,
        text_color=(1, 1, 1, 1),
    ):
        self.widget = DirectLabel(
            parent=parent,
            text=text,
            pos=pos,
            scale=scale,
            text_fg=text_color,
            text_align=TextNode.ACenter,
            relief=None,
            frameColor=(0, 0, 0, 0),
        )

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def destroy(self):
        self.widget.destroy()
