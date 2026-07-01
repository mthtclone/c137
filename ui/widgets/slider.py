from direct.gui.DirectGui import DirectSlider


class Slider:
    def __init__(
        self,
        parent,
        pos=(0, 0, 0),
        value=50,
        min_value=0,
        max_value=100,
        command=None,
        scale=0.35,
    ):
        self.command = command

        self.widget = DirectSlider(
            parent=parent,
            pos=pos,
            scale=scale,
            value=value,
            range=(min_value, max_value),
            command=self._on_change,
        )

    def _on_change(self):
        if self.command:
            self.command(self.value)

    @property
    def value(self):
        return self.widget["value"]

    @value.setter
    def value(self, value):
        self.widget["value"] = value

    def show(self):
        self.widget.show()

    def hide(self):
        self.widget.hide()

    def destroy(self):
        self.widget.destroy()
