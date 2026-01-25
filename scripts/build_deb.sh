#!/bin/bash
set -e

APP_NAME="fakelingoes"
VERSION="0.0.2"
ARCH="amd64"
BUILD_DIR="build_deb"
DIST_DIR="dist/Fake Lingoes"
DEB_NAME="Installer/${APP_NAME}_${VERSION}_${ARCH}.deb"

echo "=== Building FakeLingoes Debian Package ==="

# 1. Clean previous build
echo "Cleaning up..."
rm -rf "$BUILD_DIR"
rm -f "$DEB_NAME"

# 2. Run PyInstaller (if dist doesn't exist or forced)
if [ ! -d "$DIST_DIR" ]; then
    echo "Running PyInstaller..."
    ./venv_linux/bin/pyinstaller --clean FakeLingoes.spec
else
    echo "PyInstaller build found. Skipping rebuild to save time."
    echo "Run './venv_linux/bin/pyinstaller --clean FakeLingoes.spec' manually if you changed code."
fi

# 3. Create Debian structure
echo "Creating directory structure..."
mkdir -p "$BUILD_DIR/DEBIAN"
mkdir -p "$BUILD_DIR/opt/$APP_NAME"
mkdir -p "$BUILD_DIR/usr/share/applications"
mkdir -p "$BUILD_DIR/usr/share/icons/hicolor/256x256/apps"

# 4. Copy Application Files
echo "Copying application files..."
# PyInstaller onefile mode creates a single executable
cp "$DIST_DIR" "$BUILD_DIR/opt/$APP_NAME/"

# 5. Create Desktop Entry
echo "Creating .desktop file..."
cat > "$BUILD_DIR/usr/share/applications/$APP_NAME.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Fake Lingoes
Comment=A simple dictionary and translation tool
Exec=/opt/$APP_NAME/Fake\ Lingoes
Icon=$APP_NAME
Terminal=false
Categories=Utility;Education;
StartupNotify=true
EOF

# 6. Convert and Install Icon
echo "Converting icon..."
# Use python to convert ico to png (requires pillow)
source venv_linux/bin/activate
python3 -c "from PIL import Image; img = Image.open('icon.ico'); img.save('$BUILD_DIR/usr/share/icons/hicolor/256x256/apps/$APP_NAME.png')"

# 7. Create Control File
echo "Creating control file..."
INSTALL_SIZE=$(du -s "$BUILD_DIR/opt/$APP_NAME" | cut -f1)
cat > "$BUILD_DIR/DEBIAN/control" << EOF
Package: $APP_NAME
Version: $VERSION
Section: utils
Priority: optional
Architecture: $ARCH
Maintainer: Nam Trung <namtrung@example.com>
Depends: libxcb-cursor0, libappindicator3-1 | libayatana-appindicator3-1
Installed-Size: $INSTALL_SIZE
Description: Fake Lingoes Dictionary
 A Python-based dictionary and translation application 
 with screen capture translation and text-to-speech capabilities.
EOF

# 8. Build Deb
echo "Building .deb package..."
dpkg-deb --build "$BUILD_DIR" "$DEB_NAME"

echo "=== Success! ==="
echo "Package built at: $DEB_NAME"
echo "Install with: sudo apt install ./$DEB_NAME"
