#!/bin/bash

# Update and install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y tesseract-ocr libasound2-dev espeak scrot python3-pip python3-venv \
    libxcb-xinerama0 libxkbcommon-x11-0 libdbus-1-3 libxcb-icccm4 libxcb-image0 \
    libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xfixes0

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
