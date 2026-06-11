import os
import subprocess
from google.genai import types

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a python file. If the program does not finish in 30 seconds it will be terminated early to prevent methods from running indefinitely.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="A path to the python file to run, relative to the working directory (default is the working directory itself)",
            ),
            "args": types.Schema(
                type=types.Type.STRING,
                description="An optional varibale to add arguments when running the python file. Only arguments which python normaly accepts should be used here.",
            ),
        },
        required=["file_path"],
    ),
)

def run_python_file(working_directory: str, file_path: str, args: list[str] | None = None) -> str:
    try:
        wd_absolute_path = os.path.abspath(working_directory)
        target_file_path = os.path.normpath(os.path.join(wd_absolute_path, file_path))

        valid_target_file = os.path.commonpath([wd_absolute_path, target_file_path]) == wd_absolute_path
        if not valid_target_file:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(target_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if target_file_path[-3:] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", target_file_path]

        if args != None:
            command.extend(args)

        completed_process = subprocess.run(command, cwd=wd_absolute_path, capture_output=True, timeout=30, text=True)

        process_reslut = ""

        if completed_process.returncode != 0:
            process_reslut += f"Process exited with code {completed_process.returncode}. "

        if completed_process.stdout == None and completed_process.stderr == None:
            process_reslut += "No output produced"
        else:
            process_reslut += f"STDOUT: {completed_process.stdout}\nSTDERR: {completed_process.stderr}"

        return process_reslut

    except Exception as e:
        return f"Error: executing Python file: {e}"
