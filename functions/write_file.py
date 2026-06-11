import os
from google.genai import types

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites a file with the content provided to the method.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A path to the file to write to, relative to the working directory (default is the working directory itself)",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="A string containing the contents to be written to the file.",
            ),
        },
        required=["file_path", "content"],
    ),
)

def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        wd_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_absolute_path, file_path))

        valid_target_file = os.path.commonpath([wd_absolute_path, target_file_path]) == wd_absolute_path
        if not valid_target_file:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(target_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'

        os.makedirs(os.path.dirname(target_file_path), exist_ok=True)

        with open(target_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
