"""
File Organizer Configuration
Contains file type mappings and protected directories.
"""

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
    # Version control
    ".git", ".svn", ".hg",

    # Python
    "__pycache__", ".venv", "venv",
    ".mypy_cache", ".pytest_cache",
    ".tox", ".ruff_cache",

    # Node.js
    "node_modules", ".npm", ".yarn",
    ".pnpm-store", ".next", ".nuxt",

    # User config/cache
    ".config", ".cache", ".local",
    ".mozilla", ".thunderbird",

    # Flatpak/Snap
    "snap", ".var", "flatpak",

    # System directories
    "proc", "sys", "dev", "run",
    "boot", "etc", "lib", "lib64",
    "bin", "sbin", "usr", "var",

    # Package managers
    ".cargo", ".rustup",
    ".gradle", ".m2",
    ".composer",

    # Cloud/storage
    ".aws", ".azure",
    ".gcloud",

    # IDEs
    ".idea", ".vscode",

    # Containers
    ".docker",

    # Virtual machines
    ".vagrant",

    # Environment files
    ".env",

    # Temporary
    "tmp", ".tmp"
}

HISTORY_FILE = ".organize_history"