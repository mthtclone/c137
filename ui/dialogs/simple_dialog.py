from direct.gui.DirectGui import DirectFrame, DirectLabel
from panda3d.core import TextNode


class SimpleDialog:
    def __init__(self):
        #
        # Main dialogue panel
        #

        self.panel = DirectFrame(
            frameColor=(0.08, 0.08, 0.08, 0.82),
            frameSize=(-1.25, 1.25, -0.28, 0.28),
            pos=(0, 0, -0.70),
        )

        #
        # Speaker Name
        #

        self.speaker = DirectLabel(
            parent=self.panel,
            text="",
            pos=(-1.15, 0, 0.18),
            scale=0.055,
            text_align=TextNode.ALeft,
            frameColor=(0, 0, 0, 0),
            text_fg=(1, 1, 1, 1),
        )

        #
        # Dialogue Text
        #

        self.message = DirectLabel(
            parent=self.panel,
            text="",
            pos=(-1.15, 0, 0.03),
            scale=0.05,
            text_align=TextNode.ALeft,
            text_wordwrap=34,
            frameColor=(0, 0, 0, 0),
            text_fg=(0.96, 0.96, 0.96, 1),
        )

        #
        # Continue
        #

        self.continue_text = DirectLabel(
            parent=self.panel,
            text="Continue (Enter)",
            pos=(1.18, 0, -0.22),
            scale=0.03,
            text_align=TextNode.ARight,
            frameColor=(0, 0, 0, 0),
            text_fg=(0.75, 0.75, 0.75, 1),
        )

        self.panel.hide()

    def show(self, speaker, message):
        self.speaker["text"] = speaker

        self.message["text"] = message

        self.panel.show()

    def hide(self):
        self.panel.hide()
