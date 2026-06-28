from panda3d.core import (
    CollisionNode,
    CollisionSphere,
    CollisionTraverser,
    CollisionHandlerPusher
)

from movement import PlayerMovement
from camera import FirstPersonCamera
from interaction import PlayerInteraction


class Player:

    def __init__(self, game):

        self.game = game

        # -------------------------
        # PLAYER NODE
        # -------------------------
        self.node = render.attachNewNode("Player")
        self.node.setPos(0, 0, 0)

        # -------------------------
        # COLLISION SETUP
        # -------------------------
        self.cTrav = CollisionTraverser()
        self.pusher = CollisionHandlerPusher()

        # player collision shape
        collider_node = CollisionNode("player")
        collider_node.addSolid(CollisionSphere(0, 0, 0, 1))

        self.collider = self.node.attachNewNode(collider_node)

        self.cTrav.addCollider(self.collider, self.pusher)
        self.pusher.addCollider(self.collider, self.node)

        # -------------------------
        # SYSTEMS
        # -------------------------
        self.camera = FirstPersonCamera(game, self.node)
        self.movement = PlayerMovement(game, self.node)

        # interaction (optional)
        self.interaction = PlayerInteraction(game, self.node, self.movement)

        # IMPORTANT: start traversal
        game.taskMgr.add(self.update, "CollisionUpdate")

    def update(self, task):

        self.cTrav.traverse(render)

        return task.cont