from pathlib import Path

from engine.managers.metadata_manager import MetadataManager


class LevelManager:
    def __init__(self, base):
        self.base = base

        self.metadata = MetadataManager()

        self.current_level = None
        self.current_level_path = None

    def load_level(self, level_folder):
        level_folder = Path(level_folder)

        print("=" * 50)
        print(f"Loading level: {level_folder}")
        print("=" * 50)

        self.unload_level()
        self.metadata.unload()

        metadata_file = level_folder / "level_metadata.json"

        if not self.metadata.load(metadata_file):
            print("[LevelManager] Metadata failed.")

            return False

        self.current_level_path = level_folder

        print()

        info = self.metadata.get_level()

        print("Level Information")
        print("-----------------")

        print(f"Name: {info.get('name')}")

        print(f"Version: {info.get('version')}")

        print()

        return True

    def unload_level(self):
        if self.current_level:
            self.current_level.removeNode()

            self.current_level = None
