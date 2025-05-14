# Terminal Setup Script

This Python script helps you **backup**, **restore**, and **set up your Linux terminal environment to look and behave like Kali Linux**.  
It automates the installation and configuration of Zsh, Oh My Zsh, popular plugins, and sets the `robbyrussell` theme.  
It also safely backs up your existing terminal configuration files before making any changes.

---

## Features

- **Backup** your current `.zshrc`, `.bashrc`, and `.bash_profile` to a timestamped directory.
- **Restore** your terminal configuration from a previous backup.
- **Automated setup**:
  - Installs `git`, `zsh`, and `curl`
  - Installs [Oh My Zsh](https://ohmyz.sh/)
  - Installs [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting) and [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions) plugins
  - Sets the Oh My Zsh theme to `robbyrussell`
  - Sets up plugins in `.zshrc`
  - Changes your default shell to Zsh

---

## Requirements

- Python 3
- Debian/Ubuntu-based Linux distribution (for other distros, adapt the package manager commands)
- `sudo` privileges (for installing packages and changing the default shell)

---

## Usage

1. **Download the script**

~~~
wget https://github.com/cryptshoe/terminal-setup.git
chmod +x terminal_setup.py
~~~

2. **Run the script**

~~~
python3 terminal_setup.py
~~~

3. **Choose an option:**

- `1`: Backup terminal configuration files
- `2`: Restore terminal configuration files from backup
- `3`: Setup terminal like Kali Linux (after backup!)

---

## Backup & Restore

- Backups are stored in `~/terminal_backup/` with a timestamp.
- Restoring will overwrite your current configuration files with the selected backup.

---

## Notes

- The script will prompt for your password when installing packages or changing the default shell.
- After setup, **log out and log back in** or open a new terminal to start using Zsh with the new configuration.
- If you want to revert your changes, use the restore option.

---

## Troubleshooting

- If you encounter issues, ensure you have an active internet connection and `sudo` privileges.
- For non-Debian systems, modify the package installation commands as needed.
  
---

## Credits

- [Oh My Zsh](https://ohmyz.sh/)
- [zsh-syntax-highlighting](https://github.com/zsh-users/zsh-syntax-highlighting)
- [zsh-autosuggestions](https://github.com/zsh-users/zsh-autosuggestions)

---

**Enjoy your Kali-like terminal!**
