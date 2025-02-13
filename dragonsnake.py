from ast import parse as _parse_python
from dragonsnake.code_generation.cpp import generate_cpp
from dragonsnake.utils import load_text_files_as_one, parse_program_arguments, print_dump, save_text_file, throw_feature_not_supported


# Parse the arguments passed to the program.
args = parse_program_arguments()

# Get the source code to parse.
python_source_code = load_text_files_as_one(args.input)

# Parse the source code into an AST.
python_module = _parse_python(python_source_code)

# If the program should print the AST:
if args.ast:
    # Print the AST.
    print_dump(python_module)
    # Exit the program.
    exit()

# Generate C++ source code from the Python module.
cpp_source_code = generate_cpp(python_module)

# Write the C++ source code to the output file.
save_text_file(args.output, cpp_source_code)
