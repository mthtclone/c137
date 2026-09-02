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
            "include_patterns": [
                "**/*.png",
                "**/*.*",
                "**/*.jpg",
                "**/*.egg",
                "**/*.bam",
                "**/*.gltf",
                "**/*.gltf.rpc",
                "**/*.txt",
            ],
            # 3. List the internal Panda3D plugins you require
            "plugins": [
                "pandagl",  # OpenGL renderer (essential)
                "p3openal_audio",  # Audio player (essential for sound)
            ],
            # 4. List your third-party pip packages here
            "platforms": ["win_amd64"],  # Builds for 64-bit Windows
            "include_modules": [
                "gltf",
                "simplepbr" "black",
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
                "panda3d-blend2bam",
                "panda3d-gltf",
                "panda3d-simplepbr",
                "pathspec",
                "pillow",
                "platformdirs",
                "pre_commit",
                "pyquaternion",
                "python-discovery",
                "pytokens",
                "PyYAML",
                "requests",
                "ruff",
                "setuptools",
                "typing_extensions",
                "urllib3",
                "virtualenv",
            ],
        }
    },
)

# from setuptools import setup, find_packages


# setup(
#     name="CopenhagenTrip",
#     version="0.1.0",

#     packages=find_packages(),
#     py_modules=["main"],

#     options={
#         "build_apps": {

#             "console_apps": {
#                 "CopenhagenTrip": "main.py"
#             },

#             "platforms": [
#                 "win32"
#             ],

#             "include_patterns": [
#                 "assets/**",
#                 "game/assets/**",
#                 "levels/**"
#             ],

#             "plugins": [
#                 "pandagl",
#                 "p3openal"
#             ],

#             "include_modules": [
#                 "gltf",
#                 "simplepbr"
#             ],

#             "exclude_patterns": [
#                 "**/__pycache__/**",
#                 "**/*.pyc"
#             ]
#         }
#     },

#     install_requires=[
#         "Panda3D",
#         "panda3d-gltf",
#         "panda3d-simplepbr"
#     ]
# )

# Code archived as artifact
