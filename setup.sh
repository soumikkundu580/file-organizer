#!/bin/bash

# File Organizer Setup Script for Linux
# This script installs the file organizer and makes it accessible as 'organize' command

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ORGANIZE_PY="$SCRIPT_DIR/src/main.py"
INSTALL_DIR="$HOME/.local/bin"
ORGANIZE_CMD="$INSTALL_DIR/organize"

echo "=================================================="
echo "File Organizer Installation"
echo "=================================================="

# Check if organize.py exists
if [ ! -f "$ORGANIZE_PY" ]; then
    echo "Error: src/main.py not found in $SCRIPT_DIR"
    exit 1
fi

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

echo "Python 3 found: $(python3 --version)"

# Create .local/bin directory if it doesn't exist
if [ ! -d "$INSTALL_DIR" ]; then
    echo "Creating directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
fi

# Make organize.py executable
echo "Making src/main.py executable..."
chmod +x "$ORGANIZE_PY"

# Create the organize command wrapper with absolute path
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
    echo "Add this line to your shell profile (~/.bashrc, ~/.zshrc, etc):"
    echo "  export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "Then run: source ~/.bashrc (or ~/.zshrc)"
fi

echo ""
echo "=================================================="
echo "Installation Summary"
echo "=================================================="
echo "Organize script location: $ORGANIZE_CMD"
echo "Original script: $ORGANIZE_PY"
echo ""
echo "To use the file organizer, run:"
echo "  organize"
echo ""
echo "For help, run:"
echo "  organize --help"
echo "=================================================="