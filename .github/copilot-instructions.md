# Copilot Instructions for File Organizer

## Project Overview

File Organizer is a lightweight CLI tool that automatically categorizes and organizes files into type-based folders (Pictures, Videos, Documents, Code, etc.). It's a single-file Python application designed to work across Linux, Windows, and Android (Termux).

**Key characteristics:**
- Single-file application (`organize.py`)
- No external dependencies (standard library only)
- Interactive CLI with permission-based operations
- Cross-platform support (Linux, Windows, Android)
- Safety-focused: always asks for permission, supports dry-run mode

## Running & Testing

### Basic Usage
```bash
# Interactive mode (guided through all prompts)
python3 organize.py

# Direct with options
python3 organize.py --path ~/Downloads --dry-run

# Preview changes without moving files
python3 organize.py --path ~/Downloads --dry-run --skip-menus
```

### Test the Script
```bash
# Test with dry-run in a temporary directory
mkdir -p /tmp/test-organize
cp organize.py /tmp/test-organize/
cd /tmp/test-organize
python3 organize.py --path . --dry-run --skip-menus
```

### Installation (Linux/Termux)
```bash
bash setup.sh
```

## Architecture & Key Components

### Core Data Structures

**FILE_TYPES Dictionary**
- Maps file categories (Pictures, Videos, Music, Documents, Code, etc.) to their file extensions
- 20+ categories covering common file types
- Extensions normalized to lowercase for matching

**SYSTEM_PROTECTED_DIRS Set**
- Contains directory names that should never be touched (.git, node_modules, .venv, etc.)
- Prevents accidental modification of system/development directories

### Processing Flow

1. **Argument Parsing** (`parse_arguments()`)
   - Handles `--path`, `--skip-menus` flags
   - Falls back to interactive mode if no arguments provided

2. **User Interaction** (Interactive prompts)
   - `get_target_path()`: Get folder to organize
   - `prompt_for_dry_run()`: Enable/disable actual file movement
   - `prompt_for_recursive()`: Scan subdirectories or just top level
   - `prompt_for_restricted_dirs()`: Exclude specific directories
   - `prompt_for_permission()`: Final confirmation with file preview

3. **File Collection** (`collect_files_by_category()`)
   - Uses `pathlib.Path` for cross-platform path handling
   - Handles both recursive (`rglob()`) and non-recursive (`iterdir()`) modes
   - Skips protected dirs, dotfiles, and already-organized folders

4. **Organization** (`organize_folder()`)
   - Two separate paths: recursive vs non-recursive
   - For recursive: groups files by parent directory, creates category folders at each level
   - For non-recursive: all files go to category folders in target directory
   - Handles duplicates via `get_unique_destination()` (adds counters)
   - Provides detailed output with file sizes

### Key Design Patterns

**Safety First**
- `should_skip()`: Prevents touching dotfiles and already-organized content
- `is_protected_directory()`: Blocks system/development directories
- Dry-run mode shows all changes before execution
- Permission prompt with file preview before any operations

**Exception Handling**
- Generic `except Exception` blocks in file collection to gracefully skip inaccessible files
- Errors reported but don't halt entire operation
- Error count included in summary

**Code Categorization**
- `get_file_category()`: O(1) lookup via extension matching
- Returns "Others" for unrecognized types
- Case-insensitive extension matching

**Recursive vs Non-Recursive**
- Recursive: Categories created in *each subdirectory* (preserves structure)
- Non-recursive: All categories created at target root
- Tracked via `items_by_parent` dict for recursive mode

## Code Conventions

### Function Organization
- Utility functions first (categorization, formatting, protection checks)
- User interaction functions mid-file
- Core logic (`organize_folder()`) near end
- `main()` entry point at bottom

### Type Hints
- Function parameters include type hints (e.g., `extension: str`, `recursive: bool`)
- Return types specified (e.g., `-> Path`, `-> dict`)

### String Formatting
- Status messages use `[STATUS]` prefixes: `[OK]`, `[ERROR]`, `[WARNING]`, `[DRY-RUN]`, `[INFO]`
- Use `"="*70` for visual separators
- Plain text output only (no colors/emojis)
- Structured layout: headers, content, separators

### Path Handling
- Always use `pathlib.Path` (not string paths)
- Use `.expanduser()` to resolve `~`
- Use `.relative_to()` for display paths
- Use `.rglob()` for recursive, `.iterdir()` for non-recursive

### Variable Naming
- Counters: `moved_count`, `error_count`, `skipped_count`
- Collections: `files_by_category`, `restricted_dirs`, `organized_folders`, `items_to_process`
- Dictionary grouping: `by_parent` (group by parent directory)

### Constants
- All-caps for module-level constants: `FILE_TYPES`, `SYSTEM_PROTECTED_DIRS`

## When Modifying

### Adding New File Type Categories
1. Add entry to `FILE_TYPES` dictionary with category name and extension list
2. Category automatically available in organization flow
3. Test with `--dry-run` first

### Changing Safety Rules
- Modify `SYSTEM_PROTECTED_DIRS` to add/remove protected directories
- Update `should_skip()` or `is_protected_directory()` for new protection logic
- Always test thoroughly with test folders

### Adding New CLI Flags
1. Add to `parse_arguments()` with `parser.add_argument()`
2. Add corresponding prompt function if interactive option needed
3. Pass parameter through to `organize_folder()`

### Testing Changes
```bash
# Create test folder
mkdir -p ~/test-org && cd ~/test-org

# Create test files
touch test.txt test.py image.jpg video.mp4

# Test changes with dry-run first
python3 /path/to/organize.py --path . --dry-run --skip-menus

# Then without dry-run if satisfied
python3 /path/to/organize.py --path . --skip-menus
```

## Cross-Platform Considerations

- Use `pathlib.Path` for all path operations (not `os.path`)
- `shutil.move()` works on all platforms
- Environment variables (`HOME`, `USERPROFILE`) expanded by `Path.expanduser()`
- Test on target platforms: Linux, Windows (PowerShell), Termux (bash)
