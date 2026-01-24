$ErrorActionPreference = "Stop"

# Define paths
$currentDir = Get-Location
$issFilePath = Join-Path $currentDir "Installer\installer.iss"
$specFilePath = Join-Path $currentDir "FakeLingoes.spec"

# 1. Run PyInstaller
Write-Host "--- Step 1: Running PyInstaller ---" -ForegroundColor Cyan

$pyinstallerPath = ""
$localVenvPath = Join-Path $currentDir "venv\Scripts\pyinstaller.exe"

if (Get-Command pyinstaller -ErrorAction SilentlyContinue) {
    $pyinstallerPath = "pyinstaller"
} elseif (Test-Path $localVenvPath) {
    Write-Host "Found PyInstaller in local venv: $localVenvPath" -ForegroundColor Yellow
    $pyinstallerPath = $localVenvPath
}

if ($pyinstallerPath) {
    & $pyinstallerPath --noconfirm "$specFilePath"
} else {
    Write-Error "PyInstaller not found in PATH or 'venv\Scripts'. Please install it using 'pip install pyinstaller'."
}

# 2. Check for ISCC.exe
Write-Host "`n--- Step 2: Running Inno Setup ---" -ForegroundColor Cyan
$iscc = ""

$potentialPaths = @(
    (Join-Path $currentDir "Installer\InnoSetup\ISCC.exe"),
    "C:\Program Files (x86)\Inno Setup 6\ISCC.exe",
    "C:\Program Files\Inno Setup 6\ISCC.exe",
    "C:\Program Files (x86)\Inno Setup 5\ISCC.exe",
    "C:\Program Files\Inno Setup 5\ISCC.exe"
)

foreach ($path in $potentialPaths) {
    if (Test-Path $path) {
        $iscc = $path
        break
    }
}

if (-not $iscc) {
    # Try finding it in PATH
    $isccCmd = Get-Command "ISCC.exe" -ErrorAction SilentlyContinue
    if ($isccCmd) {
        $iscc = $isccCmd.Source
    }
}

if (-not $iscc) {
    Write-Error "Inno Setup Compiler (ISCC.exe) not found. Please install Inno Setup or add it to your PATH."
}

# 3. Run Inno Setup
Write-Host "Compiling installer using: $iscc"
& $iscc "$issFilePath"

Write-Host "`nBuild complete! Check the 'installer_output' directory." -ForegroundColor Green
