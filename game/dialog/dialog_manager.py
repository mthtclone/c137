from game.dialog.dialog_data import dialogs


class DialogManager:

    def __init__(self, ui):

        self.ui = ui
        self.current_dialog = None

        self.current_index = 0

        self.is_active = False


    # ------------------------
    # Start Dialog
    # ------------------------

    def start(self, dialog_id):

        if dialog_id not in dialogs:
            return

        self.current_dialog = dialogs[dialog_id]

        self.current_index = 0

        self.is_active = True

        self.show_current()


    # ------------------------
    # Show Current Line
    # ------------------------

    def show_current(self):

        if self.current_dialog is None:
            return

        line = self.current_dialog[self.current_index]

        self.ui.show(

            line["speaker"],

            line["text"]

        )


    # ------------------------
    # Next Line
    # ------------------------

    def next(self):

        if not self.is_active:
            return

        self.current_index += 1

        if self.current_index >= len(self.current_dialog):

            self.close()

        else:

            self.show_current()


    # ------------------------
    # Close Dialog
    # ------------------------

    def close(self):

        self.current_dialog = None

        self.current_index = 0

        self.is_active = False

        self.ui.hide()

            # ------------------------
    # Check Dialog State
    # ------------------------

    def is_playing(self):

        return self.is_active