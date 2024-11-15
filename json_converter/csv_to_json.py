import pandas as pd

def convert_csv_to_json():
    
    # Read the CSV file into a DataFrame
    df = pd.read_csv('/home/dhyanendra/Downloads/titanic/tested.csv')
    
    # Convert the DataFrame to JSON format
    data = df.to_json(orient='records')
    
    # Save the JSON data to a file
    with open('output.json', 'w') as json_file:
        json_file.write(data)
    
    return data
