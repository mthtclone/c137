"""Camera movement and mouse look for the game engine."""

from panda3d.core import NodePath, Vec3
from .config import CAMERA_MOVE_SPEED, CAMERA_MOUSE_SENSITIVITY
from .input import InputHandler


class CameraController:
    """Control the camera with keyboard movement and mouse look."""

    def __init__(self, camera: NodePath, window, input_handler: InputHandler) -> None:
        self.camera = camera
        self.window = window
        self.input_handler = input_handler

        self.heading = 0.0
        self.pitch = 0.0

    def setup(self) -> None:
        """Prepare the camera and mouse settings."""
        self.camera.setPos(0, -20, 8)
        self.camera.lookAt(0, 0, 0)

        self.window.disableMouse()
        self._center_mouse_pointer()

    def update(self, dt: float) -> None:
        """Update camera position and rotation every frame."""
        self._update_mouse_look()
        self._update_keyboard_movement(dt)

    def _center_mouse_pointer(self) -> None:
        """Center the mouse pointer in the game window."""
        if self.window.win is None:
            return

        props = self.window.win.getProperties()
        center_x = props.getXSize() // 2
        center_y = props.getYSize() // 2
        self.window.win.movePointer(0, center_x, center_y)

    def _update_mouse_look(self) -> None:
        """Rotate the camera based on mouse movement."""
        if not self.window.mouseWatcherNode.hasMouse():
            return

        mouse_x = self.window.mouseWatcherNode.getMouseX()
        mouse_y = self.window.mouseWatcherNode.getMouseY()

        self.heading -= mouse_x * CAMERA_MOUSE_SENSITIVITY
        self.pitch += mouse_y * CAMERA_MOUSE_SENSITIVITY
        self.pitch = max(-80, min(80, self.pitch))

        self.camera.setHpr(self.heading, self.pitch, 0)
        self._center_mouse_pointer()

    def _update_keyboard_movement(self, dt: float) -> None:
        """Move the camera using WASD keys."""
        direction = Vec3(0, 0, 0)

        if self.input_handler.key_state["forward"]:
            direction.y += 1
        if self.input_handler.key_state["backward"]:
            direction.y -= 1
        if self.input_handler.key_state["left"]:
            direction.x -= 1
        if self.input_handler.key_state["right"]:
            direction.x += 1

        if direction.lengthSquared() == 0:
            return

        direction.normalize()
        movement = direction * CAMERA_MOVE_SPEED * dt
        self.camera.setPos(self.camera, movement)
