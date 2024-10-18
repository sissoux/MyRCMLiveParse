#!/bin/bash

# Check if python3-venv is installed
if ! dpkg -s python3-venv > /dev/null 2>&1; then
    echo "python3-venv is not installed. Installing it now..."
    sudo apt update
    sudo apt install python3-venv -y
fi

# Create a virtual environment named venv1
echo "Creating virtual environment 'venv1'..."
python3 -m venv venv1

# Activate the virtual environment
echo "Activating the virtual environment..."
source venv1/bin/activate

# Check if the requirements.txt file exists
if [ -f "requirements.txt" ]; then
    echo "Installing dependencies from requirements.txt..."
    pip install -r requirements.txt
else
    echo "requirements.txt not found. Please make sure it is in the current directory."
fi

# Virtual environment activated, now stay in the shell with it
echo "Virtual environment 'venv1' is activated. You can now use it."
