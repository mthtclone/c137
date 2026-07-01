"""Input handling for keyboard and mouse controls."""

from typing import Dict


class InputHandler:
    """Track which movement keys are pressed."""

    def __init__(self) -> None:
        # Store the pressed state for each control key.
        self.key_state: Dict[str, bool] = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
        }

    def set_key(self, key_name: str, is_pressed: bool) -> None:
        """Update the state of a key."""
        self.key_state[key_name] = is_pressed

    def is_moving(self) -> bool:
        """Check if any movement key is currently pressed."""
        return any(self.key_state.values())
