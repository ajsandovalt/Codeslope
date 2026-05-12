import argparse
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():

    parser = argparse.ArgumentParser(
        prog="Codeslope",
        description="LLM Agent for coding",
        epilog="For more info see README.md",
    )
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")

    args = parser.parse_args()

    # Load api key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "API Key not detected, make sure you have the GEMINI_API_KEY env var set with your API key."
        )

    # Get client and make the slop flow!
    client = genai.Client(api_key=api_key)
    prompt = args.user_prompt
    messages = [
        # Store messages like a conversation
        types.Content(role="user", parts=[types.Part(text=prompt)])
    ]
    print("Processing...")
    llm_response = client.models.generate_content(
        model="gemini-2.5-flash", contents=messages # Prompt passed as messages
    )
    if not llm_response:
        raise RuntimeError(
            "Response could not be retrieved from the server due to an API error. Request response: ",
            llm_response,
        )

    print("\nThe sloppinator has awaken!🤖\n")

    if args.verbose:
        print("\t🤖---- VERBOSE MODE ACTIVATED BEEP BOOP BEEP ---🤖")
        prompt_toke_usage = llm_response.usage_metadata.prompt_token_count
        response_token_usage = llm_response.usage_metadata.candidates_token_count
        print(f"""
User prompt: {prompt}
Prompt tokens: {prompt_toke_usage}
Response tokens: {response_token_usage}
            """)

    print(f"Reponse:\n{llm_response.text}")


if __name__ == "__main__":
    main()
