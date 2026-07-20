import json
from pathlib import Path


class MetadataManager:
    """
    Handles loading and querying level metadata.
    """

    def __init__(self):
        self._metadata = {}

    def load(self, metadata_path):
        metadata_path = Path(metadata_path)

        if not metadata_path.exists():
            print("[MetadataManager] ERROR:")
            print(f"Missing file: {metadata_path}")
            return False

        try:
            with metadata_path.open("r", encoding="utf-8") as file:
                self._metadata = json.load(file)

            print("[MetadataManager] Loaded:")
            print(f"    {metadata_path}")

            return True

        except json.JSONDecodeError as error:
            print("[MetadataManager] Invalid JSON:")
            print(error)

            return False

    def unload(self):
        self._metadata = {}

    def get_level(self):
        return self._metadata.get("level", {})

    def get_collision(self):
        """Return the collision settings for the currently loaded level."""
        return self._metadata.get("collision", {})

    def get_spawn(self):
        """Return player spawn settings for the currently loaded level."""
        return self._metadata.get("spawn", {})

    def get_surface(self, surface_name):
        return self._metadata.get("surface_types", {}).get(surface_name)

    def get_collision_surface(self, collision_name):
        """Convert collision object name into surface type"""
        return (
            self._metadata.get("collision_surfaces", {})
            .get(collision_name, {})
            .get("surface")
        )

    def get_object(self, object_name):
        return self._metadata.get("objects", {}).get(object_name)

    def get_object_type(self, object_type):
        return self._metadata.get("object_types", {}).get(object_type)

    def get_zone(self, zone_name):
        return self._metadata.get("zones", {}).get(zone_name)

    def get_node_metadata(self, node):
        """
        Resolve a Panda3D node using its metadata tag.
        """

        if not node.hasTag("metadata"):
            return None

        object_id = node.getTag("metadata")

        return self.get_object(object_id)

    @property
    def data(self):
        return self._metadata
