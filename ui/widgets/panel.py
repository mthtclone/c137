from direct.gui.DirectGui import DirectFrame


class Panel:
    def __init__(
        self,
        parent,
        scroll_speed=0.05,
    ):
        self.overlay = DirectFrame(
            parent=parent,
            frameSize=(-2, 2, -2, 2),
            frameColor=(0, 0, 0, 0.65),
            relief=0,
        )

        self.content = DirectFrame(
            parent=self.overlay,
            frameSize=(0, 0, 0, 0),
            frameColor=(0, 0, 0, 0),
            relief=0,
        )

        self.cursor_y = 0.6
        self.padding_left = -0.7
        self.line_height = 0.18

        self.scroll_speed = scroll_speed
        self.scroll_y = 0.0
        self.min_y = -0.0
        self.max_y = 0.5

        self._setup_scroll_input()

    def _setup_scroll_input(self):
        # taskMgr = None

        from direct.showbase import DirectObject

        self.accept = DirectObject.DirectObject().accept

        self.accept("wheel_up", self._scroll_up)
        self.accept("wheel_down", self._scroll_down)

    def _scroll_up(self):
        self.scroll_y += self.scroll_speed
        self._apply_scroll()

    def _scroll_down(self):
        self.scroll_y -= self.scroll_speed
        self._apply_scroll()

    def _apply_scroll(self):
        # clamp
        self.scroll_y = max(self.min_y, min(self.max_y, self.scroll_y))

        self.content.setZ(self.scroll_y)

    def add_title(self, label):
        label.widget.reparentTo(self.content)
        label.widget.setPos(0, 0, self.cursor_y)

        self.cursor_y -= self.line_height * 1.5
        return label

    def add_group_title(self, label):
        label.widget.reparentTo(self.content)
        label.widget.setPos(self.padding_left, 0, self.cursor_y)

        self.cursor_y -= self.line_height * 1.2
        return label

    def add_row(self, label_widget, control_widget):
        label_widget.widget.reparentTo(self.content)
        label_widget.widget.setPos(self.padding_left, 0, self.cursor_y)

        control_widget.widget.reparentTo(self.content)
        control_widget.widget.setPos(0.35, 0, self.cursor_y)

        self.cursor_y -= self.line_height

        return (label_widget, control_widget)

    def add_spacing(self, factor=1.0):
        self.cursor_y -= self.line_height * factor

    def show(self):
        self.overlay.show()

    def hide(self):
        self.overlay.hide()

    def destroy(self):
        self.overlay.destroy()
