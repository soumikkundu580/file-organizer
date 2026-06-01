#!/usr/bin/env python3
from pathlib import Path
import shutil
import argparse
from collections import defaultdict

FILE_TYPES = {
    "Pictures": [
        ".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg",
        ".bmp", ".tiff", ".ico", ".heic", ".heif",
        ".raw", ".cr2", ".nef", ".arw", ".dng",
        ".psd", ".ai", ".eps", ".indd", ".xcf"
    ],

    "Videos": [
        ".mp4", ".mkv", ".mov", ".avi", ".webm",
        ".flv", ".wmv", ".mpeg", ".mpg",
        ".3gp", ".m4v", ".ts", ".vob", ".ogv"
    ],

    "Music": [
        ".mp3", ".wav", ".flac", ".ogg",
        ".aac", ".m4a", ".wma", ".alac",
        ".aiff", ".mid", ".midi", ".opus"
    ],

    "Documents": [
        ".pdf", ".doc", ".docx", ".txt",
        ".ppt", ".pptx", ".xls", ".xlsx",
        ".csv", ".md", ".rtf", ".odt",
        ".ods", ".odp", ".tex", ".epub",
        ".pages"
    ],

    "Archives": [
        ".zip", ".rar", ".7z", ".tar",
        ".gz", ".bz2", ".xz", ".iso",
        ".cab", ".tgz"
    ],

    "Code": [
        ".py", ".js", ".ts", ".jsx", ".tsx",
        ".cpp", ".c", ".h", ".hpp",
        ".java", ".kt", ".rs", ".go",
        ".php", ".rb", ".swift",
        ".cs", ".sh", ".bat", ".ps1",
        ".html", ".css", ".scss",
        ".sql", ".json", ".xml",
        ".yaml", ".yml",
        ".vue", ".dart", ".lua"
    ],

    "Databases": [
        ".db", ".sqlite", ".sqlite3",
        ".mdb", ".accdb", ".sqlitedb"
    ],

    "Executables": [
        ".exe", ".msi", ".apk", ".aab",
        ".app", ".bin", ".dmg",
        ".run", ".deb", ".rpm",
        ".jar"
    ],

    "Fonts": [
        ".ttf", ".otf", ".woff", ".woff2"
    ],

    "3D Models": [
        ".obj", ".fbx", ".stl",
        ".blend", ".dae", ".3ds",
        ".gltf", ".glb",
        ".step", ".iges"
    ],

    "Config Files": [
        ".ini", ".cfg", ".conf",
        ".env", ".toml",
        ".properties"
    ],

    "Logs": [
        ".log"
    ],

    "Scripts": [
        ".command", ".zsh", ".fish"
    ],

    "Disk Images": [
        ".iso", ".img", ".dmg"
    ],

    "Data Science": [
        ".ipynb", ".parquet",
        ".feather", ".h5", ".pkl"
    ],

    "GIS & Maps": [
        ".shp", ".geojson", ".kml"
    ]
}

SYSTEM_PROTECTED_DIRS = {
    ".git", ".svn", ".hg", "node_modules", ".npm",
    ".venv", "venv", ".env", "__pycache__",
    ".cache", ".local", ".config", ".aws",
    "snap", "flatpak"
}

def get_file_category(extension: str) -> str:
    extension = extension.lower()

    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category

    return "Others"


def format_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"

        size /= 1024

    return f"{size:.2f} PB"


