import simplepbr

from direct.showbase.ShowBase import ShowBase
from direct.showbase.ShowBaseGlobal import globalClock

from panda3d.core import (
    AmbientLight,
    BitMask32,
    CollisionBox,
    CollisionHandlerPusher,
    CollisionNode,
    CollisionTraverser,
    DirectionalLight,
    Fog,
    Vec3,
)

from engine.managers.level_manager import LevelManager

from game.audio.audio_manager import AudioManager
from game.collision.ground_detector import GroundDetector
from game.collision.surface_detector import SurfaceDetector
from game.controller.player_controller import PlayerController
from game.core.player import Player
from game.dialog.dialog_manager import DialogManager
from game.input.input_state import InputState
from game.input.keyboard_input import KeyboardInput
from game.zones.dialog_trigger import DialogTrigger

from ui.dialogs.simple_dialog import SimpleDialog
from ui.loading_screen import LoadingScreen
from ui.menus.main_menu import MainMenu


class GameApp(ShowBase):

    def __init__(self):
        super().__init__()

        #
        # PBR renderer
        #

        simplepbr.init(enable_fog=True)

        #
        # Camera
        #

        self.disableMouse()

        #
        # State
        #

        self.menu = None
        self.level_manager = None
        self.loading_screen = None

        #
        # Audio
        #

        self.audio = AudioManager(self)

        #
        # UI
        #

        self.setup_menu()

        self.loading_screen = LoadingScreen(
            self.aspect2d,
            self,
        )

    #
    # MENU
    #

    def setup_menu(self):

        self.menu = MainMenu(
            self.aspect2d,
            self,
            on_new_game=self.on_new_game,
            on_continue=self.on_continue,
            on_exit=self.on_exit,
        )

        self.menu.show()

    #
    # NEW GAME
    #

    def on_new_game(self):

        print("[MAIN] New game selected.")

        #
        # Remove menu
        #

        if self.menu:
            self.menu.destroy()
            self.menu = None

        #
        # Show loading screen
        #

        self.loading_screen.show()

        #
        # Render loading screen first
        #

        self.graphicsEngine.renderFrame()

        #
        # Start loading on next task
        #

        self.taskMgr.doMethodLater(
            0.1,
            self._start_new_game_loading,
            "startNewGameLoading",
        )

    def _start_new_game_loading(self, task):

        print("[MAIN] Starting game load...")

        self.start_game()

        print("[MAIN] Finished game load.")

        return task.done

    #
    # CONTINUE
    #

    def on_continue(self):

        print("[MAIN] Continue selected.")

        # TODO:
        # Load save data here

        if self.menu:
            self.menu.destroy()
            self.menu = None

        #
        # Show loading screen
        #

        self.loading_screen.show()

        #
        # Render loading screen first
        #

        self.graphicsEngine.renderFrame()

        #
        # Start loading on next task
        #

        self.taskMgr.doMethodLater(
            0.1,
            self._start_continue_loading,
            "startContinueLoading",
        )

    def _start_continue_loading(self, task):

        self.start_game()

        return task.done

    #
    # EXIT
    #

    def on_exit(self):

        print("[MAIN] Exit selected.")

        if self.menu:
            self.menu.destroy()
            self.menu = None

        self.userExit()

    #
    # GAME START
    #

    def start_game(self):

        #
        # 0% - PREPARING
        #

        self.loading_screen.set_progress(
            0,
            "Preparing game...",
        )

        #
        # 10% - LIGHTING
        #

        self.setup_lighting()

        self.loading_screen.set_progress(
            10,
            "Setting up environment...",
        )

        #
        # 15% - FOG
        #

        self.setup_fog()

        self.loading_screen.set_progress(
            15,
            "Preparing atmosphere...",
        )

        #
        # 20% - LEVEL MANAGER
        #

        self.level_manager = LevelManager(self)

        self.loading_screen.set_progress(
            20,
            "Preparing level...",
        )

        #
        # 30% - LOAD LEVEL
        #

        self.loading_screen.set_progress(
            30,
            "Loading environment...",
        )

        success = self.level_manager.load_level(
            "levels/test_level"
        )

        #
        # CHECK LEVEL
        #

        if not success:

            print("[MAIN] Failed to load level.")

            self.loading_screen.set_progress(
                100,
                "Failed to load level.",
            )

            return

        #
        # 55% - ENVIRONMENT OBJECTS
        #

        self.loading_screen.set_progress(
            55,
            "Loading environment objects...",
        )

        #
        # 65% - PLAYER
        #

        spawn = self.level_manager.get_spawn_point()

        self.loading_screen.set_progress(
            65,
            "Creating player...",
        )

        self.setup_player(spawn)

        #
        # 75% - COLLISION
        #

        self.loading_screen.set_progress(
            75,
            "Setting up collision...",
        )

        self.setup_player_collision()

        #
        # 85% - CONTROLS
        #

        self.loading_screen.set_progress(
            85,
            "Setting up controls...",
        )

        self.setup_player_controls()

        self.loading_screen.set_progress(
    95,
    "Finalizing...",
)

        self.debug_model()

#
# 100% - COMPLETE
#

        self.loading_screen.set_progress(
    100,
    "Ready",
)

        print()
        print("[MAIN] Level loaded successfully.")

