# File Organizer

A lightweight, fast, and safe command-line tool to organize files into categories. Works on Linux, Windows, and Android (Termux).

## Features

- **Safe & Non-Intrusive**: Never touches system config files, app configurations, or protected directories
- **Smart Recursive Organization**: In recursive mode, creates category folders within each subdirectory (not just at root)
- **Directory Restriction**: Exclude specific directories from organization
- **File Type Categories**: Automatically organizes files into:
  - Pictures (images, photos, graphics)
  - Videos (all video formats)
  - Music (audio files)
  - Documents (PDFs, Word docs, sheets)
  - Archives (compressed files)
  - Code (source code, scripts)
  - Databases (DB files)
  - Executables (binaries, installers)
  - Fonts (font files)
  - 3D Models (3D asset files)
  - Config Files (configuration)
  - Logs (log files)
  - Scripts (shell scripts)
  - Disk Images (ISO, IMG, DMG)
  - Data Science (notebooks, datasets)
  - GIS & Maps (spatial data)
  - Others (unrecognized types)

- **Permission-Based**: Shows all files to organize and asks for permission before moving anything
- **Dry-Run Mode**: Preview what will be moved without actually moving files
- **Plain CLI Interface**: Clean, simple text output (no colors, no emojis)
- **Duplicate Handling**: Automatically renames duplicates with counters
- **Error Handling**: Gracefully handles errors and reports them

## System Requirements

- **Linux**: Python 3.6+
- **Windows**: Python 3.6+ (or use standalone installer)
- **Android/Termux**: Python 3.8+ via Termux

---

## Installation

### Linux

#### Method 1: Automatic Setup (Recommended)

```bash
git clone https://github.com/soumikkundu580/file-organizer.git
cd file-organizer
bash setup.sh
```

Add to your shell profile (~/.bashrc, ~/.zshrc, or ~/.profile):
```bash
export PATH="$HOME/.local/bin:$PATH"
```

Then reload your shell:
```bash
source ~/.bashrc  # or ~/.zshrc or ~/.profile
```

#### Method 2: Manual Setup

```bash
# Clone or download the repository
cd ~/file-organizer

# Make scripts executable
chmod +x organize.py
chmod +x setup.sh

# Run setup
bash setup.sh
```

#### Method 3: Direct Usage (No Installation)

```bash
python3 organize.py --path /path/to/folder
```

---

### Windows

#### Method 1: Automatic Setup with PowerShell (Recommended)

1. **Download or Clone** the repository to a folder (e.g., `C:\file-organizer`)

2. **Open PowerShell as Administrator** and run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

3. **Run the setup script**:

```powershell
cd C:\file-organizer
.\setup.ps1
```

4. **Add to PATH** (if not done automatically):
   - Search for "Environment Variables" in Start Menu
   - Click "Edit environment variables for your account"
   - Under "User variables", click "Path" and add: `C:\Users\YourUsername\AppData\Local\bin`
   - Click OK and restart PowerShell

#### Method 2: Manual Setup

1. Download/clone the repository

2. Open PowerShell and navigate to the folder:
```powershell
cd C:\file-organizer
```

3. Use directly with Python:
```powershell
python organize.py --path "C:\Users\YourUsername\Downloads"
```

#### Method 3: Create a Batch File Shortcut

Create a file named `organize.bat` in `C:\Windows\System32\`:

```batch
@echo off
python "%USERPROFILE%\AppData\Local\Programs\file-organizer\organize.py" %*
```

---

### Android (Termux)

#### Prerequisites

1. Install **Termux** from F-Droid or Google Play Store

2. Update and install Python:
```bash
pkg update
pkg install python
```

#### Installation Steps

1. **Clone/download repository** into Termux:
```bash
cd ~
git clone https://github.com/soumikkundu580/file-organizer.git
cd file-organizer
```

2. **Make setup executable**:
```bash
chmod +x setup-termux.sh
```

3. **Run the setup**:
```bash
bash setup-termux.sh
```

4. **Reload Termux environment**:
```bash
source ~/.bashrc
```

#### Direct Usage (No Installation)

```bash
python organize.py --path /sdcard/Download
```

**Storage Access**: You may need to grant Termux storage permission:
```bash
termux-setup-storage
```

---

## Usage

### Basic Commands

```bash
# Interactive mode (guides you through all options)
organize

# Organize specific folder (will prompt for options)
organize --path ~/Downloads

# Direct execution with Python
python3 organize.py --path /path/to/folder

