from flask import Flask, request, jsonify
from flask_cors import CORS
import app as openaiservice
import os
from pathlib import Path
import pandas as pd

# Get the path of the current script
script_dir = Path(__file__).resolve().parent
DATASETS_PATH = script_dir /  '../data'

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

        df, columns, description, unique_values = openaiservice.get_dataset(DATASETS_PATH / '{}'.format(user_dataset))
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
      

@app.route('/api/datasets', methods=['GET'])
def get_files():
    """
    Endpoint to retrieve all files in the data directory.
    """
    try:
        # List all files in the DATA_DIRECTORY
        files = os.listdir(DATASETS_PATH)
        
        # Filter to include only files (exclude directories)
        file_list = [f for f in files if os.path.isfile(os.path.join(DATASETS_PATH, f))]
        
        # Return the list of files as a JSON response
        return jsonify({"files": file_list}), 200
    except FileNotFoundError:
        # Handle case where the directory doesn't exist
        return jsonify({"error": "Data directory not found"}), 404
    except Exception as e:
        # Handle other exceptions
        return jsonify({"error": str(e)}), 500


@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Endpoint to upload a file to the data directory.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    
    try:
        # Ensure the data directory exists
        os.makedirs(DATASETS_PATH, exist_ok=True)
        # Save the file to the DATA_DIRECTORY
        file_path = os.path.join(DATASETS_PATH, file.filename)
        file.save(file_path)
        
        # Return a success message
        return jsonify({"message": f"File {file.filename} uploaded successfully"}), 201
    except Exception as e:
        # Handle exceptions during file saving
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
