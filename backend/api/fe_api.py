from flask import Flask, request, jsonify
from flask_cors import CORS
import app as openaiservice

from pathlib import Path

# Get the path of the current script
script_dir = Path(__file__).resolve().parent


app = Flask(__name__)
CORS(app)

# Custom error messages
def error_response(message, status_code):
    return jsonify({"error": message}), status_code

# Endpoint to handle free text data
@app.route('/api/prompt', methods=['POST'])
def process_text():
    try:
        # Check if the request has a JSON body
        if not request.is_json:
            return error_response("Request must be in JSON format", 400)

        # Extract data from JSON payload
        request_data = request.get_json()
        if 'prompt' not in request_data:
            return error_response("Missing 'prompt' field in request body", 400)

        # Process the 'prompt' field
        user_prompt = request_data['prompt']
        user_dataset = request_data['datasetName']

        dataset_path = script_dir /  '../data/{}'.format(user_dataset)

        df, columns, description, unique_values = openaiservice.get_dataset(dataset_path)
        prompt1_result = openaiservice.generate_pandas_query(columns, description, unique_values, user_prompt)
        print(prompt1_result)
        evaluated_prompt1 = eval(prompt1_result)
        print(evaluated_prompt1)
        data_struct = openaiservice.structure_data_with_format(str(evaluated_prompt1))
        print(data_struct)
        final_data = openaiservice.generate_additional_text(data_struct, user_prompt)
        print(final_data)
        return jsonify(final_data), 200

    except KeyError as e:
        # Handle specific KeyError issues
        return error_response(f"Key error: {str(e)}", 400)

    except Exception as e:
        # Handle unexpected errors
        return error_response(f"An unexpected error occurred: {str(e)}", 500)
      

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
