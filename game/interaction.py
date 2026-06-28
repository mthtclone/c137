from direct.showbase.DirectObject import DirectObject

class PlayerInteraction(DirectObject):

    def __init__(self, game, player, movement):

        self.game = game
        self.player = player
        self.movement = movement
        self.blocks = game.world.blocks

        self.accept("e", self.interact)

    def interact(self):

        nearest = None
        nearest_dist = 5

        for block in self.blocks:

            dist = (block.getPos() - self.player.getPos()).length()

            if dist < nearest_dist:
                nearest = block
                nearest_dist = dist

        if nearest:
            nearest.setColor(0, 1, 0, 1)
            print("Object Interacted!")
        else:
            print("Nothing nearby.")