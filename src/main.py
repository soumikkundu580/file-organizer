"""
File Organizer Main Entry Point
Handles command line interface and application flow.
"""

import sys
import argparse
from pathlib import Path
# Add the src directory to sys.path to allow imports from utils and config
sys.path.insert(0, str(Path(__file__).parent))

from utils import (
    load_history,
    save_history,
    add_history_entry,
    display_history,
    undo_operations,
    get_file_category,
    format_size,
    get_unique_destination,
    should_skip,
    is_protected_directory,
    collect_files_by_category,
    prompt_for_permission,
    prompt_for_restricted_dirs,
    prompt_for_dry_run,
    prompt_for_recursive,
    organize_folder
)
from config import FILE_TYPES, SYSTEM_PROTECTED_DIRS, HISTORY_FILE


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="File Organizer - Automatically organize files into categories",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument(
        "--path",
        type=str,
        default=None,
        help="Folder path to organize (interactive if not provided)"
    )

    parser.add_argument(
        "--skip-menus",
        action="store_true",
        help="Skip initial menu and go straight to configuration prompts"
    )

    parser.add_argument(
        "--history",
        action="store_true",
        help="View organization history for a folder"
    )

    parser.add_argument(
        "--undo",
        type=int,
        nargs='?',
        const=1,
        metavar="COUNT",
        help="Undo the last N organization operations (default: 1)"
    )

    return parser.parse_args()


def print_header():
    """Print application header."""
    print("\n" + "="*70)
    print("FILE ORGANIZER - INTERACTIVE MODE")
    print("="*70)


def get_target_path() -> Path:
    """Get target path from user input."""
    while True:
        default_path = Path.home() / "Downloads"
        prompt = f"\nEnter folder path (or press Enter for {default_path}): "
        path_input = input(prompt).strip()

        if not path_input:
            target = default_path
        else:
            target = Path(path_input).expanduser()

        if target.exists() and target.is_dir():
            print(f"[OK] Target folder selected: {target}")
            return target
        else:
            print(f"[ERROR] Path does not exist or is not a directory: {target}")


def display_configuration(target_folder: Path, dry_run: bool, recursive: bool, restricted_dirs: set):
    """Display the current configuration."""
    print("\n" + "="*70)
    print("CONFIGURATION SUMMARY")
    print("="*70)
    print(f"Target Folder: {target_folder}")
    recursive_status = "ENABLED" if recursive else "DISABLED"
    dry_run_status = "ENABLED" if dry_run else "DISABLED"
    print(f"Recursive Mode: {recursive_status}")
    print(f"Dry-Run Mode: {dry_run_status}")
    if restricted_dirs:
        print(f"Restricted Dirs: {', '.join(restricted_dirs)}")
    else:
        print(f"Restricted Dirs: None")
    print("="*70)


def main():
    """Main entry point with interactive CLI."""
    print_header()

    args = parse_arguments()

    # Step 0: Handle special commands (history and undo)
    if args.path:
        target_folder = Path(args.path).expanduser()
        if not target_folder.exists() or not target_folder.is_dir():
            print(f"\n[ERROR] Invalid path: {target_folder}")
            return
    else:
        target_folder = get_target_path()

    # Handle --history flag
    if args.history:
        display_history(target_folder)
        return

    # Handle --undo flag
    if args.undo is not None:
        undo_operations(target_folder, args.undo)
        return

    # Step 1: Get target folder (already done above)

    # Step 2: Ask for dry-run mode
    dry_run = prompt_for_dry_run()

    # Step 3: Ask for recursive mode
    recursive = prompt_for_recursive()

    # Step 4: Ask for restricted directories
    print("\n" + "="*70)
    restrict_prompt = input("Do you want to restrict any directories? (yes/no): ").strip().lower()
    restricted_dirs = set()
    if restrict_prompt in ["yes", "y"]:
        restricted_dirs = prompt_for_restricted_dirs()

    # Step 5: Show configuration summary
    display_configuration(target_folder, dry_run, recursive, restricted_dirs)

    # Step 6: Collect and preview files
    files_by_category = collect_files_by_category(
        target_folder,
        recursive,
        set(FILE_TYPES.keys()),
        restricted_dirs
    )

    # Step 7: Ask for final confirmation
    categories_to_organize = prompt_for_permission(files_by_category, dry_run=dry_run)

    if not categories_to_organize:
        print("\n[CANCELLED] Operation cancelled.")
        return

    # Step 8: Organize files
    organize_folder(
        target_folder=target_folder,
        recursive=recursive,
        dry_run=dry_run,
        categories_to_organize=categories_to_organize,
        restricted_dirs=restricted_dirs
    )

    print()


if __name__ == "__main__":
    main()