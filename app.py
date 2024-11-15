from flask import Flask, abort, jsonify, request, send_file
from api import new_api
from read_data import read
from functools import wraps
from plots import plots
from file_converters import file_converter
from json_converter import csv_to_json

app = Flask(__name__)
app.config.from_object("config.ProdConfig")
def require_api_key(view_function):
    """Verifies that API key is included in header request, else 401 unauthorized"""
    @wraps(view_function)
    def decorated_function(*args, **kwargs):
        # Check if the 'api_key' header matches the API_KEY in the config
        if request.headers.get("api_key") == app.config.get("API_KEY"):
            return view_function(*args, **kwargs)
        else:
            # Return 401 Unauthorized if the API key is missing or incorrect
            abort(401)
    return decorated_function

# Inserting data
@app.route('/insert_data')
@require_api_key
def insert_data():
    """
    Inserts data into the database.
    This endpoint calls the `sql_func` function from the `new_api` module,
    which handles the database insertion logic.
    Returns a success message or an error message if something goes wrong.
    """
    try:
        insert_response = new_api.sql_func()
        return jsonify({"message": insert_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Reading data
@app.route('/read_data')
@require_api_key
def read_data():
    """
    Reads data from the database.
    This endpoint calls the `read` function from the `read_data` module,
    which retrieves the required information from the database.
    Returns the data in JSON format or an error message.
    """
    try:
        data = read.read()
        return jsonify({"data": data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CSV to JSON conversion
@app.route('/convert_csv_to_json', methods=['POST'])
@require_api_key
def convert_csv_to_json_endpoint():
    """
    Converts a CSV file to JSON format.
    This endpoint uses the `convert_csv_to_json` function from the `csv_to_json` module.
    It processes a hardcoded or uploaded CSV file and converts it into a JSON string.
    Returns the JSON data or an error message.
    """
    try:
        json_data = csv_to_json.convert_csv_to_json()
        return jsonify({"data": json_data})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Processing Titanic data
@app.route('/process_titanic_data', methods=['POST'])
@require_api_key
def process_titanic_data_endpoint():
    """
    Processes Titanic dataset information.
    This endpoint accepts JSON data in the request body and passes it to the
    `process_titanic_data` function from the `process_data` module for processing.
    Returns the processed result in JSON format or an error message.
    """
    from process_data import process
    try:
        data = request.get_json()
        result = process.process_titanic_data(data)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Generating plots
@app.route('/generate_plots', methods=['POST'])
@require_api_key
def generate_plots_endpoint():
    """
    Generates plots from data.
    This endpoint accepts JSON data in the request body and passes it to the
    `generate_plots` function in the `plots` module.
    Returns the generated plot as an image file or an error message.
    """
    try:
        data = request.get_json()
        img_buffer = plots.generate_plots(data)
        return send_file(img_buffer, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# CSV to Excel conversion
@app.route('/convert_csv_to_excel', methods=['POST'])
@require_api_key
def convert_csv_to_excel_endpoint():
    """
    Converts a CSV file to an Excel file.
    This endpoint uses the `convert_csv_to_excel` function from the `file_converter` module.
    It processes a hardcoded or uploaded CSV file and converts it into an Excel file with multiple sheets.
    Returns the Excel file as a downloadable response or an error message.
    """
    try:
        output = file_converter.convert_csv_to_excel()
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='converted_file.xlsx'
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    """
    Main entry point of the Flask application.
    Starts the Flask server with debug mode enabled.
    If an error occurs while starting the app, it prints the error message.
    """
    try:
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting the app: {e}")

