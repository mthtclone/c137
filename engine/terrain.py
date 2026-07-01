"""Terrain loading module for the Panda3D game engine."""

from pathlib import Path
from panda3d.core import NodePath, TextNode, TransparencyAttrib


class TerrainLoader:
    """Load a terrain model from a GLB file into the scene."""

    def __init__(self, render: NodePath) -> None:
        self.render = render
        self.terrain_file = "assets/models/terrain.glb"
        self.terrain_scale = 1.0

    def load(self) -> None:
        """Load the terrain model or show a friendly message if it is missing."""
        if not Path(self.terrain_file).exists():
            self._show_missing_terrain_message()
            return

        terrain_node = loader.loadModel(self.terrain_file)

        if terrain_node.isEmpty():
            print(
                f"Error: Could not load terrain from {self.terrain_file}."
            )
            self._show_missing_terrain_message()
            return

        # Preserve textures and materials from the GLB file.
        terrain_node.setShaderAuto()
        terrain_node.setTransparency(TransparencyAttrib.MNone)

        # Attach the terrain to the render graph so it becomes visible.
        terrain_node.reparentTo(self.render)

        # Place the terrain at the world origin.
        terrain_node.setPos(0, 0, 0)

        # Keep the default rotation unless you need to adjust it later.
        terrain_node.setScale(self.terrain_scale)

        print(f"Terrain loaded successfully from {self.terrain_file}")

    def _show_missing_terrain_message(self) -> None:
        """Show a placeholder message when the terrain file is not found."""
        text_node = TextNode("terrain_placeholder")
        text_node.setText(
            "Missing terrain model:\nassets/models/terrain.glb"
        )
        text_node.setAlign(TextNode.ACenter)
        text_node_path = self.render.attachNewNode(text_node)
        text_node_path.setScale(1.5)
        text_node_path.setPos(0, 10, 2)
