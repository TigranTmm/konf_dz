import yaml
import argparse
import re
import sys

def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("input_file_path", type=str, help="Path to the input YAML file")
	return parser.parse_args()

def read_input_file(input_file_path):
	try:
		with open(input_file_path, "r", encoding="utf-8") as file:
			return file.readlines()
	except FileNotFoundError:
		sys.stderr.write(f"Error: File not found: {input_file_path}\n")
		sys.exit(1)

def extract_comments(input_data):
	comments = []
	data_lines = []
	for line in input_data:
		if line.lstrip().startswith("#"):
			comments.append(line.strip())
		else:
			data_lines.append(line)
	return comments, "".join(data_lines)

def parse_yaml(input_data):
	try:
		return yaml.safe_load(input_data)
	except yaml.YAMLError as e:
		sys.stderr.write(f"Error: Invalid YAML syntax:\n{e}\n")
		sys.exit(1)

def convert_to_config(data, indent=0):
	output = []
	indentation = " " * indent

	if isinstance(data, dict):
		output.append(f"{indentation}struct {{")
		for key, value in data.items():
			if not re.match(r"^[A-Z]+$", key):
				raise ValueError(f"Invalid name '{key}' in dictionary. Names must match [A-Z]+.")
			converted_value = convert_to_config(value, indent + 4)
			output.append(f"{indentation}    {key} = {converted_value},")
		output.append(f"{indentation}}}")
	elif isinstance(data, str):
		output.append(f'@"{data}"')
	elif isinstance(data, int):
		output.append(str(data))
	else:
		raise ValueError(f"Unsupported data type: {type(data).__name__}")

	return "\n".join(output)

def main():
	args = parse_args()
	input_lines = read_input_file(args.input_file_path)
	comments, input_data = extract_comments(input_lines)
	yaml_data = parse_yaml(input_data)

	try:
		config_output = convert_to_config(yaml_data)
		print("Comments in the file:")
		print("\n".join(comments))
		print("\nConverted config:")
		print(config_output)
	except ValueError as e:
		sys.stderr.write(f"Error: {e}\n")
		sys.exit(1)

if __name__ == '__main__':
	main()
