#!/bin/bash

# Update and install system dependencies
echo "Installing system dependencies..."
sudo apt update
sudo apt install -y tesseract-ocr libasound2-dev espeak scrot python3-pip python3-venv

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate venv and install python dependencies
source venv/bin/activate
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create necessary directories
mkdir -p Tempfile Capture

echo "Setup complete! Run the app using: source venv/bin/activate && python src/fake_lingoes/main.py"
