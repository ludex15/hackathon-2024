from flask import Flask, request, jsonify
from flask_cors import CORS
from app import query_openai


app = Flask(__name__)
CORS(app)

# Custom error messages
def error_response(message, status_code):
    return jsonify({"error": message}), status_code

app = Flask(__name__)

# Endpoint to handle free text data
@app.route('/api/prompt', methods=['POST'])
def process_text():
    try:
        # Check if the request has a JSON body
        if not request.is_json:
            return error_response("Request must be in JSON format", 400)

        # Extract data from JSON payload
        data = request.get_json()
        if 'prompt' not in data:
            return error_response("Missing 'prompt' field in request body", 400)

        # Process the 'prompt' field
        user_prompt = data['prompt']
        openai_response = query_openai(user_prompt)

        if openai_response["return_code"] != 0:
            return error_response("Openai error", 400) 

        return jsonify({"message": openai_response["content"]}), 200

    except KeyError as e:
        # Handle specific KeyError issues
        return error_response(f"Key error: {str(e)}", 400)

    except Exception as e:
        # Handle unexpected errors
        return error_response(f"An unexpected error occurred: {str(e)}", 500)
      
        # Extract data from JSON payload
        data = request.get_json()
        
        if not data or 'prompt' not in data:
            return jsonify({"error": "Missing 'prompt' field in request"}), 400
        
        response = "je to ok"
        return response, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the server
if __name__ == '__main__':
    app.run(debug=True)
