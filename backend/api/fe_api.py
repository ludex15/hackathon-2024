from flask import Flask, request, jsonify
from flask_cors import CORS
from app import get_dataset, generate_pandas_query, structure_data_with_format, generate_additional_text


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

        df, columns, description, unique_values = get_dataset(user_dataset)
        prompt1_result = generate_pandas_query(columns, description, unique_values, user_prompt)
        evaluated_prompt1 = eval(prompt1_result)
        data_struct = structure_data_with_format(str(evaluated_prompt1))
        final_data = generate_additional_text(data_struct, user_prompt)
        return jsonify({"message": final_data}), 200

    except KeyError as e:
        # Handle specific KeyError issues
        return error_response(f"Key error: {str(e)}", 400)

    except Exception as e:
        # Handle unexpected errors
        return error_response(f"An unexpected error occurred: {str(e)}", 500)
      

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
