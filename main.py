import os
import argparse
from prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types
from call_function import available_functions, call_function

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Could not read api key")

    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="AI Chatbot agent")
    parser.add_argument("user_prompt", type=str, help="A prompt for the AI to respond to")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages: list[types.Content] = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(20):
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=messages,
            config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt
                )
            )

        if response.usage_metadata == None:
            raise RuntimeError("Failed API request: Did not get a respons from Gemini")

        if len(response.candidates) > 0:
            for respons_candidate in response.candidates:
                messages.append(respons_candidate.content)

        if args.verbose:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        function_results = []
        if response.function_calls:
            for function_call in response.function_calls:
                print(f"- Calling function: {function_call.name}")

                function_call_result = call_function(function_call, args.verbose)

                if function_call_result.parts[0].function_response == None:
                    raise Exception("function_response is none")
                if function_call_result.parts[0].function_response.response == None:
                    raise Exception("function_response.response is none")

                function_results.append(function_call_result.parts[0])

                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")

            messages.append(types.Content(role="user", parts=function_results))

        else:
            print("Final response:")
            print(response.text)
            return None

    print("Maximum number of agent iterations reached.")
    exit(1)


if __name__ == "__main__":
    main()