#
# Keep the loading screen visible.
# Schedule gameplay to appear AFTER 100% has been rendered.
#

        self.taskMgr.doMethodLater(
    0.5,
        self._show_gameplay,
    "showGameplay",
)

    def _show_gameplay(self, task):

        print("[MAIN] 100% reached.")
        print("[MAIN] Starting gameplay.")

        if self.loading_screen:
            self.loading_screen.hide()

        return task.done

    #
    # PLAYER SETUP
    #

    def setup_player(self, spawn):

        player_node = self.render.attachNewNode(
            "Player"
        )

        if spawn is not None:

            spawn_position = spawn.getPos(
                self.render
            )

            player_node.setPos(
                spawn_position
                + self.level_manager.get_spawn_offset()
            )

            player_node.setH(
                spawn.getH(self.render)
            )

        else:

            player_node.setPos(
                0,
                -20,
                5,
            )

        self.player = Player(
            player_node,
            self.camera,
            self.audio,
            SurfaceDetector(
                self.level_manager.metadata
            ),
            GroundDetector(
                self,
                player_node,
            ),
        )

        print("[MAIN] Camera height set.")

    #
    # INPUT + DIALOG
    #

    def setup_player_controls(self):

        dialog_settings = (
            self.level_manager.metadata.get_dialog()
        )

        self.dialog_enabled = dialog_settings.get(
            "enabled",
            True,
        )

        #
        # Input
        #

        self.input_state = InputState()

        self.keyboard_input = KeyboardInput(
            self,
            self.input_state,
        )

        #
        # Dialog
        #

        self.dialog_ui = SimpleDialog()

        self.dialog_manager = DialogManager(
            self.dialog_ui
        )

        self.accept(
            "enter",
            self.dialog_manager.next,
        )

        if self.dialog_enabled:

            self.dialog_trigger = DialogTrigger(
                self.player,
                self.dialog_manager,
                self.level_manager.metadata,
            )

            print("[MAIN] Dialog enabled.")

        else:

            self.dialog_trigger = None

            print("[MAIN] Dialog disabled.")

        #
        # Controller
        #

        self.player_controller = PlayerController(
            self.input_state
        )

        #
        # Physics
        #

        self.player_physics_enabled = (
            self.level_manager.metadata
            .get_collision()
            .get(
                "player_physics",
                True,
            )
        )

        self.taskMgr.add(
            self.update_player,
            "updatePlayer",
        )

    #
    # UPDATE
    #

    def update_player(self, task):

        self.keyboard_input.update_keys()

        dt = globalClock.getDt()

        if self.dialog_manager.is_playing():

            self.input_state.reset()

            return task.cont

        for command in self.player_controller.build_commands():

            command.execute(
                self.player,
                dt,
            )

        if self.player_physics_enabled:

            self.player.update_physics(dt)

        if self.dialog_trigger:

            self.dialog_trigger.update()

        self.input_state.reset()

        return task.cont

    #
    # COLLISION
    #

    def setup_player_collision(self):

        print("[MAIN] Creating player collider.")

        self.cTrav = CollisionTraverser()

        player_node = CollisionNode(
            "Player"
        )

        player_node.addSolid(
            CollisionBox(
                Vec3(0, 0, 1),
                0.4,
                0.4,
                1,
            )
        )

        player_node.setFromCollideMask(
            BitMask32.bit(1)
        )

        player_node.setIntoCollideMask(
            BitMask32.allOff()
        )

        self.player_collision_np = (
            self.player.node.attachNewNode(
                player_node
            )
        )

        self.player_collision_np.show()

        self.player_pusher = (
            CollisionHandlerPusher()
        )

        self.player_pusher.addCollider(
            self.player_collision_np,
            self.player.node,
        )

        self.cTrav.addCollider(
            self.player_collision_np,
            self.player_pusher,
        )

        print("[MAIN] Player collider created.")

    #
    # LIGHTING
    #

    def setup_lighting(self):

        ambient = AmbientLight(
            "ambient"
        )

        ambient.setColor(
            (
                0.8,
                0.8,
                0.8,
                1,
            )
        )

        ambient_np = self.render.attachNewNode(
            ambient
        )

        self.render.setLight(
            ambient_np
        )

        sun = DirectionalLight(
            "sun"
        )

        sun.setColor(
            (
                1,
                1,
                1,
                1,
            )
        )

        sun_np = self.render.attachNewNode(
            sun
        )

        sun_np.setHpr(
            45,
            -60,
            0,
        )

        self.render.setLight(
            sun_np
        )

    #
    # FOG
    #

    def setup_fog(self):

        fog = Fog(
            "scence_fog"
        )

        fog.setColor(
            0.55,
            0.60,
            0.55,
        )

        fog.setExpDensity(
            0.015
        )

        self.render.setFog(
            fog
        )

        print("[MAIN] Fog enabled.")

    #
    # DEBUG
    #

    def debug_model(self):

        model = self.level_manager.current_level

        if model is None:
            return

        print(
            "========== MODEL DEBUG =========="
        )

        print(model)

        print(model.getBounds())

        model.ls()


if __name__ == "__main__":

    app = GameApp()

    app.run()