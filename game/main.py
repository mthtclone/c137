from direct.showbase.ShowBase import ShowBase
from test_world import TestWorld
from player import Player

class Game(ShowBase):

    def __init__(self):
        super().__init__()

        self.disableMouse()

        # Create world first
        self.world = TestWorld()

        # Create player
        self.player = Player(self)

game = Game()
game.run()