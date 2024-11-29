import unittest
import os
import shutil
import yaml
from main import *


class TestShellEmulator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.config_path = "config.yaml"
        cls.test_vfs_zip = "superzip.zip"
        os.mkdir("superzip1.zip")
        os.mkdir("test_vfs/dir1")
        os.mkdir("test_vfs/dir2")
        with open("test_vfs/file1.txt", "w") as f:
            f.write("This is a test file.")
        shutil.make_archive("test_vfs", 'zip', "test_vfs")
        shutil.rmtree("test_vfs")
        config_data = {
            "username": "testuser",
            "hostname": "testhost",
            "vfs_path": cls.test_vfs_zip,
        }
        with open(cls.config_path, 'w') as f:
            yaml.dump(config_data, f)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.test_vfs_zip)
        os.remove(cls.config_path)

    def setUp(self):
        self.emulator = ShellEmulator(self.config_path)

    def tearDown(self):
        shutil.rmtree(self.emulator.temp_dir)

    def test_prompt(self):
        self.assertEqual(
            self.emulator.prompt(),
            "testuser@testhost:/tmp$ "
        )

    def test_list_directory(self):
        result = self.emulator.list_directory()
        self.assertIn("file1.txt", result)
        self.assertIn("dir1", result)
        self.assertIn("dir2", result)

    def test_change_directory(self):
        result = self.emulator.change_directory("dir1")
        self.assertIn("Changed directory to", result)
        self.assertTrue(self.emulator.current_path.endswith("dir1"))
        result = self.emulator.change_directory("nonexistent")
        self.assertEqual(result, "No such file or directory.")

    def test_remove_directory(self):
        result = self.emulator.remove_directory("dir1")
        self.assertEqual(result, "Removed directory dir1")
        result = self.emulator.remove_directory("nonexistent")
        self.assertIn("No such file or directory", result)

    def test_current_date(self):
        result = self.emulator.current_date()
        self.assertRegex(result, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")

    def test_show_help(self):
        result = self.emulator.show_help()
        self.assertIn("Available commands:", result)
        self.assertIn("ls", result)
        self.assertIn("cd <directory>", result)

    def test_run_command(self):
        result = self.emulator.run_command("ls")
        self.assertIn("file1.txt", result)
        self.assertIn("dir1", result)
        result = self.emulator.run_command("cd dir1")
        self.assertIn("Changed directory to", result)
        self.assertTrue(self.emulator.current_path.endswith("dir1"))
        result = self.emulator.run_command("rmdir dir2")
        self.assertEqual(result, "Removed directory dir2")
        result = self.emulator.run_command("unknown")
        self.assertEqual(result, "unknown: command not found")
        result = self.emulator.run_command("date")
        self.assertRegex(result, r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}")
        result = self.emulator.run_command("help")
        self.assertIn("Available commands:", result)


if __name__ == "__main__":
    unittest.main()
