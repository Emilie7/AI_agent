import os
from .config import MAX_CHARS
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Fetches all the content from a file unless it is greater than MAX_CHARS (Stored in config.py) in which case it only fetches the first fx 10000 chars from the file.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A path to the file to fetch contents from, relative to the working directory (default is the working directory itself)",
            ),
        },
        required=["file_path"],
    ),
)

def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        wd_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_absolute_path, file_path))

        valid_target_file = os.path.commonpath([wd_absolute_path, target_file_path]) == wd_absolute_path
        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)

            if f.read(1):
                file_content += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

        return file_content

    except Exception as e:
        return f"Error: {e}"
