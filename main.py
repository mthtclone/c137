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
    Vec3,
)

from engine.managers.level_manager import LevelManager
from game.audio.audio_manager import AudioManager
from game.collision.ground_detector import GroundDetector
from game.collision.surface_detector import SurfaceDetector
from game.controller.player_controller import PlayerController
from game.core.player import Player
from game.input.input_state import InputState
from game.input.keyboard_input import KeyboardInput


class Game(ShowBase):
    def __init__(self):
        super().__init__()

        #
        # Enable PBR renderer
        #

        simplepbr.init()

        #
        # Disable default camera
        #

        self.disableMouse()

        #
        # Lighting
        #

        self.setup_lighting()

        #
        # Load level
        #

        self.level_manager = LevelManager(self)

        success = self.level_manager.load_level("levels/test_level")

        if success:
            spawn = self.level_manager.get_spawn_point()

            self.setup_player(spawn)

            #
            # Collision
            #

            self.setup_player_collision()

            #
            # Player input and movement
            #

            self.setup_player_controls()

            print()

            print("[MAIN] Level loaded successfully.")

            self.debug_model()

        else:
            print("[MAIN] Failed to load level.")

    #
    # Player setup
    #

    def setup_player(self, spawn):
        player_node = self.render.attachNewNode("Player")

        if spawn is not None:
            spawn_position = spawn.getPos(self.render)
            player_node.setPos(spawn_position + self.level_manager.get_spawn_offset())
            player_node.setH(spawn.getH(self.render))

        else:
            player_node.setPos(0, -20, 5)

        self.player = Player(
            player_node,
            self.camera,
            AudioManager(self),
            SurfaceDetector(self.level_manager.metadata),
            GroundDetector(self, player_node),
        )

        print("[MAIN] Camera height set.")

    def setup_player_controls(self):
        self.input_state = InputState()
        self.keyboard_input = KeyboardInput(self, self.input_state)
        self.player_controller = PlayerController(self.input_state)
        self.player_physics_enabled = self.level_manager.metadata.get_collision().get(
            "player_physics", True
        )

        self.taskMgr.add(self.update_player, "updatePlayer")

    def update_player(self, task):
        self.keyboard_input.update_keys()

        dt = globalClock.getDt()

        for command in self.player_controller.build_commands():
            command.execute(self.player, dt)

        if self.player_physics_enabled:
            self.player.update_physics(dt)

        self.input_state.reset()

        return task.cont

    #
    # Player collision
    #

    def setup_player_collision(self):
        print("[MAIN] Creating player collider.")

        self.cTrav = CollisionTraverser()

        player_node = CollisionNode("Player")

        player_node.addSolid(CollisionBox(Vec3(0, 0, 1), 0.4, 0.4, 1))

        player_node.setFromCollideMask(BitMask32.bit(1))

        player_node.setIntoCollideMask(BitMask32.allOff())

        self.player_collision_np = self.player.node.attachNewNode(player_node)

        #
        # Show debug box
        #

        self.player_collision_np.show()

        #
        # Push collisions
        #

        self.player_pusher = CollisionHandlerPusher()

        self.player_pusher.addCollider(self.player_collision_np, self.player.node)

        self.cTrav.addCollider(self.player_collision_np, self.player_pusher)

        print("[MAIN] Player collider created.")

    #
    # Lighting
    #

    def setup_lighting(self):
        ambient = AmbientLight("ambient")

        ambient.setColor((0.8, 0.8, 0.8, 1))

        ambient_np = self.render.attachNewNode(ambient)

        self.render.setLight(ambient_np)

        sun = DirectionalLight("sun")

        sun.setColor((1, 1, 1, 1))

        sun_np = self.render.attachNewNode(sun)

        sun_np.setHpr(45, -60, 0)

        self.render.setLight(sun_np)

    #
    # Debug
    #

    def debug_model(self):
        model = self.level_manager.current_level

        if model is None:
            return

        print("========== MODEL DEBUG ==========")

        print(model)

        print(model.getBounds())

        model.ls()


if __name__ == "__main__":
    game = Game()

    game.run()
