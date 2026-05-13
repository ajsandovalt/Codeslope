import argparse
import os
import sys

from dotenv import load_dotenv
from google import genai
from google.genai import types

from utilities.prompts import *
from utilities.config import MODEL_NAME
from utilities.call_function import *


def main():

    try:
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

        # Get client and set up prompt
        client = genai.Client(api_key=api_key)
        prompt = args.user_prompt
        messages = [
            # Store messages like a conversation
            types.Content(role="user", parts=[types.Part(text=prompt)])
        ]

        print("Processing...")
        
        for i in range(20):

            llm_response = client.models.generate_content(
                model=MODEL_NAME,
                contents=messages, # Prompt passed as messages
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[AVAILABLE_FUNCTIONS],
                    #temperature=0 # We want a deterministic output
                    )
            )
            if not llm_response:
                raise RuntimeError(
                    "Response could not be retrieved from the server due to an API error. Request response: ",
                    llm_response,
                )
            
            candidates = llm_response.candidates

            if candidates:
                
                for candidate in candidates:
                    messages.append(candidate.content)

            llm_function_calls = llm_response.function_calls
            
            if llm_function_calls:

                function_results = []

                for call in llm_function_calls:
                    call_result = call_function(call)
                    if not call_result.parts:
                        raise Exception("Parts list is empty")
                    if not call_result.parts[0].function_response:
                        raise Exception("Function Reponse is empty")
                    if not call_result.parts[0].function_response.response:
                        raise Exception("Reponse is empty")
                    
                    function_results.append(call_result.parts[0])
            else:
                final_result = llm_response.text
                break
            
            messages.append(types.Content(role="user", parts=function_results))
            
            if args.verbose:
                print (llm_response.text)

            if i == 19:
                print("Error: LLM Could not give a definitive answer")
                sys.exit(1)


        print("\nCodeslope has awaken!🤖\n")

        if args.verbose:
            print("\t🤖---- VERBOSE MODE ACTIVATED BEEP BOOP BEEP ---🤖")
            prompt_toke_usage = llm_response.usage_metadata.prompt_token_count
            response_token_usage = llm_response.usage_metadata.candidates_token_count
            print(f"""
    User prompt: {prompt}
    Prompt tokens: {prompt_toke_usage}
    Response tokens: {response_token_usage}

                """)
            for result in function_results:
                print(f"-> {result.function_response.response}")
            
        


        print("---------------------------------\n")
        print(final_result)
    except Exception as e:
        print(f"An exception has occurred: {e}")



if __name__ == "__main__":
    main()
