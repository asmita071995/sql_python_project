from flask import Flask, jsonify
from api import new_api  # Ensure this imports the correct module

# Create a Flask application instance
app = Flask(__name__)

# Define a route for inserting data
@app.route('/insert_data')
def insert_data():
    try:
        # Call the function to insert data
        insert_response = new_api.sql_func()  # Assuming sql_func inserts data here
        return jsonify({"message": insert_response})

    except Exception as e:
        # Handle any exceptions that might occur
        return jsonify({"error": str(e)}), 500


# Define a route for reading data
@app.route('/read_data')
def read_data():
    try:
        # Call the function from new_api to read data from the database
        data = new_api.sql_func()  # Ensure this function is for reading data
        return jsonify({"data": data})

    except Exception as e:
        # Handle any exceptions that might occur
        return jsonify({"error": str(e)}), 500

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
