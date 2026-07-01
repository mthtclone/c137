"""Lighting setup for the Panda3D game engine."""

from panda3d.core import AmbientLight, DirectionalLight, NodePath


class LightingManager:
    """Create ambient and directional lighting for the scene."""

    def __init__(self, render: NodePath) -> None:
        self.render = render

    def setup(self) -> None:
        """Add the lights to the render scene."""
        self._add_ambient_light()
        self._add_directional_light()

    def _add_ambient_light(self) -> None:
        """Add a soft ambient light for overall scene brightness."""
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor((0.4, 0.4, 0.45, 1.0))
        ambient_node = self.render.attachNewNode(ambient_light)
        self.render.setLight(ambient_node)

    def _add_directional_light(self) -> None:
        """Add a directional light to simulate sunlight."""
        directional_light = DirectionalLight("directional_light")
        directional_light.setColor((0.95, 0.9, 0.8, 1.0))
        directional_light.setShadowCaster(True, 1024, 1024)
        light_node = self.render.attachNewNode(directional_light)
        light_node.setHpr(-45, -45, 0)
        self.render.setLight(light_node)
