from pathlib import Path

from panda3d.core import TextNode

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

        #
        # Clear previous level
        #

        self.unload_level()
        self.metadata.unload()

        #
        # Load metadata
        #

        metadata_file = level_folder / "level_metadata.json"

        if not self.metadata.load(metadata_file):
            print("[LevelManager] Metadata failed.")

            return False

        #
        # Find model
        #

        model_file = self.find_level_model(level_folder)

        #
        # Load model
        #

        if model_file is not None:
            print("[LevelManager] Loading model...")

            self.current_level = self.base.loader.loadModel(str(model_file))

            self.current_level.reparentTo(self.base.render)

            print("[LevelManager] Model loaded:")
            print(f"    {model_file.name}")

        else:
            print("[LevelManager] WARNING")
            print("    No level model found.")

            self.current_level = self.create_placeholder()

        self.current_level_path = level_folder

        #
        # Level information
        #

        info = self.metadata.get_level()

        print()
        print("Level Information")
        print("-----------------")
        print(f"Name: {info.get('name')}")
        print(f"Version: {info.get('version')}")
        print()

        return True

    def find_level_model(self, level_folder):
        #
        # Preferred order
        #

        supported_models = ["level_model.glb", "level_model.gltf", "level_model.bam"]

        for filename in supported_models:
            path = level_folder / filename

            if path.exists():
                return path

        return None

    def unload_level(self):
        if self.current_level:
            self.current_level.removeNode()

            self.current_level = None

    def create_placeholder(self):
        text = TextNode("missing_model")

        text.setText("Missing level model")

        node = self.base.render.attachNewNode(text)

        node.setScale(2)

        node.setPos(0, 20, 5)

        return node
