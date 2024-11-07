import pandas as pd
from sqlalchemy import create_engine, inspect, text
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Fetch database credentials from environment variables
username = os.getenv("username")
password = os.getenv("password")
host = os.getenv("host")
database = os.getenv("database")

def read():

   # Check if any credentials are missing
    if not all([username, password, host, database]):
        print("Error: Missing one or more environment variables.")
        return "Error: Missing database credentials."

    # Create the connection URL
    connection_url = f"mysql+pymysql://{username}:{password}@{host}/{database}"

    # Create the SQLAlchemy engine
    engine = create_engine(connection_url)

    # Use the inspector to check if the table exists
    inspector = inspect(engine)
    tables = inspector.get_table_names()

  

    # Fetch data from 'tested' table and save it to a CSV file
    try:
        query = text("SELECT * FROM tested")
        df_tested = pd.read_sql(query, con=engine)
        
        # Specify the CSV file path to save the data
        output_csv_path = '/home/dhyanendra/Downloads/titanic/tested.csv'
        
        # Export data to CSV
        df_tested.to_csv(output_csv_path, index=False)
        print("Data retrieved and saved to CSV successfully.")
        
        return f"Data retrieved and saved to {output_csv_path}"
    
    except Exception as e:
        print(f"Error during data retrieval: {e}")
        return f"Error during data retrieval: {e}"
