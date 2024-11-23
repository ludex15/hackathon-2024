from flask import Flask, request, jsonify

app = Flask(__name__)

# Endpoint to handle free text data
@app.route('/api/prompt', methods=['POST'])
def process_text():
    try:
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
