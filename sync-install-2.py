import os
import sys
import configparser
import subprocess

# File containing the list of programs
PROGRAMS_FILE = "programs.ini"

# Define commands for supported package managers
PACKAGE_MANAGERS = {
    "apt": {
        "check": ["which"],
        "install": ["sudo", "apt", "install", "-y"],
        "update": ["sudo", "apt", "update"]
    },
    "brew": {
        "check": ["brew", "list"],
        "install": ["brew", "install"],
        "update": ["brew", "update"]
    },
    "dnf": {
        "check": ["which"],
        "install": ["sudo", "dnf", "install", "-y"],
        "update": ["sudo", "dnf", "check-update"]
    },
    "yum": {
        "check": ["which"],
        "install": ["sudo", "yum", "install", "-y"],
        "update": ["sudo", "yum", "check-update"]
    },
    "pacman": {
        "check": ["pacman", "-Q"],
        "install": ["sudo", "pacman", "-S", "--noconfirm"],
        "update": ["sudo", "pacman", "-Sy"]
    }
}

def is_installed(manager, program):
    """Check if a program is installed using the specified package manager."""
    check_cmd = PACKAGE_MANAGERS[manager]["check"]
    try:
        if manager == "brew":
            # Special case: brew uses a list command
            subprocess.run(check_cmd + [program], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        else:
            subprocess.run(check_cmd + [program], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError:
        return False

def install_program(manager, program):
    """Install a program using the specified package manager."""
    print(f"Installing {program} with {manager}...")
    subprocess.run(PACKAGE_MANAGERS[manager]["update"], check=True)
    subprocess.run(PACKAGE_MANAGERS[manager]["install"] + [program], check=True)

def main():
    # Check if the programs file exists
    if not os.path.isfile(PROGRAMS_FILE):
        print(f"Error: File '{PROGRAMS_FILE}' not found.")
        sys.exit(1)

    # Parse the ini file
    config = configparser.ConfigParser()
    config.read(PROGRAMS_FILE)

    # Iterate through each section (package manager)
    for manager, programs in config.items():
        if manager not in PACKAGE_MANAGERS:
            print(f"Warning: Unsupported package manager '{manager}' in '{PROGRAMS_FILE}'. Skipping...")
            continue

        print(f"\nProcessing programs for {manager}...")
        for program in programs.values():
            program = program.strip()
            if not program:
                continue

            if is_installed(manager, program):
                print(f"{program} is already installed.")
            else:
                print(f"{program} is not installed.")
                try:
                    install_program(manager, program)
                except subprocess.CalledProcessError as e:
                    print(f"Error installing {program} with {manager}: {e}")

if __name__ == "__main__":
    main()
