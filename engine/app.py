"""Main application setup for the Panda3D engine."""

from direct.showbase.ShowBase import ShowBase
from panda3d.core import WindowProperties

from .camera import CameraController
from .config import BACKGROUND_COLOR, WINDOW_HEIGHT, WINDOW_TITLE, WINDOW_WIDTH
from .input import InputHandler
from .lighting import LightingManager
from .terrain import TerrainLoader


class GameApp(ShowBase):
    """Main game application class that launches the Panda3D window."""

    def __init__(self) -> None:
        super().__init__()

        self.input_handler = InputHandler()
        self.camera_controller = CameraController(self.camera, self, self.input_handler)
        self.lighting_manager = LightingManager(self.render)
        self.terrain_loader = TerrainLoader(self.render)

        self._setup_window()
        self._setup_scene()
        self._setup_controls()
        self.taskMgr.add(self._update_task, "update_task")

    def _setup_window(self) -> None:
        """Set up the game window and background color."""
        self.win.setClearColor(BACKGROUND_COLOR)

        window_properties = WindowProperties()
        window_properties.setSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        window_properties.setTitle(WINDOW_TITLE)
        self.win.requestProperties(window_properties)

        self.camera_controller.setup()

    def _setup_scene(self) -> None:
        """Load lighting and terrain for the scene."""
        self.lighting_manager.setup()
        self.terrain_loader.load()

    def _setup_controls(self) -> None:
        """Bind keys for camera movement."""
        self.accept("w", self.input_handler.set_key, ["forward", True])
        self.accept("w-up", self.input_handler.set_key, ["forward", False])
        self.accept("s", self.input_handler.set_key, ["backward", True])
        self.accept("s-up", self.input_handler.set_key, ["backward", False])
        self.accept("a", self.input_handler.set_key, ["left", True])
        self.accept("a-up", self.input_handler.set_key, ["left", False])
        self.accept("d", self.input_handler.set_key, ["right", True])
        self.accept("d-up", self.input_handler.set_key, ["right", False])
        self.accept("escape", self.userExit)

    def _update_task(self, task) -> None:
        """Update the camera every frame."""
        dt = globalClock.getDt()
        self.camera_controller.update(dt)
        return task.cont