def get_unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    counter = 1

    while True:
        new_name = (
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_destination = destination.parent / new_name

        if not new_destination.exists():
            return new_destination

        counter += 1


def should_skip(item: Path, organized_folders: set) -> bool:
    """Skip dotfiles, files in organized folders, and protected directories."""
    if item.name.startswith("."):
        return True

    # Check if any parent directory is in organized folders
    for parent in item.parents:
        if parent.name in organized_folders:
            return True

    return False


def is_protected_directory(path: Path, restricted_dirs: set) -> bool:
    """Check if a directory is protected (system config or user-restricted)."""
    if path.name in SYSTEM_PROTECTED_DIRS:
        return True
    
    if path.name in restricted_dirs:
        return True
    
    return False


def collect_files_by_category(
    target_folder: Path,
    recursive: bool,
    organized_folders: set,
    restricted_dirs: set
) -> dict:
    """Collect files grouped by category for permission prompt."""
    files_by_category = defaultdict(list)

    if recursive:
        items = target_folder.rglob("*")
    else:
        items = target_folder.iterdir()

    for item in items:
        try:
            if not item.is_file():
                continue

            if should_skip(item, organized_folders):
                continue

            # Check for protected dirs in path
            if any(is_protected_directory(p, restricted_dirs) for p in item.parents):
                continue

            extension = item.suffix.lower()
            category = get_file_category(extension)
            
            # Store relative path from target folder
            rel_path = item.relative_to(target_folder)
            files_by_category[category].append((item, str(rel_path)))

        except Exception:
            pass

    return files_by_category


def prompt_for_permission(files_by_category: dict) -> set:
    """Ask user for permission to organize file types."""
    if not files_by_category:
        print("\nNo files to organize found.")
        return set()

    print("\n" + "="*60)
    print("FILE ORGANIZATION SUMMARY")
    print("="*60)

    for category in sorted(files_by_category.keys()):
        files = files_by_category[category]
        print(f"\n{category}: ({len(files)} files)")
        for _, rel_path in files[:5]:
            print(f"  - {rel_path}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more files")

    print("\n" + "="*60)
    
    while True:
        response = input("Do you want to organize these files? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            return set(files_by_category.keys())
        elif response in ["no", "n"]:
            return set()
        else:
            print("Please enter 'yes' or 'no'.")


def prompt_for_restricted_dirs() -> set:
    """Ask user for directories to exclude from organization."""
    print("\n" + "="*60)
    print("RESTRICT DIRECTORIES")
    print("="*60)
    print("Enter directory names to exclude from organization.")
    print("Separate multiple directories with commas (or press Enter to skip).")
    print("Example: My Projects, Important Docs, Work")
    
    response = input("Restricted directories: ").strip()
    
    if not response:
        return set()
    
    restricted = {d.strip() for d in response.split(",")}
    restricted = {d for d in restricted if d}
    
    if restricted:
        print(f"\nRestricted directories: {', '.join(restricted)}")
    
    return restricted


def organize_folder(
    target_folder: Path,
    recursive: bool = False,
    dry_run: bool = False,
    categories_to_organize: set = None,
    restricted_dirs: set = None
):
    """Organize files into category folders."""
    if not target_folder.exists():
        print(f"Error: Folder not found: {target_folder}")
        return

    if restricted_dirs is None:
        restricted_dirs = set()
    
    if categories_to_organize is None:
        categories_to_organize = set(FILE_TYPES.keys())
    
    organized_folders = set(FILE_TYPES.keys())
    
    print(f"\nScanning: {target_folder}")

    moved_count = 0
    error_count = 0

    if recursive:
        # In recursive mode, organize files in each directory
        items = list(target_folder.rglob("*"))
        items_to_process = []
        
        for item in items:
            try:
                if not item.is_file():
                    continue

                if should_skip(item, organized_folders):
                    continue

                # Check for protected/restricted dirs in path
                if any(is_protected_directory(p, restricted_dirs) for p in item.parents):
                    continue

                items_to_process.append(item)
            except Exception:
                pass
        
        # Group items by their parent directory
        by_parent = defaultdict(list)
        for item in items_to_process:
            by_parent[item.parent].append(item)
        
        # Process each parent directory
        for parent_dir, files in by_parent.items():
            for item in files:
                try:
                    extension = item.suffix.lower()
                    category = get_file_category(extension)

                    if category not in categories_to_organize:
                        continue

                    # Create folder in the SAME directory as the file
                    destination_folder = parent_dir / category

                    destination_file = destination_folder / item.name
                    destination_file = get_unique_destination(destination_file)

                    size = format_size(item.stat().st_size)

                    if dry_run:
                        print(
                            f"[DRY RUN] {item.name} | {category} | "
                            f"{size} -> {destination_file.relative_to(target_folder)}"
                        )
                        continue

                    destination_folder.mkdir(exist_ok=True, parents=True)
                    shutil.move(str(item), str(destination_file))

                    print(
                        f"MOVED {item.name} | {category} | {size}"
                    )

                    moved_count += 1

                except Exception as e:
                    print(f"ERROR {item.name} | {str(e)}")
                    error_count += 1

    else:
        # Non-recursive: organize files at target folder level only
        items = target_folder.iterdir()

        for item in items:
            try:
                if not item.is_file():
                    continue

                if should_skip(item, organized_folders):
                    continue

                # Check for protected/restricted dirs in path
                if any(is_protected_directory(p, restricted_dirs) for p in item.parents):
                    continue

                extension = item.suffix.lower()
                category = get_file_category(extension)

                if category not in categories_to_organize:
                    continue

                destination_folder = target_folder / category
                destination_file = destination_folder / item.name
                destination_file = get_unique_destination(destination_file)

                size = format_size(item.stat().st_size)

                if dry_run:
                    print(
                        f"[DRY RUN] {item.name} | {category} | {size}"
                    )
                    continue

                destination_folder.mkdir(exist_ok=True)
                shutil.move(str(item), str(destination_file))

                print(
                    f"MOVED {item.name} | {category} | {size}"
                )

                moved_count += 1

            except Exception as e:
                print(f"ERROR {item.name} | {str(e)}")
                error_count += 1

    print(f"\nCompleted! Moved {moved_count} files.")
    if error_count > 0:
        print(f"Errors: {error_count}")



def parse_arguments():
    parser = argparse.ArgumentParser(
        description="File Organizer - Organize files into categories"
    )

    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Folder to organize (interactive if not provided)"
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Scan recursively and organize in each subfolder"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview without moving files"
    )

    parser.add_argument(
        "--no-prompt",
        action="store_true",
        help="Skip permission prompt (organize all file types)"
    )

    parser.add_argument(
        "--restrict",
        type=str,
        default=None,
        help="Comma-separated list of directories to exclude"
    )

    return parser.parse_args()


def print_header():
    """Print application header."""
    print("\n" + "="*60)
    print("FILE ORGANIZER")
    print("="*60)


def get_target_path() -> Path:
    """Get target path from user input."""
    while True:
        path_input = input("\nEnter folder path to organize (or press Enter for Downloads): ").strip()
        
        if not path_input:
            target = Path.home() / "Downloads"
        else:
            target = Path(path_input).expanduser()
        
        if target.exists() and target.is_dir():
            return target
        else:
            print(f"Error: Path does not exist or is not a directory: {target}")


def main():
    print_header()
    
    args = parse_arguments()

    # Get target folder
    if args.path:
        target_folder = Path(args.path).expanduser()
        if not target_folder.exists() or not target_folder.is_dir():
            print(f"Error: Invalid path: {target_folder}")
            return
    else:
        target_folder = get_target_path()

    print(f"Target folder: {target_folder}")

    # Get restricted directories
    restricted_dirs = set()
    if args.restrict:
        restricted_dirs = {d.strip() for d in args.restrict.split(",")}
    else:
        restrict_prompt = input("\nDo you want to restrict any directories? (yes/no): ").strip().lower()
        if restrict_prompt in ["yes", "y"]:
            restricted_dirs = prompt_for_restricted_dirs()

    # Get file categories to organize
    categories_to_organize = None
    if not args.no_prompt:
        files_by_category = collect_files_by_category(
            target_folder,
            args.recursive,
            set(FILE_TYPES.keys()),
            restricted_dirs
        )
        categories_to_organize = prompt_for_permission(files_by_category)
        
        if not categories_to_organize:
            print("Operation cancelled.")
            return

    # Show dry-run notice if applicable
    if args.dry_run:
        print("\nRUNNING IN DRY-RUN MODE (no files will be moved)")

    # Organize files
    organize_folder(
        target_folder=target_folder,
        recursive=args.recursive,
        dry_run=args.dry_run,
        categories_to_organize=categories_to_organize,
        restricted_dirs=restricted_dirs
    )

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    main()