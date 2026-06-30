class BaseMenu:
    def __init__(self, render2d):
        self.render2d = render2d
        self.root = self.render2d.attach_new_node("menu-root")
        self.widgets = []
        self.build()

        self.root.set_bin("fixed", 100)
        self.root.set_depth_write(False)
        self.root.set_depth_test(False)

    def build(self):
        # override in subclasses
        pass

    def show(self):
        self.root.show()

        for w in self.widgets:
            if hasattr(w, "show"):
                w.show()

    def hide(self):
        self.root.hide()

        for w in self.widgets:
            if hasattr(w, "hide"):
                w.hide()

    def destroy(self):
        for w in self.widgets:
            if hasattr(w, "destroy"):
                w.destroy()

        self.widgets.clear()
        self.root.remove_node()
