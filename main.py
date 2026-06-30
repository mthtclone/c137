from direct.showbase.ShowBase import ShowBase

# from direct.task import Task
from ui.menus.main_menu import MainMenu

# from direct.gui.DirectGui import DirectButton


class GameApp(ShowBase):
    def __init__(self):
        super().__init__()

        # self.taskMgr.add(self.debug_mouse, "debug_mouse")

        self.disableMouse()  # This is for camera control

        self.menu = MainMenu(
            render2d=self.aspect2d,
            on_new_game=self.on_new_game,
            on_continue=self.on_continue,
            on_exit=self.on_exit,
        )

        self.menu.show()

        # self.test_btn = DirectButton(
        #     text="TEST",
        #     scale=0.1,
        #     pos=(0, 0, 0),
        #     command=lambda: print("DIRECT BUTTON WORKS")
        # )

    def on_new_game(self):
        print("New Game clicked")

    def on_continue(self):
        print("Continue clicked")

    def on_options(self):
        print("Options clicked")

    def on_exit(self):
        print("Exit clicked")

        if self.menu:
            self.menu.destroy()

        self.userExit()

    # def debug_mouse(self, task):
    #     print(self.mouseWatcherNode.hasMouse())
    #     return Task.cont


if __name__ == "__main__":
    app = GameApp()
    app.run()
