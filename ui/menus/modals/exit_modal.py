from direct.gui.DirectGui import DirectFrame

from ui.menus.modals.base_modal import BaseModal
from ui.widgets.button import Button
from ui.widgets.label import Label


class ExitModal(BaseModal):
    def __init__(self, parent, on_confirm=None, on_cancel=None):
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel

        super().__init__(parent)

    def build(self):
        self.overlay = DirectFrame(
            parent=self.parent,
            frameColor=(0, 0, 0, 0.6),
            frameSize=(-2, 2, -2, 2),
        )

        self.widgets.append(self.overlay)

        title = Label(
            parent=self.parent,
            text="Exit Game?",
            pos=(0, 0, 0.3),
            scale=0.09,
        )
        title.widget["state"] = "disabled"

        self.widgets.append(title)

        yes_btn = Button(
            parent=self.parent,
            text="Yes",
            command=self._confirm,
            pos=(-0.3, 0, -0.1),
        )

        no_btn = Button(
            parent=self.parent,
            text="No",
            command=self._cancel,
            pos=(0.3, 0, -0.1),
        )

        self.widgets.extend([yes_btn, no_btn])

    def _confirm(self):
        if self.on_confirm:
            self.on_confirm()

    def _cancel(self):
        if self.on_cancel:
            self.on_cancel()
