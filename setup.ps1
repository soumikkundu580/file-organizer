# File Organizer Setup Script for Windows PowerShell

Write-Host "=================================================="
Write-Host "File Organizer Installation for Windows"
Write-Host "=================================================="
Write-Host ""

# Check if running as administrator
$isAdmin = ([System.Security.Principal.WindowsIdentity]::GetCurrent().Groups -match "S-1-5-32-544") -ne $null

if (-not $isAdmin) {
    Write-Host "Warning: This script should ideally run as Administrator."
    Write-Host "Some features may not work correctly without admin privileges."
    Write-Host ""
}

# Check if Python is installed
$pythonPath = (Get-Command python -ErrorAction SilentlyContinue).Source
$python3Path = (Get-Command python3 -ErrorAction SilentlyContinue).Source

if ($pythonPath) {
    $pythonExe = "python"
    Write-Host "Python found: $(python --version)"
} elseif ($python3Path) {
    $pythonExe = "python3"
    Write-Host "Python 3 found: $(python3 --version)"
} else {
    Write-Host "Error: Python is not installed or not in PATH"
    Write-Host "Please install Python 3.6+ from https://www.python.org"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    exit 1
}

Write-Host ""

# Get the script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$organizePy = Join-Path $scriptDir "organize.py"
$installDir = Join-Path $env:LOCALAPPDATA "Programs\file-organizer"
$binDir = Join-Path $env:LOCALAPPDATA "bin"

# Check if organize.py exists
if (-not (Test-Path $organizePy)) {
    Write-Host "Error: organize.py not found in $scriptDir"
    exit 1
}

# Create installation directories
if (-not (Test-Path $installDir)) {
    Write-Host "Creating directory: $installDir"
    New-Item -ItemType Directory -Path $installDir -Force | Out-Null
}

if (-not (Test-Path $binDir)) {
    Write-Host "Creating directory: $binDir"
    New-Item -ItemType Directory -Path $binDir -Force | Out-Null
}

# Copy organize.py to installation directory
Write-Host "Copying organize.py to installation directory..."
Copy-Item $organizePy $installDir -Force

# Create batch file wrapper
$batchFile = Join-Path $binDir "organize.bat"
Write-Host "Creating organize command batch file..."

$batchContent = "@echo off`n"
$batchContent += "$pythonExe `"$installDir\organize.py`" %*`n"

Set-Content -Path $batchFile -Value $batchContent -Encoding ASCII

Write-Host ""

# Check if binDir is in PATH
$pathEnv = [Environment]::GetEnvironmentVariable("Path", "User")
if ($pathEnv -like "*$binDir*") {
    Write-Host "Installation completed successfully!"
    Write-Host ""
} else {
    Write-Host "Adding to PATH..."
    $newPath = "$binDir;$pathEnv"
    [Environment]::SetEnvironmentVariable("Path", $newPath, "User")
    Write-Host "Installation completed successfully!"
    Write-Host ""
    Write-Host "Important: Restart PowerShell or any terminal for PATH changes to take effect"
}

Write-Host ""
Write-Host "=================================================="
Write-Host "Installation Summary"
Write-Host "=================================================="
Write-Host "Installation directory: $installDir"
Write-Host "Command location: $batchFile"
Write-Host "Bin directory added to PATH: $binDir"
Write-Host ""
Write-Host "To use the file organizer, run:"
Write-Host "  organize"
Write-Host ""
Write-Host "For help, run:"
Write-Host "  organize --help"
Write-Host ""
Write-Host "Or directly with Python:"
Write-Host "  python organize.py --path C:\Users\YourUsername\Downloads"
Write-Host "=================================================="

# Refresh PATH for current session
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
