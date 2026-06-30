from ui.menus.base_menu import BaseMenu
from ui.menus.modals.exit_modal import ExitModal
from ui.menus.screens.main_screen import MainScreen
from ui.menus.screens.options_screen import OptionsScreen


class MainMenu(BaseMenu):
    def __init__(
        self,
        render2d,
        on_new_game=None,
        on_continue=None,
        on_exit=None,
    ):
        self.on_new_game = on_new_game
        self.on_continue = on_continue
        self.on_exit = on_exit

        self.current_screen = None
        self.active_modal = None

        self.main_screen = None
        self.options_screen = None

        self.exit_modal = None

        super().__init__(render2d)

    def build(self):
        self.main_screen = MainScreen(
            parent=self.root,
            on_new_game=self.on_new_game,
            on_continue=self.on_continue,
            on_options=self.show_options,
            on_exit=self.show_exit_modal,
        )

        self.options_screen = OptionsScreen(parent=self.root, on_back=self.show_main)

        self.main_screen.hide()
        self.options_screen.hide()

        self.current_screen = self.main_screen
        self.current_screen.show()

    def show_main(self):
        if self.active_modal:
            self.hide_modal()

        self._switch_screen(self.main_screen)

    def show_options(self):
        if self.active_modal:
            self.hide_modal()

        self._switch_screen(self.options_screen)
        print("Show Options Screen")

    def _switch_screen(self, next_screen):
        if self.current_screen:
            self.current_screen.hide()

        self.current_screen = next_screen
        self.current_screen.show()

    def show_exit_modal(self):
        if self.active_modal:
            return

        self.exit_modal = ExitModal(
            parent=self.root,
            on_confirm=self.on_exit,
            on_cancel=self.hide_modal,
        )

        self.active_modal = self.exit_modal
        self.active_modal.show()

    def hide_modal(self):
        if self.active_modal:
            self.active_modal.hide()
            self.active_modal.destroy()

        self.active_modal = None
        self.exit_modal = None
