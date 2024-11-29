import os
import sys
import zipfile
import yaml
import tempfile
from datetime import datetime

class ShellEmulator:
    def __init__(self, config_path):
        self.load_config(config_path)
        self.current_path = self.vfs_path

    def load_config(self, config_path):
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
            self.username = config['username']
            self.hostname = config['hostname']
            self.vfs_zip_path = config['vfs_path']

        self.temp_dir = tempfile.mkdtemp()
        with zipfile.ZipFile(self.vfs_zip_path, 'r') as zip_ref:
            zip_ref.extractall(self.temp_dir)

        self.vfs_path = self.temp_dir

    def prompt(self):
        relative_path = os.path.relpath(self.current_path, self.vfs_path)
        display_path = relative_path if relative_path != '.' else '/'
        return f"{self.username}@{self.hostname}:{display_path}$ "

    def list_directory(self):
        try:
            items = os.listdir(self.current_path)
            return "\n".join(items)
        except FileNotFoundError:
            return "Directory not found."

    def change_directory(self, path):
        target_path = os.path.normpath(os.path.join(self.current_path, path))

        if not target_path.startswith(self.vfs_path):
            return "Permission denied: Cannot navigate outside the virtual file system."

        if os.path.isdir(target_path):
            self.current_path = target_path
            return f"Changed directory to {os.path.relpath(self.current_path, self.vfs_path)}"
        else:
            return "No such file or directory."

    def remove_directory(self, dirname):
        path_to_remove = os.path.join(self.current_path, dirname)
        try:
            os.rmdir(path_to_remove)
            return f"Removed directory {dirname}"
        except OSError as e:
            return str(e)

    def current_date(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def show_help(self):
        help_text = (
            "Available commands:\n"
            "  ls              - List directory contents\n"
            "  cd <directory>  - Change directory\n"
            "  rmdir <directory> - Remove directory\n"
            "  date            - Show current date and time\n"
            "  help            - Show this help message\n"
            "  exit            - Exit the shell emulator\n"
        )
        return help_text

    def run_command(self, command):
        parts = command.strip().split()
        if not parts:
            return ""

        cmd = parts[0]
        if cmd == "ls":
            return self.list_directory()
        elif cmd == "cd":
            if len(parts) < 2:
                return "cd: missing argument"
            return self.change_directory(parts[1])
        elif cmd == "rmdir":
            if len(parts) < 2:
                return "rmdir: missing argument"
            return self.remove_directory(parts[1])
        elif cmd == "date":
            return self.current_date()
        elif cmd == "help":
            return self.show_help()
        elif cmd == "exit":
            return "Exiting..."
        else:
            return f"{cmd}: command not found"

    def start(self):
        print("Welcome to the Shell Emulator!")
        while True:
            command = input(self.prompt())
            output = self.run_command(command)
            print(output)
            if command.strip() == "exit":
                break

if __name__ == "__main__":
    # Uncomment to use config file argument
    # if len(sys.argv) != 2:
    #     print("Usage: python shell_emulator.py <config_file.yaml>")
    #     sys.exit(1)

    emulator = ShellEmulator("config.yaml")
    emulator.start()
