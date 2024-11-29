import unittest
from unittest.mock import patch, mock_open
import io
import yaml
import re
from main import *

class TestConfigTool(unittest.TestCase):
    def test_remove_comments(self):
        input_data = """
        key: value  # This is a comment
        another_key: 123 # Another comment
        # Full line comment
        """
        expected_output = """
        key: value  
        another_key: 123 

        """
        self.assertEqual(remove_comments(input_data), expected_output)

    def test_parse_yaml_valid(self):
        input_data = """
        KEY: value
        NUMBER: 123
        """
        expected_output = {"KEY": "value", "NUMBER": 123}
        self.assertEqual(parse_yaml(input_data), expected_output)

    def test_parse_yaml_invalid(self):
        input_data = """
        KEY value
        NUMBER: 123
        """
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
                parse_yaml(input_data)
            self.assertIn("Error: Invalid YAML syntax", mock_stderr.getvalue())

    def test_convert_to_config_valid(self):
        input_data = {"KEY": "value", "NUMBER": 123}
        expected_output = (
            "struct {\n"
            "    KEY = @\"value\",\n"
            "    NUMBER = 123,\n"
            "}"
        )
        self.assertEqual(convert_to_config(input_data), expected_output)

    def test_convert_to_config_invalid_name(self):
        input_data = {"Invalid_KEY": "value"}
        with self.assertRaises(ValueError) as context:
            convert_to_config(input_data)
        self.assertIn("Invalid name 'Invalid_KEY'", str(context.exception))

    def test_convert_to_config_nested(self):
        input_data = {"OUTER": {"INNER": 456}}
        expected_output = (
            "struct {\n"
            "    OUTER = struct {\n"
            "        INNER = 456,\n"
            "    },\n"
            "}"
        )
        self.assertEqual(convert_to_config(input_data), expected_output)

    @patch("builtins.open", new_callable=mock_open, read_data="KEY: value\nNUMBER: 123")
    def test_read_input_file(self, mock_file):
        result = read_input_file("fake_path.yaml")
        self.assertEqual(result, "KEY: value\nNUMBER: 123")

    @patch("builtins.open", side_effect=FileNotFoundError)
    def test_read_input_file_not_found(self, mock_file):
        with self.assertRaises(SystemExit):
            with patch('sys.stderr', new_callable=io.StringIO) as mock_stderr:
                read_input_file("nonexistent_file.yaml")
            self.assertIn("Error: File not found", mock_stderr.getvalue())

    @patch("sys.stdout", new_callable=io.StringIO)
    @patch("sys.argv", ["main.py", "fake_path.yaml"])
    @patch("builtins.open", new_callable=mock_open, read_data="KEY: value\nNUMBER: 123")
    def test_main_valid(self, mock_file, mock_stdout):
        with patch("main.parse_args", return_value=argparse.Namespace(input_file_path="fake_path.yaml")):
            main()
        self.assertIn("struct {\n    KEY = @\"value\",\n    NUMBER = 123,\n}", mock_stdout.getvalue())

    @patch("sys.stderr", new_callable=io.StringIO)
    @patch("sys.argv", ["main.py", "fake_path.yaml"])
    @patch("builtins.open", new_callable=mock_open, read_data="KEY value\nNUMBER: 123")
    def test_main_invalid_yaml(self, mock_file, mock_stderr):
        with self.assertRaises(SystemExit):
            main()
        self.assertIn("Error: Invalid YAML syntax", mock_stderr.getvalue())

if __name__ == "__main__":
    unittest.main()