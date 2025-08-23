package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"

	"gopkg.in/yaml.v3"
)

const configFile = "programs.yaml"

// Config represents the structure of the YAML config.
// Keys are package managers, values are lists of programs.
type Config map[string][]string

// Commands for supported package managers
var packageManagers = map[string]map[string][]string{
	"apt": {
		"check":   {"which"},
		"install": {"sudo", "apt", "install", "-y"},
		"update":  {"sudo", "apt", "update"},
	},
	"brew": {
		"check":   {"brew", "list"},
		"install": {"brew", "install"},
		"update":  {"brew", "update"},
	},
	"dnf": {
		"check":   {"which"},
		"install": {"sudo", "dnf", "install", "-y"},
		"update":  {"sudo", "dnf", "check-update"},
	},
	"yum": {
		"check":   {"which"},
		"install": {"sudo", "yum", "install", "-y"},
		"update":  {"sudo", "yum", "check-update"},
	},
	"pacman": {
		"check":   {"pacman", "-Q"},
		"install": {"sudo", "pacman", "-S", "--noconfirm"},
		"update":  {"sudo", "pacman", "-Sy"},
	},
}

// runCommand executes a command and returns any error.
func runCommand(cmdArgs []string) error {
	cmd := exec.Command(cmdArgs[0], cmdArgs[1:]...)
	cmd.Stdout = nil
	cmd.Stderr = nil
	return cmd.Run()
}

// isInstalled checks if a program is installed with the given package manager.
func isInstalled(manager, program string) bool {
	checkCmd := append(packageManagers[manager]["check"], program)
	err := runCommand(checkCmd)
	return err == nil
}

// installProgram updates package lists and installs the given program.
func installProgram(manager, program string) error {
	fmt.Printf("Installing %s with %s...\n", program, manager)
	if err := runCommand(packageManagers[manager]["update"]); err != nil {
		return fmt.Errorf("update failed: %w", err)
	}
	return runCommand(append(packageManagers[manager]["install"], program))
}

func main() {
	// Read config file
	data, err := os.ReadFile(configFile)
	if err != nil {
		log.Fatalf("Error reading config file: %v", err)
	}

	// Parse YAML
	var cfg Config
	if err := yaml.Unmarshal(data, &cfg); err != nil {
		log.Fatalf("Error parsing config: %v", err)
	}

	// Process each package manager
	for manager, programs := range cfg {
		if _, ok := packageManagers[manager]; !ok {
			fmt.Printf("Warning: Unsupported package manager '%s'. Skipping...\n", manager)
			continue
		}

		fmt.Printf("\nProcessing programs for %s...\n", manager)
		for _, program := range programs {
			if isInstalled(manager, program) {
				fmt.Printf("%s is already installed.\n", program)
			} else {
				fmt.Printf("%s is not installed.\n", program)
				if err := installProgram(manager, program); err != nil {
					fmt.Printf("Error installing %s with %s: %v\n", program, manager, err)
				}
			}
		}
	}
}
