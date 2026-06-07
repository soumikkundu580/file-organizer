"""
File Organizer Utility Functions
Contains all the core logic for file organization.
"""

from pathlib import Path
import shutil
from collections import defaultdict
import json
from datetime import datetime
from config import FILE_TYPES, SYSTEM_PROTECTED_DIRS, HISTORY_FILE


def get_history_file(target_folder: Path) -> Path:
    """Get path to history file in target folder."""
    return target_folder / HISTORY_FILE


def load_history(target_folder: Path) -> list:
    """Load organization history from file."""
    history_file = get_history_file(target_folder)
    if not history_file.exists():
        return []
    try:
        with open(history_file, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return []


def save_history(target_folder: Path, history: list):
    """Save organization history to file."""
    history_file = get_history_file(target_folder)
    try:
        with open(history_file, 'w') as f:
            json.dump(history, f, indent=2)
    except IOError as e:
        print(f"[WARNING] Could not save history: {e}")


def add_history_entry(target_folder: Path, from_path: str, to_path: str, operation: str = "move"):
    """Add an entry to the history log."""
    history = load_history(target_folder)
    entry = {
        "timestamp": datetime.now().isoformat(),
        "operation": operation,
        "from": from_path,
        "to": to_path
    }
    history.append(entry)
    save_history(target_folder, history)


def display_history(target_folder: Path):
    """Display the organization history."""
    history = load_history(target_folder)

    if not history:
        print("\n[INFO] No organization history found.")
        return

    print("\n" + "="*70)
    print("ORGANIZATION HISTORY")
    print("="*70)

    for idx, entry in enumerate(history, 1):
        timestamp = entry.get("timestamp", "Unknown")
        from_file = entry.get("from", "Unknown")
        to_file = entry.get("to", "Unknown")
        print(f"\n[{idx}] {timestamp}")
        print(f"    From: {from_file}")
        print(f"    To:   {to_file}")

    print("\n" + "="*70)
    print(f"Total operations: {len(history)}")
    print("="*70)


def undo_operations(target_folder: Path, count: int = 1) -> int:
    """Undo the last N organization operations."""
    history = load_history(target_folder)

    if not history:
        print("\n[INFO] No history to undo.")
        return 0

    count = min(count, len(history))
    operations_to_undo = history[-count:]

    print("\n" + "="*70)
    print("UNDO OPERATIONS")
    print("="*70)
    print(f"Will undo last {count} operation(s):")

    for idx, entry in enumerate(operations_to_undo, 1):
        from_file = entry.get("from", "Unknown")
        to_file = entry.get("to", "Unknown")
        print(f"  [{idx}] {to_file} -> {from_file}")

    print("="*70)

    while True:
        response = input("\nProceed with undo? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            break
        elif response in ["no", "n"]:
            print("[CANCELLED] Undo cancelled.")
            return 0
        else:
            print("[WARNING] Please enter 'yes' or 'no'.")

    reverted_count = 0
    failed_count = 0

    for entry in operations_to_undo:
        try:
            original_path = Path(entry.get("from"))
            current_path = Path(entry.get("to"))

            if current_path.exists():
                original_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(current_path), str(original_path))
                print(f"[OK] Reverted: {current_path.name} -> {original_path.parent.name}/")
                reverted_count += 1
            else:
                print(f"[WARNING] File not found: {current_path}")
                failed_count += 1
        except Exception as e:
            print(f"[ERROR] Failed to revert {entry.get('to')}: {str(e)}")
            failed_count += 1

    # Remove reverted operations from history
    history = history[:-count]
    save_history(target_folder, history)

    print("\n" + "="*70)
    print("UNDO SUMMARY")
    print("="*70)
    print(f"[OK] Reverted: {reverted_count} operations")
    if failed_count > 0:
        print(f"[ERROR] Failed: {failed_count}")
    print("="*70)

    return reverted_count


def get_file_category(extension: str) -> str:
    """Get file category based on extension."""
    extension = extension.lower()
    for category, extensions in FILE_TYPES.items():
        if extension in extensions:
            return category
    return "Others"


def format_size(size: int) -> str:
    """Format file size in human-readable format."""
    units = ["B", "KB", "MB", "GB", "TB"]
    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"


def get_unique_destination(destination: Path) -> Path:
    """Get unique destination path if file already exists."""
    if not destination.exists():
        return destination

    counter = 1
    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name
        if not new_destination.exists():
            return new_destination
        counter += 1


def should_skip(item: Path, organized_folders: set) -> bool:
    """Skip dotfiles, files in organized folders, and protected directories."""
    if item.name.startswith("."):
        return True

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

            if any(is_protected_directory(p, restricted_dirs) for p in item.parents):
                continue

            extension = item.suffix.lower()
            category = get_file_category(extension)
            rel_path = item.relative_to(target_folder)
            files_by_category[category].append((item, str(rel_path)))

        except Exception:
            pass

    return files_by_category


def prompt_for_permission(files_by_category: dict, dry_run: bool = False) -> set:
    """Ask user for permission to organize file types."""
    if not files_by_category:
        print("\n[WARNING] No files to organize found.")
        return set()

    print("\n" + "="*70)
    print("FILE ORGANIZATION SUMMARY")
    print("="*70)

    total_files = 0
    for category in sorted(files_by_category.keys()):
        files = files_by_category[category]
        total_files += len(files)
        print(f"\n[{category}]: ({len(files)} files)")
        for _, rel_path in files[:3]:
            print(f"   |-- {rel_path}")
        if len(files) > 3:
            print(f"   |-- ... and {len(files) - 3} more files")

    print("\n" + "="*70)
    print(f"Total: {total_files} files to organize")

    if dry_run:
        print("[DRY-RUN MODE] Preview only, no files will be moved")
    print("="*70)

    while True:
        response = input("\nProceed with organization? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            return set(files_by_category.keys())
        elif response in ["no", "n"]:
            print("[CANCELLED] Operation cancelled.")
            return set()
        else:
            print("[WARNING] Please enter 'yes' or 'no'.")


def prompt_for_restricted_dirs() -> set:
    """Ask user for directories to exclude from organization."""
    print("\n" + "="*70)
    print("RESTRICT DIRECTORIES")
    print("="*70)
    print("Enter directory names to exclude from organization.")
    print("Separate multiple directories with commas (or press Enter to skip).")
    print("Example: 'My Projects, Important Docs, Work'")

    response = input("\nRestricted directories: ").strip()

    if not response:
        return set()

    restricted = {d.strip() for d in response.split(",")}
    restricted = {d for d in restricted if d}

    if restricted:
        print(f"[OK] Restricted directories: {', '.join(restricted)}")

    return restricted


def prompt_for_dry_run() -> bool:
    """Ask user if they want to run in dry-run mode."""
    print("\n" + "="*70)
    print("DRY-RUN MODE")
    print("="*70)
    print("In dry-run mode, the script will preview changes without")
    print("actually moving any files. This is useful for testing.")

    while True:
        response = input("\nRun in dry-run mode? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            print("[OK] Dry-run mode ENABLED - No files will be moved")
            return True
        elif response in ["no", "n"]:
            print("[OK] Dry-run mode DISABLED - Files will be moved")
            return False
        else:
            print("[WARNING] Please enter 'yes' or 'no'.")


def prompt_for_recursive() -> bool:
    """Ask user if they want recursive mode."""
    print("\n" + "="*70)
    print("RECURSIVE MODE")
    print("="*70)
    print("Non-recursive: Organize only files in the target folder")
    print("Recursive: Organize files in all subfolders")

    while True:
        response = input("\nOrganize recursively (all subfolders)? (yes/no): ").strip().lower()
        if response in ["yes", "y"]:
            print("[OK] Recursive mode ENABLED - All subfolders will be organized")
            return True
        elif response in ["no", "n"]:
            print("[OK] Recursive mode DISABLED - Only target folder will be organized")
            return False
        else:
            print("[WARNING] Please enter 'yes' or 'no'.")


def organize_folder(
    target_folder: Path,
    recursive: bool = False,
    dry_run: bool = False,
    categories_to_organize: set = None,
    restricted_dirs: set = None
):
    """Organize files into category folders."""
    if not target_folder.exists():
        print(f"\n[ERROR] Folder not found: {target_folder}")
        return

    if restricted_dirs is None:
        restricted_dirs = set()

    if categories_to_organize is None:
        categories_to_organize = set(FILE_TYPES.keys())

    organized_folders = set(FILE_TYPES.keys())

    status = "Scanning" if dry_run else "Processing"
    print(f"\n[{status}]: {target_folder}")
    if recursive:
        print("[MODE] RECURSIVE (organizing in all subdirectories)")
    if dry_run:
        print("[MODE] DRY-RUN (preview only, no files will be moved)")

    moved_count = 0
    error_count = 0
    skipped_count = 0

    if recursive:
        items = list(target_folder.rglob("*"))
        items_to_process = []

        for item in items:
            try:
                if not item.is_file():
                    continue
                if should_skip(item, organized_folders):
                    skipped_count += 1
                    continue
                if any(is_protected_directory(p, restricted_dirs) for p in item.parents):
                    skipped_count += 1
                    continue
                items_to_process.append(item)
            except Exception:
                pass

        by_parent = defaultdict(list)
        for item in items_to_process:
            by_parent[item.parent].append(item)

        for parent_dir, files in by_parent.items():
            for item in files:
                try:
                    extension = item.suffix.lower()
                    category = get_file_category(extension)

                    if category not in categories_to_organize:
                        skipped_count += 1
                        continue

                    destination_folder = parent_dir / category
                    destination_file = destination_folder / item.name
                    destination_file = get_unique_destination(destination_file)

                    size = format_size(item.stat().st_size)

                    if dry_run:
                        rel_path = item.relative_to(target_folder)
                        print(
                            f"[DRY-RUN] {rel_path}\n"
                            f"          -> {category}/ ({size})"
                        )
                        moved_count += 1
                    else:
                        destination_folder.mkdir(exist_ok=True, parents=True)
                        shutil.move(str(item), str(destination_file))
                        add_history_entry(target_folder, str(item), str(destination_file))
                        print(f"[OK] {item.name} -> {category}/ ({size})")
                        moved_count += 1

                except Exception as e:
                    print(f"[ERROR] {item.name} | {str(e)}")
                    error_count += 1

    else:
        items = target_folder.iterdir()

        for item in items:
            try:
                if not item.is_file():
                    continue

                if should_skip(item, organized_folders):
                    skipped_count += 1
                    continue

                if any(is_protected_directory(p, restricted_dirs) for p in item.parents):
                    skipped_count += 1
                    continue

                extension = item.suffix.lower()
                category = get_file_category(extension)

                if category not in categories_to_organize:
                    skipped_count += 1
                    continue

                destination_folder = target_folder / category
                destination_file = destination_folder / item.name
                destination_file = get_unique_destination(destination_file)

                size = format_size(item.stat().st_size)

                if dry_run:
                    print(
                        f"[DRY-RUN] {item.name}\n"
                        f"          -> {category}/ ({size})"
                    )
                    moved_count += 1
                else:
                    destination_folder.mkdir(exist_ok=True)
                    shutil.move(str(item), str(destination_file))
                    add_history_entry(target_folder, str(item), str(destination_file))
                    print(f"[OK] {item.name} -> {category}/ ({size})")
                    moved_count += 1

            except Exception as e:
                print(f"[ERROR] {item.name} | {str(e)}")
                error_count += 1

    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    action = "Would move" if dry_run else "Moved"
    print(f"[OK] {action}: {moved_count} files")
    if skipped_count > 0:
        print(f"[SKIPPED] Skipped: {skipped_count} files")
    if error_count > 0:
        print(f"[ERROR] Errors: {error_count}")
    if dry_run:
        print("\n[INFO] This was a DRY-RUN. Re-run with dry-run disabled to actually organize files.")
    print("="*70)