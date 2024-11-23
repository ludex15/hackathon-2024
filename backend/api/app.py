import json
import pandas as pd
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Load the dataset
dataset_path = "../data/dataset.csv"

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
        return json.dumps(error_response)

    # Initialize OpenAI client
    client = OpenAI(api_key=api_key)

    try:
        # Read dataset columns for AI prompt
        df = pd.read_csv(dataset_path, nrows=0)
        columns = ', '.join(df.columns)

        # AI prompt
        ai_prompt = f"""
        The dataset contains the following columns: {columns}.
        Write Python Pandas code to answer the query: "{inputprompt}".
        - Ensure the code handles case sensitivity (e.g., for 'Gender', use `.str.lower()`).
        - Assign the result to a variable named `result`.
        Only return the Pandas code, no additional explanations or text.
        """

        # Call OpenAI API
        response = client.chat.completions.create(
            model='gpt-4',
            messages=[{'role': 'user', 'content': ai_prompt}]
        )

        # Extract the generated code
        generated_code = response.choices[0].message.content.strip()

        # Remove code block formatting if present
        if generated_code.startswith("```") and generated_code.endswith("```"):
            generated_code = generated_code.split("\n", 1)[1].rsplit("\n", 1)[0]

        # Debug: Log the generated code
        print("Generated Code:", generated_code)

        # Load the dataset
        df = pd.read_csv(dataset_path)

        # Prepare a secure execution environment
        local_env = {'df': df}

        # Validate and execute the code
        exec(generated_code, {}, local_env)

        # Retrieve the result from the execution environment
        result = local_env.get('result', None)
        if result is None:
            raise ValueError("The AI-generated code did not produce a 'result' variable.")

        # Convert result to JSON
        if isinstance(result, pd.DataFrame):
            result_json = result.to_json(orient="records")
        else:
            result_json = json.dumps(result)

        # Return success JSON
        success_response = {"return_code": 0, "content": result_json}
        return json.dumps(success_response)

    except Exception as e:
        # Return error JSON with debug information
        error_response = {
            "return_code": 1,
            "content": f"Error: {str(e)}",
            "debug": {
                "inputprompt": inputprompt,
                "generated_code": locals().get("generated_code", "No code generated")
            }
        }
        return json.dumps(error_response)

# Example usage
if __name__ == "__main__":
    inputprompt = input("Enter your query: ")
    result = query_openai(inputprompt)
    print(result)
