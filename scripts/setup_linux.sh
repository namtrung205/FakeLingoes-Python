#!/bin/bash
set -e

# Update and install system dependencies
echo "Updating package list..."
sudo apt update || echo "Warning: apt update returned errors, but attempting to proceed..."

echo "Installing build tools..."
sudo apt install -y pkg-config build-essential python3-dev

echo "Installing system dependencies..."
# Added libxcb-cursor0 which is often required by newer PyQt5/Qt5 versions
sudo apt install -y tesseract-ocr libasound2-dev espeak scrot python3-pip python3-venv \
    libxcb-xinerama0 libxkbcommon-x11-0 libdbus-1-3 libxcb-icccm4 libxcb-image0 \
    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xfixes0 \
    libxcb-shape0 libxcb-shm0 libxcb-sync1 libxcb-xkb1 libxcb-render0 \
    libxcb-cursor0 libx11-xcb1 \
    libfontconfig1 libfreetype6 libxfixes3 libxi6 libxrender1 \
    libsm6 libice6 libgl1 \
    libgirepository1.0-dev libcairo2-dev \
    gir1.2-gstreamer-1.0 gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-tools

# Create virtual environment if it doesn't exist
if [ ! -d "venv_linux/bin" ]; then
    echo "Creating virtual environment for Linux..."
    python3 -m venv venv_linux
fi

# Activate venv and install python dependencies
source venv_linux/bin/activate
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p Tempfile Capture

echo "Setup complete! Run the app using: source venv_linux/bin/activate && python src/fake_lingoes/main.py"
