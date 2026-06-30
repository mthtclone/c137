from ui.widgets.button import Button


class MainScreen:
    def __init__(
        self,
        parent,
        on_new_game=None,
        on_continue=None,
        on_options=None,
        on_exit=None,
    ):
        self.parent = parent

        self.on_new_game = on_new_game
        self.on_continue = on_continue
        self.on_options = on_options
        self.on_exit = on_exit

        self.widgets = []
        self.visible = False

        self.build()

    def build(self):
        start_z = 0.4
        spacing = 0.2

        items = [
            ("New Game", self.on_new_game),
            ("Continue", self.on_continue),
            ("Options", self.on_options),
            ("Exit", self.on_exit),
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
