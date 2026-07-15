from panda3d.core import TextNode
from direct.gui.DirectGui import DirectLabel


class DebugPosition:

    def __init__(self, base, player, enabled=True):

        self.base = base
        self.player = player
        self.enabled = enabled


        if not self.enabled:
            return


        self.text = DirectLabel(

            text="",

            scale=0.045,

            pos=(-1.30, 0, 0.90),

            text_align=TextNode.ALeft,


            # Professional debug style
            text_fg=(1, 1, 1, 1),

            text_shadow=(0, 0, 0, 1),

            frameColor=(0, 0, 0, 0)

        )


        self.base.taskMgr.add(
            self.update,
            "DebugPosition"
        )



    def update(self, task):

        pos = self.player.node.getPos()


        self.text["text"] = (
            "DEBUG MODE\n"
            "\n"
            "PLAYER\n"
            f"X : {pos.x:8.2f}\n"
            f"Y : {pos.y:8.2f}\n"
            f"Z : {pos.z:8.2f}"
        )


        return task.cont