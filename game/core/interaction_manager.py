from direct.gui.OnscreenText import OnscreenText
from panda3d.core import (
    BitMask32,
    CollisionHandlerQueue,
    CollisionNode,
    CollisionRay,
    CollisionSphere,
    CollisionTraverser,
    LineSegs,
    NodePath,
    TextNode,
    Vec3,
)

from game.core.pickable import DoorInteractable, Pickable


class InteractionManager:
    """Raycast interaction manager for camera-focused objects."""

    def __init__(self, base, camera, max_distance=3.0):
        self.base = base
        self.camera = camera
        self.max_distance = max_distance
        self.current_target = None
        self.registry = {}

        self.traverser = CollisionTraverser()
        self.queue = CollisionHandlerQueue()

        ray_node = CollisionNode("interact_ray")
        ray_node.setFromCollideMask(BitMask32.bit(1))
        ray_node.setIntoCollideMask(BitMask32.allOff())
        self.ray = CollisionRay()
        ray_node.addSolid(self.ray)

        self.ray_np = camera.attachNewNode(ray_node)
        self.traverser.addCollider(self.ray_np, self.queue)

        self.prompt_text = OnscreenText(
            text="",
            pos=(0, -0.82),
            scale=0.055,
            fg=(1, 1, 1, 1),
            align=TextNode.ACenter,
            mayChange=True,
        )

        self._create_sample_objects()

    def register(self, collision_node, interactable):
        collision_node.setCollideMask(BitMask32.bit(1))
        self.registry[collision_node] = interactable

    def update(self):
        self.ray.setOrigin(0, 0, 0)
        self.ray.setDirection(0, 1, 0)

        self.queue.clearEntries()
        self.traverser.traverse(self.base.render)
        self.queue.sortEntries()

        new_target = self._find_target_from_ray()

        if new_target is not self.current_target:
            if self.current_target:
                self.current_target.on_blur()
            if new_target:
                new_target.on_focus()
            self.current_target = new_target

        self._update_prompt()

    def try_interact(self, player, interaction_key="E"):
        if self.current_target:
            if self.current_target.interaction_key != interaction_key:
                return
            self.current_target.on_interact(player)
            return

        # E also drops the currently held pickable when no target is focused.
        if interaction_key == "E" and player.held_pickable:
            player.held_pickable.drop(player)

    def _find_target_from_ray(self):
        if self.queue.getNumEntries() == 0:
            return None

        for index in range(self.queue.getNumEntries()):
            entry = self.queue.getEntry(index)
            hit_node = entry.getIntoNodePath()
            distance = entry.getSurfacePoint(self.camera).length()

            if distance > self.max_distance:
                continue

            interactable = self.registry.get(hit_node)
            if interactable and interactable.can_interact():
                return interactable

        return None

    def _update_prompt(self):
        if not self.current_target:
            self.prompt_text.setText("")
            return

        self.prompt_text.setText(
            f"Press {self.current_target.interaction_key} "
            f"to {self.current_target.prompt}"
        )

    def _create_sample_objects(self):
        self._create_pickable("Key", (1.0, 3.0, 0.75), (1.0, 0.9, 0.25, 1.0))
        self._create_pickable(
            "Health Pack",
            (-1.0, 3.0, 0.75),
            (0.9, 0.15, 0.18, 1.0),
        )
        self._create_door("Open Door", (0.0, 5.0, 1.2), (0.4, 0.72, 0.52, 1.0))

    def _create_pickable(self, name, position, color):
        node, collision_node = self._create_sample_node(name, position, color)
        self.register(collision_node, Pickable(node, collision_node, "Pick up"))

    def _create_door(self, name, position, color):
        node, collision_node = self._create_sample_node(name, position, color)
        self.register(collision_node, DoorInteractable(node))

    def _create_sample_node(self, name, position, color):
        node = NodePath(name)
        node.reparentTo(self.base.render)
        node.setPos(*position)
        node.setColor(*color)

        self._attach_wire_box(node, f"{name}_wire", color)
        self._attach_label(node, name)

        # A simple sphere is enough for sample ray targeting.
        collision = CollisionNode(f"{name}_collision")
        collision.addSolid(CollisionSphere(0, 0, 0, 0.65))
        collision.setIntoCollideMask(BitMask32.bit(1))
        collision.setFromCollideMask(BitMask32.allOff())
        collision_np = node.attachNewNode(collision)

        return node, collision_np

    def _attach_wire_box(self, parent, name, color):
        lines = LineSegs(name)
        lines.setThickness(3)
        lines.setColor(*color)

        half_width = 0.45
        bottom_z = -0.45
        top_z = 0.45
        corners = [
            Vec3(-half_width, -half_width, bottom_z),
            Vec3(half_width, -half_width, bottom_z),
            Vec3(half_width, half_width, bottom_z),
            Vec3(-half_width, half_width, bottom_z),
            Vec3(-half_width, -half_width, top_z),
            Vec3(half_width, -half_width, top_z),
            Vec3(half_width, half_width, top_z),
            Vec3(-half_width, half_width, top_z),
        ]
        edges = [
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 4),
            (0, 4),
            (1, 5),
            (2, 6),
            (3, 7),
        ]

        for start, end in edges:
            lines.moveTo(corners[start])
            lines.drawTo(corners[end])

        parent.attachNewNode(lines.create())

    def _attach_label(self, parent, label):
        text_node = TextNode(f"{label}_label")
        text_node.setText(label)
        text_node.setAlign(TextNode.ACenter)
        text_path = parent.attachNewNode(text_node)
        text_path.setBillboardAxis()
        text_path.setPos(0, 0, 0.85)
        text_path.setScale(0.2)
        text_path.setColor(1, 1, 1, 1)

