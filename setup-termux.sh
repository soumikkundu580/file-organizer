#!/bin/bash

# File Organizer Setup Script for Android (Termux)
# This script installs the file organizer for Termux environment

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORGANIZE_PY="$SCRIPT_DIR/organize.py"
INSTALL_DIR="$HOME/.local/bin"
ORGANIZE_CMD="$INSTALL_DIR/organize"

echo "=================================================="
echo "File Organizer Installation for Termux (Android)"
echo "=================================================="

# Check if organize.py exists
if [ ! -f "$ORGANIZE_PY" ]; then
    echo "Error: organize.py not found in $SCRIPT_DIR"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo ""
    echo "Install Python 3 with:"
    echo "  pkg update"
    echo "  pkg install python"
    echo ""
    exit 1
fi

echo "Python 3 found: $(python3 --version)"
echo ""

# Check storage permission
echo "Checking storage access..."
if [ ! -d "$HOME/storage" ]; then
    echo "Warning: Termux storage not configured"
    echo "Run: termux-setup-storage"
    echo "to enable access to device storage"
    echo ""
fi

# Create .local/bin directory if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Creating directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
fi

# Make organize.py executable
echo "Making organize.py executable..."
chmod +x "$ORGANIZE_PY"

# Create the organize command wrapper
echo "Creating organize command..."
cat > "$ORGANIZE_CMD" << EOF
#!/bin/bash
python3 "$ORGANIZE_PY" "\$@"
EOF

chmod +x "$ORGANIZE_CMD"

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" == *":$INSTALL_DIR:"* ]]; then
    echo "Installation completed successfully!"
else
    echo "Warning: $INSTALL_DIR is not in your PATH"
    echo ""
    echo "Add this line to ~/.bashrc:"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
fi

echo ""
echo "=================================================="
echo "Installation Summary"
echo "=================================================="
echo "Organize command: $ORGANIZE_CMD"
echo "Original script: $ORGANIZE_PY"
echo "Home storage: $HOME/storage/downloads"
echo ""
echo "Common Termux Paths:"
echo "  Downloads: $HOME/storage/downloads"
echo "  Documents: $HOME/storage/documents"
echo "  Pictures: $HOME/storage/pictures"
echo "  Home: $HOME"
echo ""
echo "To use the file organizer, run:"
echo "  organize"
echo ""
echo "For help, run:"
echo "  organize --help"
echo ""
echo "Example: Organize Downloads folder"
echo "  organize --path $HOME/storage/downloads"
echo ""
echo "If 'organize' command not found after first restart:"
echo "  1. Reload shell: source ~/.bashrc"
echo "  2. Check PATH: echo \$PATH"
echo "  3. Run directly: python3 organize.py --path ~/storage/downloads"
echo "=================================================="
