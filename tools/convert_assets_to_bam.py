"""
Convert every .glb/.gltf model under levels/ and assets/ into a .bam file,
and update each level's level_metadata.json "assets" table to point at the
converted .bam files.

Run this BEFORE `python setup.py build_apps`. The compiled build ships only
.bam files -- see the note at the top of setup.py's include_patterns for why
raw .glb/.gltf cannot be shipped in a frozen build.

Usage:
    python tools/convert_assets_to_bam.py

Requires panda3d-gltf to be installed (`pip install panda3d-gltf`), which
provides the `gltf2bam` command-line tool used here. This is a build-time
dependency only -- it does not need to be present in the compiled game.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SEARCH_DIRS = [REPO_ROOT / "levels", REPO_ROOT / "assets"]

GLTF_EXTENSIONS = {".glb", ".gltf"}


def find_gltf_files():
    for directory in SEARCH_DIRS:
        if not directory.exists():
            continue
        for path in directory.rglob("*"):
            if path.suffix.lower() in GLTF_EXTENSIONS:
                yield path


def convert_to_bam(source: Path) -> Path:
    """Convert a single .glb/.gltf file to .bam using gltf2bam."""
    destination = source.with_suffix(".bam")

    print(f"[convert] {source.relative_to(REPO_ROOT)} -> {destination.name}")

    result = subprocess.run(
        ["gltf2bam", str(source), str(destination)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print(f"[convert] FAILED: {source}")
        print(result.stdout)
        print(result.stderr)
        raise SystemExit(1)

    return destination


def update_level_metadata(level_folder: Path, converted: dict[Path, Path]):
    """Rewrite assets.<name>.path entries in level_metadata.json to .bam."""
    metadata_path = level_folder / "level_metadata.json"

    if not metadata_path.exists():
        return

    with metadata_path.open("r", encoding="utf-8") as file:
        metadata = json.load(file)

    assets = metadata.get("assets", {})
    changed = False

    for asset_name, asset_info in assets.items():
        asset_path = REPO_ROOT / asset_info.get("path", "")
        bam_path = asset_path.with_suffix(".bam")

        if asset_path.suffix.lower() in GLTF_EXTENSIONS and bam_path.exists():
            new_relative = bam_path.relative_to(REPO_ROOT).as_posix()
            print(f"[metadata] {asset_name}: {asset_info['path']} -> {new_relative}")
            asset_info["path"] = new_relative
            changed = True
        elif asset_path.suffix.lower() not in GLTF_EXTENSIONS.union({".bam"}):
            print(
                f"[metadata] WARNING: {asset_name} uses unsupported format "
                f"'{asset_path.suffix}' ({asset_info.get('path')}). "
                "Panda3D cannot load this at runtime -- re-export it as .glb."
            )

    if changed:
        backup_path = metadata_path.with_suffix(".json.bak")
        shutil.copy2(metadata_path, backup_path)

        with metadata_path.open("w", encoding="utf-8") as file:
            json.dump(metadata, file, indent=4)

        print(
            f"[metadata] Updated {metadata_path.relative_to(REPO_ROOT)} "
            f"(backup at {backup_path.name})"
        )


def main():
    if shutil.which("gltf2bam") is None:
        print(
            "gltf2bam not found on PATH. Install it with:\n"
            "    pip install panda3d-gltf\n"
        )
        sys.exit(1)

    gltf_files = list(find_gltf_files())

    if not gltf_files:
        print("No .glb/.gltf files found under levels/ or assets/.")
        return

    converted = {}
    for source in gltf_files:
        converted[source] = convert_to_bam(source)

    level_folders = {path.parent for path in gltf_files if "levels" in path.parts}
    # level_model.glb lives directly in the level folder; also check every
    # level folder even if only its instanced assets referenced .glb files.
    level_folders |= {p for p in (REPO_ROOT / "levels").glob("*") if p.is_dir()}

    for level_folder in level_folders:
        update_level_metadata(level_folder, converted)

    print(f"\nDone. Converted {len(gltf_files)} file(s).")
    print("Run `python setup.py build_apps` to produce the compiled build.")


if __name__ == "__main__":
    main()