# Get help
organize --help
```

### How It Works

The organizer uses **interactive prompts** to guide you through the options:

1. **Dry-Run Mode**: Choose whether to preview changes or actually move files
2. **Recursive Mode**: Choose whether to organize just the folder or all subfolders
3. **Restrict Directories**: Optionally exclude specific directories
4. **Permission Confirmation**: Review files to be organized with a file preview

### Command Options

| Option | Description |
|--------|-------------|
| `--path PATH` | Folder to organize (interactive prompt if not provided) |
| `--skip-menus` | Skip initial menu and go straight to configuration prompts |
| `--help` | Show help message |

### Examples

**Organize Downloads folder:**
```bash
organize --path ~/Downloads
```
You'll be guided through interactive prompts to choose:
- Dry-run mode (preview only or actually move)
- Recursive mode (this folder or all subfolders)
- Restricted directories (optional)

**Direct Python execution:**
```bash
python3 organize.py --path ~/Documents
```

**Using the installed command:**
```bash
# After running setup.sh (Linux/Termux) or setup.ps1 (Windows)
organize
```

---

## How It Works

### Standard Mode (Non-Recursive)
- Scans only the top-level of the target directory
- Creates category folders at the target location
- Moves matching files into category folders

### Recursive Mode
- Scans all subdirectories
- Creates category folders **inside each subdirectory** (not at root)
- Preserves folder structure while organizing files
- Skips already-organized folders to prevent re-organization

### Permission System
- Shows a summary of all files grouped by category
- Displays sample filenames for each category
- Asks for permission before moving any files
- Can be skipped with `--no-prompt` flag

### Protection Features
- **System Config Protection**: Never touches `.git`, `.config`, `node_modules`, `.venv`, etc.
- **Hidden Files**: Ignores dotfiles (files starting with `.`)
- **Already Organized Folders**: Skips files already in category folders
- **Directory Restriction**: Excludes user-specified directories

---

## Protected System Directories

The organizer will never touch these directories:

```
.git          .svn          .hg
node_modules  .npm          .venv
venv          .env          __pycache__
.cache        .local        .config
.aws          snap          flatpak
```

---

## Troubleshooting

### "organize: command not found"

**Linux/Termux:**
```bash
export PATH="$HOME/.local/bin:$PATH"
source ~/.bashrc
```

Then add the export line to your shell profile permanently.

**Windows:**
- Ensure Python is installed and in PATH
- Try using `python organize.py` directly
- Check that `C:\Users\YourUsername\AppData\Local\bin` is in System PATH

### Permission Denied (Linux/Termux)

```bash
chmod +x organize.py
chmod +x setup.sh
bash setup.sh
```

### Python Not Found

**Linux:**
```bash
sudo apt-get install python3
```

**Windows:**
- Download from [python.org](https://www.python.org)
- Make sure "Add Python to PATH" is checked during installation

**Android (Termux):**
```bash
pkg install python
```

### Cannot Access Storage (Android)

```bash
termux-setup-storage
```

Then grant storage permission when prompted.

### Dry-Run Shows Files But They Don't Move

This is expected! Use `--dry-run` to preview. Remove the flag to actually move files:

```bash
organize --path ~/Downloads --dry-run   # Preview only
organize --path ~/Downloads             # Actually move files
```

---

## Uninstallation

### Linux

```bash
rm ~/.local/bin/organize
```

### Windows

Remove from PATH:
1. Search "Environment Variables"
2. Remove the installation directory from PATH
3. Delete the batch file from `C:\Windows\System32\` if created

### Android (Termux)

```bash
rm ~/.local/bin/organize
rm -rf ~/file-organizer
```

---

## File Type Extensions

### Pictures
`.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`, `.svg`, `.bmp`, `.tiff`, `.ico`, `.heic`, `.heif`, `.raw`, `.cr2`, `.nef`, `.arw`, `.dng`, `.psd`, `.ai`, `.eps`, `.indd`, `.xcf`

### Videos
`.mp4`, `.mkv`, `.mov`, `.avi`, `.webm`, `.flv`, `.wmv`, `.mpeg`, `.mpg`, `.3gp`, `.m4v`, `.ts`, `.vob`, `.ogv`

### Music
`.mp3`, `.wav`, `.flac`, `.ogg`, `.aac`, `.m4a`, `.wma`, `.alac`, `.aiff`, `.mid`, `.midi`, `.opus`

### Documents
`.pdf`, `.doc`, `.docx`, `.txt`, `.ppt`, `.pptx`, `.xls`, `.xlsx`, `.csv`, `.md`, `.rtf`, `.odt`, `.ods`, `.odp`, `.tex`, `.epub`, `.pages`

### Archives
`.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`, `.xz`, `.iso`, `.cab`, `.tgz`

### Code
`.py`, `.js`, `.ts`, `.jsx`, `.tsx`, `.cpp`, `.c`, `.h`, `.hpp`, `.java`, `.kt`, `.rs`, `.go`, `.php`, `.rb`, `.swift`, `.cs`, `.sh`, `.bat`, `.ps1`, `.html`, `.css`, `.scss`, `.sql`, `.json`, `.xml`, `.yaml`, `.yml`, `.vue`, `.dart`, `.lua`

### And more...
See the complete list in [organize.py](organize.py) under `FILE_TYPES` dictionary.

---

## Development

To contribute or modify the organizer:

1. Fork or clone the repository
2. Make your changes to `organize.py`
3. Test: `python3 organize.py --path /test/folder` and follow interactive prompts
4. For testing without moving files, select "yes" for dry-run mode when prompted
5. Submit improvements

---

## License

This project is free to use and modify.

## Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Verify Python version: `python3 --version` (needs 3.6+)
3. Test with `--dry-run` first to ensure it works as expected

---

## Notes

- **No External Dependencies**: Uses only Python standard library
- **No System Changes**: Does not modify system files or application configs
- **No Color Output**: Plain CLI text for better terminal compatibility
- **Safe by Default**: Always asks for permission before moving files
- **Cross-Platform**: Same functionality on Linux, Windows, and Android

Happy organizing!
