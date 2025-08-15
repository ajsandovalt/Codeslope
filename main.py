import os
import sys
import argparse
from google import genai
from dotenv import load_dotenv
from google.genai import types


def main():
    #Load the .env file, you should have your API key in the GEMINI_API_KEY env variable
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    parser = argparse.ArgumentParser(
            prog="Codeslope",
            description="AI Agent to help you generate more code faster than ever!",
            epilog="This program is licensed under the GNU GPLv3 License")

    parser.add_argument("prompt")
    parser.add_argument("-v", "--verbose", action="store_const", const=True)

    arguments = parser.parse_args()


    #Check if user entered prompt

    prompt = arguments.prompt

    # Save user prompts in memory to keep track of the convesation and the LLM can have context
    messages = [

        types.Content(role="user", parts=[types.Part(text=prompt)]),
    ]

    # Call the genAI model ussing our messages (The context)
    client = genai.Client(api_key=api_key)
    response = client.models.generate_content(
        model="gemini-2.0-flash-001", contents=messages
    )

    #Print response
    print(response.text)

    #Print verbose data
    if arguments.verbose:
        print(f"User prompt: {prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    sys.exit(0)

if __name__ == "__main__":
    main()
