from flask import Flask, abort, jsonify, request
from api import new_api  # Ensure this imports the correct module
from read_data import read
from functools import wraps
from plots import generate_plots
from plots import graph

app = Flask(__name__)


app.config.from_object("config.ProdConfig")

def require_api_key(view_function):
    """
    verifies that API key is included in header request, else 401 unauthorized
    """

    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        if request.headers.get("api_key") and (request.headers.get("api_key")) == app.config.get("API_KEY"):
            return view_function(*args, **kwargs)
        else:
            abort(401)

    return decorated_function

# Define a route for inserting data
@app.route('/insert_data')
@require_api_key
def insert_data():
    try:
        # Call the function to insert data
        insert_response = new_api.sql_func()
        return jsonify({"message": insert_response})

    except Exception as e:
        # Handle any exceptions that might occur
        return jsonify({"error": str(e)}), 500

# Define a route for reading data
@app.route('/read_data')
@require_api_key
def read_data():
    try:
        # Call the function to read data from the database
        data = read.read()
        return jsonify({"data": data})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Define a new route for processing Titanic data
@app.route('/process_titanic_data', methods=['POST'])
@require_api_key
def process_titanic_data_endpoint():
    from process_data import process  
    try:
        # Get the JSON data from the request
        data = request.get_json()
        # Process the data using the imported function
        result = process.process_titanic_data(data)
        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@app.route('/generate_plots', methods=['GET'])
@require_api_key
def generate_plots_endpoint():
    try:
        
        data = request.get_json()

        # Call the function in plots.py to generate plots
        img_buffer = generate_plots(data)

        # Return the image as a response
        return send_file(img_buffer, mimetype='image/png')

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
