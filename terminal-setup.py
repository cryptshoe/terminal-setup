#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
from datetime import datetime

HOME = os.path.expanduser("~")
BACKUP_DIR = os.path.join(HOME, "terminal_backup")
TIMESTAMP = datetime.now().strftime("%Y%m%d_%H%M%S")
THIS_BACKUP = os.path.join(BACKUP_DIR, TIMESTAMP)
CONFIG_FILES = [".zshrc", ".bashrc", ".bash_profile"]

def run_cmd(cmd, check=True):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check, text=True)
    return result

def backup_configs():
    os.makedirs(THIS_BACKUP, exist_ok=True)
    files_backed_up = []
    for fname in CONFIG_FILES:
        src = os.path.join(HOME, fname)
        if os.path.exists(src):
            dest = os.path.join(THIS_BACKUP, fname)
            shutil.copy(src, dest)
            files_backed_up.append(fname)
            print(f"Backed up {fname} to {dest}")
    if not files_backed_up:
        print("No config files found to backup.")
    else:
        print(f"\nBackup complete. Backup folder: {THIS_BACKUP}")

def list_backups():
    if not os.path.isdir(BACKUP_DIR):
        print("No backups found.")
        return []
    backups = sorted(os.listdir(BACKUP_DIR), reverse=True)
    for i, b in enumerate(backups):
        print(f"{i+1}: {b}")
    return backups

def restore_configs():
    backups = list_backups()
    if not backups:
        print("No backups to restore.")
        return
    choice = input("Enter the number of the backup to restore: ")
    try:
        idx = int(choice) - 1
        backup_path = os.path.join(BACKUP_DIR, backups[idx])
    except (ValueError, IndexError):
        print("Invalid selection.")
        return
    for fname in CONFIG_FILES:
        src = os.path.join(backup_path, fname)
        dest = os.path.join(HOME, fname)
        if os.path.exists(src):
            shutil.copy(src, dest)
            print(f"Restored {fname} from {src}")
    print("Restore complete. Please restart your terminal.")

def set_zsh_theme_and_plugins(zshrc_path):
    # Read existing .zshrc if it exists
    theme_set = False
    plugins_set = False
    lines = []
    if os.path.exists(zshrc_path):
        with open(zshrc_path, "r") as f:
            for line in f:
                if line.startswith("ZSH_THEME="):
                    lines.append('ZSH_THEME="robbyrussell"\n')
                    theme_set = True
                elif line.startswith("plugins="):
                    lines.append("plugins=(git zsh-syntax-highlighting zsh-autosuggestions)\n")
                    plugins_set = True
                else:
                    lines.append(line)
    # Add theme if not set
    if not theme_set:
        lines.insert(0, 'ZSH_THEME="robbyrussell"\n')
    # Add plugins if not set
    if not plugins_set:
        # After theme or at top if theme wasn't present
        insert_idx = 1 if theme_set or lines and lines[0].startswith('ZSH_THEME=') else 0
        lines.insert(insert_idx, "plugins=(git zsh-syntax-highlighting zsh-autosuggestions)\n")
    # Ensure Oh My Zsh is sourced
    if not any("source $ZSH/oh-my-zsh.sh" in l for l in lines):
        lines.append("\nsource $ZSH/oh-my-zsh.sh\n")
    # Write back
    with open(zshrc_path, "w") as f:
        f.writelines(lines)

def install_zsh_and_ohmyzsh():
    # Install git first
    run_cmd("sudo apt-get update && sudo apt-get install -y git")
    # Install Zsh
    run_cmd("sudo apt-get install -y zsh")
    # Install curl if not present
    run_cmd("sudo apt-get install -y curl")
    # Install Oh My Zsh (unattended)
    run_cmd('sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" "" --unattended')
    # Install plugins
    plugins_dir = os.path.expanduser("~/.oh-my-zsh/custom/plugins")
    os.makedirs(plugins_dir, exist_ok=True)
    run_cmd(f"git clone https://github.com/zsh-users/zsh-syntax-highlighting.git {plugins_dir}/zsh-syntax-highlighting")
    run_cmd(f"git clone https://github.com/zsh-users/zsh-autosuggestions {plugins_dir}/zsh-autosuggestions")
    # Set theme and plugins in .zshrc
    zshrc = os.path.expanduser("~/.zshrc")
    set_zsh_theme_and_plugins(zshrc)
    # Change default shell to zsh
    run_cmd("chsh -s $(which zsh)")
    print("\nSetup complete! Please log out and log back in, or start a new terminal session to use Zsh.")

def main():
    print("1. Backup terminal configuration files")
    print("2. Restore terminal configuration files from backup")
    print("3. Setup terminal like Kali Linux (after backup!)")
    choice = input("Choose an option [1/2/3]: ").strip()
    if choice == "1":
        backup_configs()
    elif choice == "2":
        restore_configs()
    elif choice == "3":
        backup_configs()
        install_zsh_and_ohmyzsh()
    else:
        print("Invalid option.")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Some steps require sudo privileges. You may be prompted for your password.")
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
