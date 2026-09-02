from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectWaitBar,
)
from panda3d.core import TextNode


class LoadingScreen:
    def __init__(self, parent, game):
        self.parent = parent
        self.game = game

        self.visible = False
        self.progress = 0

        # ==================================================
        # BACKGROUND
        # ==================================================

        self.background = DirectFrame(
            parent=self.parent,
            frameSize=(
                -2,
                2,
                -1.2,
                1.2,
            ),
            frameColor=(
                0.12,
                0.12,
                0.12,
                1,
            ),
            relief=0,
        )

        # ==================================================
        # LOADING TEXT
        # ==================================================

        self.loading_text = DirectLabel(
            parent=self.background,
            text="LOADING",
            pos=(
                0,
                0,
                0.35,
            ),
            scale=0.07,
            text_fg=(
                0.9,
                0.9,
                0.9,
                1,
            ),
            text_align=TextNode.ACenter,
            relief=None,
        )

        # ==================================================
        # PROGRESS BAR
        # ==================================================

        self.progress_bar = DirectWaitBar(
            parent=self.background,
            pos=(
                0,
                0,
                0.05,
            ),
            scale=0.8,
            value=0,
            range=100,
            frameSize=(
                -1,
                1,
                -0.06,
                0.06,
            ),
            frameColor=(
                0.08,
                0.08,
                0.08,
                1,
            ),
            barColor=(
                0.75,
                0.75,
                0.75,
                1,
            ),
            relief=0,
        )

        # ==================================================
        # PERCENTAGE
        # ==================================================

        self.percent_text = DirectLabel(
            parent=self.background,
            text="0%",
            pos=(
                0,
                0,
                -0.12,
            ),
            scale=0.045,
            text_fg=(
                0.65,
                0.65,
                0.65,
                1,
            ),
            text_align=TextNode.ACenter,
            relief=None,
        )

        # ==================================================
        # STATUS TEXT
        # ==================================================

        self.status_text = DirectLabel(
            parent=self.background,
            text="Preparing...",
            pos=(
                0,
                0,
                -0.38,
            ),
            scale=0.038,
            text_fg=(
                0.55,
                0.55,
                0.55,
                1,
            ),
            text_align=TextNode.ACenter,
            relief=None,
        )

        self.hide()

    # ======================================================
    # PROGRESS
    # ======================================================

    def set_progress(self, value, status=None):
        self.progress = max(
            0,
            min(100, value),
        )

        self.progress_bar["value"] = self.progress

        self.percent_text["text"] = f"{int(self.progress)}%"

        if status is not None:
            self.status_text["text"] = status

        # Force GUI update
        self.game.graphicsEngine.renderFrame()

    # ======================================================
    # SHOW
    # ======================================================

    def show(self):
        self.visible = True

        self.set_progress(
            0,
            "Preparing...",
        )

        self.background.show()

        # Make sure it appears immediately
        self.game.graphicsEngine.renderFrame()

        print("[LoadingScreen] SHOW")

    # ======================================================
    # HIDE
    # ======================================================

    def hide(self):
        self.visible = False

        self.background.hide()

        print("[LoadingScreen] HIDE")

    # ======================================================
    # DESTROY
    # ======================================================

    def destroy(self):
        self.background.destroy()
