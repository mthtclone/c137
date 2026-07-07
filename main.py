from direct.showbase.ShowBase import ShowBase
from direct.task import Task

from game.controller.player_controller import PlayerController
from game.core.interaction_manager import InteractionManager
from game.core.player import Player
from game.input.input_state import InputState
from game.input.keyboard_input import KeyboardInput


class Prototype(ShowBase):

    def __init__(self):
        super().__init__()

        self.disableMouse()

        # WORLD
        self.model = self.loader.loadModel("models/environment")
        self.model.reparentTo(self.render)
        self.model.setScale(0.1)
        self.model.setPos(-8, 42, 0)

        # INPUT SYSTEM
        self.state = InputState()
        self.keyboard = KeyboardInput(self, self.state)
        self.controller = PlayerController(self.state)

        # PLAYER
        player_node = self.render.attachNewNode("Player")
        self.interaction_manager = InteractionManager(self, self.camera)
        self.player = Player(player_node, self.camera, self.interaction_manager)

        # UPDATE LOOP
        self.taskMgr.add(self.update, "update")

    def update(self, task):

        dt = globalClock.getDt()

        # IMPORTANT: update real-time key state
        self.keyboard.update_keys()

        commands = self.controller.build_commands()

        for cmd in commands:
            cmd.execute(self.player, dt)

        self.interaction_manager.update()

        self.state.reset()

        return Task.cont


app = Prototype()
app.run()
