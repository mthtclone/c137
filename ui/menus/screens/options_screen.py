from ui.widgets.button import Button


class OptionsScreen:
    def __init__(
        self,
        parent,
        on_back=None,
    ):
        self.parent = parent
        self.on_back = on_back

        self.widgets = []
        self.visible = False

        self.build()

    def build(self):
        start_z = 0.4
        spacing = 0.2

        items = [
            ("Graphics", None),
            ("Audio", None),
            ("Controls", None),
            ("Back", self.on_back),
        ]

        for i, (text, callback) in enumerate(items):
            btn = Button(
                parent=self.parent,
                text=text,
                command=callback,
                pos=(0, 0, start_z - i * spacing),
            )

            self.widgets.append(btn)

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
