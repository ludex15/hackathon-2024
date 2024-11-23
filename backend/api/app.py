import json
from openai import OpenAI
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def query_openai(inputprompt):
    """
    Sends a query to OpenAI and returns the response content in JSON format.

    Args:
        inputprompt (str): The query to send to OpenAI.

    Returns:
        str: A JSON string containing the return code and response content.
    """
    # Get API key from environment variable
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        error_response = {"return_code": 1, "content": "Error: OPENAI_API_KEY not found in environment variables."}
        return error_response

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    try:
        # Send a ChatCompletion request with the user's input
        response = client.chat.completions.create(
            model='gpt-4o-mini',  # Replace with the desired model name
            messages=[
                {'role': 'user', 'content': inputprompt}
            ],
            temperature=0,
        )

        # Extract the content of the response
        content = response.choices[0].message.content

        # Return success JSON
        success_response = {"return_code": 0, "content": content}
        return success_response

    except Exception as e:
        # Return error JSON
        error_response = {"return_code": 1, "content": str(e)}
        return error_response

