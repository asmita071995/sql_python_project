import pandas as pd
from io import BytesIO

def convert_csv_to_excel():
    # Read the uploaded CSV file into a DataFrame
    file = '/home/dhyanendra/Downloads/titanic/tested.csv'
    excel_file_path = '/home/dhyanendra/Desktop/output_file.xlsx'
    df = pd.read_csv(file)
  
    # Create a BytesIO buffer to store the Excel file in memory
    output = BytesIO()

    # Create a copy of the DataFrame (df1)
    df1 = df.copy()

    # Use pd.ExcelWriter to save both DataFrames into different sheets
    with pd.ExcelWriter(excel_file_path, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name="Sheet1", index=False)
        df1.to_excel(writer, sheet_name="Sheet2", index=False)

    # Seek to the beginning of the BytesIO buffer before sending it
    output.seek(0)

    return output
