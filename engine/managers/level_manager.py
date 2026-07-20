from pathlib import Path

from panda3d.core import (
    BitMask32,
    CollisionBox,
    CollisionNode,
    CollisionPolygon,
    GeomNode,
    GeomVertexReader,
    Point3,
    TextNode,
    Vec3,
)

from engine.managers.metadata_manager import MetadataManager


class LevelManager:
    def __init__(self, base):
        self.base = base

        self.metadata = MetadataManager()

        self.current_level = None
        self.current_level_path = None

        self.spawn_point = None
        self.collision_root = None

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
        # Metadata
        #

        metadata_file = level_folder / "level_metadata.json"

        if not self.metadata.load(metadata_file):
            print("[LevelManager] Metadata failed.")

            return False

        #
        # Locate level model
        #

        model_file = self.find_level_model(level_folder)

        if model_file is not None:
            print("[LevelManager] Loading model...")

            # Panda3D's MINGW build does not resolve Windows-style absolute
            # paths (``C:\\...``) through its virtual file system.  Keep this
            # project-relative path and use forward slashes on every platform.
            self.current_level = self.base.loader.loadModel(model_file.as_posix())

            self.current_level.reparentTo(self.base.render)

            print("[LevelManager] Model loaded:")
            print(f"    {model_file.name}")

            self.find_spawn_point()

        else:
            print("[LevelManager] WARNING")
            print("    No supported level model found.")

            self.current_level = self.create_placeholder()

        self.current_level_path = level_folder

        self.load_collision(level_folder)

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
        supported_models = ["level_model.glb", "level_model.gltf", "level_model.bam"]

        for filename in supported_models:
            path = level_folder / filename

            if path.exists():
                return path

        return None

    def find_spawn_point(self):
        self.spawn_point = None

        spawn = self.current_level.find("**/SpawnPoint")

        if spawn.isEmpty():
            print("[LevelManager] No SpawnPoint found.")

            return

        self.spawn_point = spawn

        print("[LevelManager] SpawnPoint found.")

        print(f"    Position: {spawn.getPos(self.base.render)}")

        print(f"    Rotation: {spawn.getHpr(self.base.render)}")

    def get_spawn_point(self):
        return self.spawn_point

    def get_spawn_offset(self):
        offset = self.metadata.get_spawn().get("offset", [0, 0, 1])
        return Vec3(*offset)

    def unload_level(self):
        if self.collision_root:
            self.collision_root.removeNode()
            self.collision_root = None

        if self.current_level:
            self.current_level.removeNode()

            self.current_level = None

        self.spawn_point = None

    def create_placeholder(self):
        text = TextNode("missing_model")

        text.setText("Missing level model")

        node = self.base.render.attachNewNode(text)

        node.setScale(2)

        node.setPos(0, 20, 5)

        return node

    #
    # Collision
    #

    def load_collision(self, level_folder):
        """Build static collision from ``COL_`` meshes in the level model.

        Collision meshes are authored in Blender and exported with the level,
        while Panda3D collision nodes are created here.  This keeps gameplay
        configuration out of Blender and lets the mesh stay invisible in game.
        """
        settings = self.metadata.get_collision()
        mask = BitMask32.bit(settings.get("mask", 1))
        node_prefix = settings.get("node_prefix", "COL_")

        self.collision_root = self.base.render.attachNewNode("LevelCollision")

        if self._load_collision_meshes(node_prefix, mask):
            return

        fallback = settings.get("fallback")
        if fallback:
            self._load_box_collision(fallback, mask)
            print("[LevelManager] Using metadata collision fallback.")
        else:
            print("[LevelManager] WARNING: Level has no collision.")

    def _load_collision_meshes(self, node_prefix, mask):
        """Convert every GeomNode below a ``COL_`` node to collision faces."""
        collision_meshes = self.current_level.findAllMatches(f"**/{node_prefix}*")

        if collision_meshes.getNumPaths() == 0:
            print(
                f"[LevelManager] No collision meshes found with '{node_prefix}' prefix."
            )
            return False

        triangle_count = 0
        geometry_source_count = 0
        debug_collision = self.metadata.get_collision().get("debug", False)
        seen_geom_nodes = set()
        for collision_mesh in collision_meshes:
            # A COL_ object can be either a GeomNode itself or a parent that
            # contains several GeomNodes after glTF import.
            geom_paths = collision_mesh.findAllMatches("**/+GeomNode")
            if isinstance(collision_mesh.node(), GeomNode):
                geom_paths.addPath(collision_mesh)

            if debug_collision:
                collision_mesh.show()
                collision_mesh.setColor(1, 0, 0, 1)
                collision_mesh.setRenderModeWireframe()
                collision_mesh.setTwoSided(True)
            else:
                collision_mesh.hide()

            for geom_path in geom_paths:
                geometry_source_count += 1
                geom_node = geom_path.node()
                node_id = id(geom_node)
                if node_id in seen_geom_nodes:
                    continue
                seen_geom_nodes.add(node_id)

                collision_node = CollisionNode(f"Collision-{geom_path.getName()}")
                collision_node.setIntoCollideMask(mask)
                collider = geom_path.attachNewNode(collision_node)

                for index in range(geom_node.getNumGeoms()):
                    geom = geom_node.getGeom(index)
                    reader = GeomVertexReader(geom.getVertexData(), "vertex")
                    for primitive_index in range(geom.getNumPrimitives()):
                        primitive = geom.getPrimitive(primitive_index).decompose()
                        vertices = primitive.getVertexList()

                        for vertex_index in range(0, len(vertices) - 2, 3):
                            points = []
                            for offset in range(3):
                                reader.setRow(vertices[vertex_index + offset])
                                points.append(Point3(reader.getData3f()))
                            collision_node.addSolid(CollisionPolygon(*points))
                            triangle_count += 1

                if debug_collision:
                    collider.show()
                else:
                    collider.hide()

        if triangle_count:
            print(
                f"[LevelManager] Loaded {triangle_count} collision triangles "
                f"from {collision_meshes.getNumPaths()} COL_ node(s)."
            )
        elif geometry_source_count == 0:
            print(
                "[LevelManager] COL_ nodes were found, but they contain no "
                "exported mesh geometry."
            )

        return triangle_count > 0

    def _load_box_collision(self, settings, mask):
        if settings.get("type") != "box":
            print("[LevelManager] Unsupported collision fallback type.")
            return

        center = Point3(*settings["center"])
        half_extents = Point3(*settings["half_extents"])

        collision_node = CollisionNode("LevelCollisionFallback")
        collision_node.addSolid(CollisionBox(center, *half_extents))
        collision_node.setIntoCollideMask(mask)
        self.collision_root.attachNewNode(collision_node)
