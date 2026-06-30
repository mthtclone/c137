class BaseModal:
    def __init__(self, parent):
        self.parent = parent
        self.widgets = []
        self.visible = False

        self.build()

    def build(self):
        # override in subclass
        pass

    def show(self):
        for w in self.widgets:
            if hasattr(w, "show"):
                w.show()
        self.visible = True

    def hide(self):
        for w in self.widgets:
            if hasattr(w, "hide"):
                w.hide()
        self.visible = False

    def destroy(self):
        for w in self.widgets:
            if hasattr(w, "destroy"):
                w.destroy()
        self.widgets.clear()
