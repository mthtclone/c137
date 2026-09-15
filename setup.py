from setuptools import setup

setup(
    name="CopenhagenTrip",
    version="0.1.0",
    options={
        "build_apps": {
            # 1. Add your main script file name here
            "gui_apps": {
                "CopenhagentTrip": "main.py",
            },
            # 2. Add all your asset extensions and folders here
            #
            # NOTE: .glb / .gltf are intentionally NOT included here.
            # panda3d-gltf registers itself with Panda3D via a Python
            # entry point, and that registration does not survive
            # freezing into a standalone .exe (importlib.metadata sees
            # no installed-package metadata inside a frozen build), so
            # any .glb/.gltf shipped as-is will fail to load at runtime
            # even though they load fine when run from source.
            #
            # Run `python tools/convert_assets_to_bam.py` before packaging
            # to convert every .glb/.gltf under levels/ and assets/ into
            # .bam (which Panda3D reads natively, no plugin required) and
            # to rewrite level_metadata.json asset paths to match. Only
            # the resulting .bam files need to ship with the build.
            "include_patterns": [
                "**/*.png",
                "**/*.jpg",
                "**/*.egg",
                "**/*.bam",
                "**/*.json",
                "**/*.txt",
            ],
            # Never bundle the source glTF/GLB files into the frozen
            # build — they cannot be loaded there (see note above).
            # Keep them for local development / re-exporting only.
            "exclude_patterns": [
                "**/*.glb",
                "**/*.gltf",
                "**/*.gltf.rpc",
                "**/*.fbx",
            ],
            # 3. List the internal Panda3D plugins you require
            "plugins": [
                "pandagl",  # OpenGL renderer (essential)
                "p3openal_audio",  # Audio player (essential for sound)
            ],
            # 4. List your third-party pip packages here
            "platforms": ["win_amd64"],  # Builds for 64-bit Windows
            "include_modules": [
                "certifi",
                "cfgv",
                "charset-normalizer",
                "click",
                "colorama",
                "distlib",
                "filelock",
                "identify",
                "idna",
                "mypy_extensions",
                "nodeenv",
                "numpy",
                "packaging",
                "Panda3D",
                "panda3d-simplepbr",
                "pathspec",
                "pillow",
                "platformdirs",
                "pyquaternion",
                "python-discovery",
                "pytokens",
                "PyYAML",
                "requests",
                "setuptools",
                "simplepbr",
                "typing_extensions",
                "urllib3",
                "virtualenv",
                # panda3d-gltf / panda3d-blend2bam / ruff / black / pre_commit
                # are build-time-only tools (asset conversion + dev
                # tooling). They are deliberately NOT frozen into the
                # runtime app.
            ],
        }
    },
)
