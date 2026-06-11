This is a project on creating a toy AI in python from the Boot.dev cours "Build an AI Agent in Python".

OBS!: Running this project as is can be dangerouse! 
This is becouse the AI has the ability to run Python code on your machin through the subrutine method. Please 
insure that all the python files in functions are limited to work within the folder you expect by looking at 
call_function.py. By defualt the code should only work when calling methods on files and folders within the 
calculator directory of this project.

Important files/folders:
- The project is set up with uv. Start buy running "uv init <project_name>"
- main.py: Calls the AI gemini-2.5-flash (You will need to get a API key and put it in a .env file: https://aistudio.google.com/app/api-keys)
- call_function.py: Handels how the AI can call the python functions which are located in the functions folder.
- prompts.py: Contains the system prompt
- The calculator folder currently holdes the "toy" project which the AI agent can interact with  
