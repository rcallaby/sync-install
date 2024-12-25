#!/bin/bash

# File containing the list of programs
PROGRAMS_FILE="programs.txt"

# Function to check if a program is installed
is_installed() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install a program
install_program() {
    echo "Installing $1..."
    sudo apt update && sudo apt install -y "$1"
}

# Check if the programs file exists
if [[ ! -f "$PROGRAMS_FILE" ]]; then
    echo "Error: File '$PROGRAMS_FILE' not found."
    exit 1
fi

# Read the file line by line
while IFS= read -r PROGRAM || [[ -n "$PROGRAM" ]]; do
    # Skip empty lines and comments
    [[ -z "$PROGRAM" || "$PROGRAM" =~ ^# ]] && continue

    if is_installed "$PROGRAM"; then
        echo "$PROGRAM is already installed."
    else
        echo "$PROGRAM is not installed."
        install_program "$PROGRAM"
    fi
done < "$PROGRAMS_FILE"
