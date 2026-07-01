from direct.gui.DirectGui import DirectCheckButton


class Checkbox:
    def __init__(
        self,
        parent,
        pos=(0, 0, 0),
        checked=False,
        command=None,
        scale=0.06,
    ):
        self.command = command

        self.widget = DirectCheckButton(
            parent=parent,
            pos=pos,
            scale=scale,
            indicatorValue=checked,
            command=self._on_toggle,
        )

    def _on_toggle(self, value):
        if self.command:
            self.command(value)

    @property
    def checked(self):
        return self.widget["indicatorValue"]

    @checked.setter
    def checked(self, value):
        self.widget["indicatorValue"] = value

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def destroy(self):
        self.widget.destroy()
