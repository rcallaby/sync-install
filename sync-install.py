import os
import subprocess
import sys

# File containing the list of programs
PROGRAMS_FILE = "programs.txt"

def is_installed(program):
    """Check if a program is installed."""
    return subprocess.call(['which', program], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

def install_program(program):
    """Install a program using apt."""
    print(f"Installing {program}...")
    subprocess.run(['sudo', 'apt', 'update'], check=True)
    subprocess.run(['sudo', 'apt', 'install', '-y', program], check=True)

def main():
    # Check if the programs file exists
    if not os.path.isfile(PROGRAMS_FILE):
        print(f"Error: File '{PROGRAMS_FILE}' not found.")
        sys.exit(1)

    # Read the file line by line
    with open(PROGRAMS_FILE, 'r') as file:
        for line in file:
            program = line.strip()
            
            # Skip empty lines and comments
            if not program or program.startswith('#'):
                continue

            if is_installed(program):
                print(f"{program} is already installed.")
            else:
                print(f"{program} is not installed.")
                try:
                    install_program(program)
                except subprocess.CalledProcessError as e:
                    print(f"Error installing {program}: {e}")

if __name__ == "__main__":
    main()
