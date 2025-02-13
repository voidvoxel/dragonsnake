import argparse as _argparse
import ast as _ast
from ast import dump as _dump_python_ast


def _get_default_output(
    format: str
) -> str:
    # Windows Executable
    if format == "exe":
        return "program.exe"
    # C++
    if format == "cpp":
        return "main.cpp"
    # Default
    return "program"


def abort(
    code: int = 0xFFFFFFFF,
    message: str = ""
):
    '''
    Abort the program by printing `message` and then returning `code`.
    '''
    # If a message was provided:
    if (type(message) is str and len(message) > 0):
        # Print the error message.
        print("[Error " + hex(code) + "] " + message)
    # Otherwise:
    else:
        # Print a generic error message.
        print("[Error " + hex(code) + "] An unknown error occured. ")
    # DEBUG: To debug errors, uncomment the following line and re-run.
    # raise Exception()
    # Exit the program, returning the provided exit code.
    exit(code)


def list_bool(values: list[object]) -> list[bool]:
    converted_values = []
    for value in values:
        converted_value = bool(value)
        converted_values.append(converted_value)
    return converted_values


def list_int(values: list[object]) -> list[int]:
    converted_values = []
    for value in values:
        converted_value = int(value)
        converted_values.append(converted_value)
    return converted_values


def list_float(values: list[object]) -> list[float]:
    converted_values = []
    for value in values:
        converted_value = float(value)
        converted_values.append(converted_value)
    return converted_values


def list_str(values: list[object]) -> list[str]:
    converted_values = []
    for value in values:
        converted_value = str(value)
        converted_values.append(converted_value)
    return converted_values


def print_dump(object_: object) -> str:
    # Get a prettified dump of the AST.
    python_ast_dump = _dump_python_ast(object_, indent=4)
    # Print the dump.
    print(python_ast_dump)


def resolve_variable_name(function_id: int, variable_name: str) -> str:
    # If the variable name is a class property name:
    if variable_name.startswith("__"):
        # Return the resolved class attribute name.
        return resolve_class_attribute_name(variable_name)
    # If the variable name is an unmangled variable name:
    if variable_name.startswith("@"):
        # Return the resolved unmangled variable name.
        return resolve_unmangled_variable_name(variable_name)
    # Return the resolved local variable name.
    return resolve_local_variable_name(function_id, variable_name)


def resolve_class_attribute_name(variable_name: str) -> str:
    return variable_name


def hex2(value: int) -> str:
    return hex(value)[3:]


def _resolve_hex(value: object) -> str:
    hash_code = value
    if isinstance(hash_code, int):
        hash_code = 11 * hash_code * 13 * hash_code * 27
    hash_code = hash(hash_code)
    return hex2(hash_code)[:6]


def resolve_local_variable_name(function_id: int, variable_name: str) -> str:
    function_id_hex = _resolve_hex(function_id)
    variable_name_hex = _resolve_hex(variable_name)
    resolved_variable_name = "_" + function_id_hex + "_" + variable_name_hex
    return resolved_variable_name


def resolve_unmangled_variable_name(variable_name: str) -> str:
    return variable_name[1:]


def load_text_file(
    file_path: str
) -> str:
    '''
    Load the contents of a text file.
    '''
    # Open the file and close the resource afterwards.
    with open(file_path, 'r') as file:
        # Read and return the contents of the file.
        return file.read().strip()


def load_text_files(
    input_paths: list[str]
) -> list[str]:
    '''
    Load the contents of multiple text files.
    '''
    # Create an empty list to hold the contents of each file.
    file_contents = []
    # For each file path:
    for file_path in input_paths:
        # Load the contents of the text file.
        file_content = load_text_file(file_path)
        # Add the contents of the text file to the list.
        file_contents.append(file_content)
    # Return the list of contents of each file.
    return file_contents


def load_text_files_as_one(
    input_paths: list[str]
) -> str:
    '''
    Load the contents of multiple text files as one string.
    '''
    file_contents = load_text_files(input_paths)
    return "\n".join(file_contents)


def parse_program_arguments() -> object:
    '''
    Parse any arguments passed to the program.
    '''
    # Create a new program argument parser.
    argument_parser = _argparse.ArgumentParser(
        prog = "dragonsnake",
        description = "Dragonsnake Python-to-C++ Transpiler",
        epilog = "Made with lots of love <3",
        usage = "dragonsnake <input_files> [options] -o <output_file>"
    )
    # Add arguments to the parser.
    argument_parser.add_argument(
        "input",
        action = "extend",
        nargs = "+",
        type = str
    )
    argument_parser.add_argument(
        "--ast",
        action="store_true"
    )
    argument_parser.add_argument(
        "--debug",
        type = bool,
        default = False
    )
    # argument_parser.add_argument("-h", "--help")
    argument_parser.add_argument(
        "-f",
        "--format",
        type = str,
        default = ""
    )
    argument_parser.add_argument(
        "-o",
        "--output",
        type = str,
        default = "{DEFAULT_OUTPUT}"
    )
    # argument_parser.add_argument("--usage")
    argument_parser.add_argument("-V", "--verbose")
    # argument_parser.add_argument("-v", "--version")
    # Parse the program arguments.
    program_arguments = argument_parser.parse_args()
    # Auto-detect the output format using the output file extension.
    if program_arguments.format is None or len(program_arguments.format) < 1:
        # Get the file extension of the output file path.
        output_file_extension = program_arguments.output.split(".")[-1]
        # Use the output file extension as the default output format.
        program_arguments.format = output_file_extension
    program_arguments.output.replace(
        "{DEFAULT_OUTPUT}",
        _get_default_output(program_arguments.format)
    )
    # Return the program's arguments.
    return program_arguments


def save_text_file(
    path: str,
    data: str
):
    '''
    Save the contents of a text file.
    '''
    # Open the file and close the resource afterwards.
    with open(path, 'w') as file:
        # Write the contents of the file.
        return file.write(data)


def throw_feature_not_supported(
        feature: object,
        namespace: str = None,
        category: str = None
):
    error_message = "Feature not yet supported: "
    if namespace is not None:
        namespace = str(namespace)
        error_message += namespace + "/"
    if category is not None:
        category = str(category)
        error_message += category + "/"
    error_message += feature.__class__.__name__
    abort(
        code = 0x111E_ED42,
        message = error_message
    )
