import openpyxl
import pandas as pd

# Define the path to the Excel file on your desktop in the folder "888/ScalpNet"
file_path = r'C:\Users\caden\Desktop\ScalpNetPrototype\data\ScalpNet v2 (With Futures Conversion).xlsm'
combined_csv_path = r'C:\Users\caden\Desktop\ScalpNetPrototype\data\options_data.csv'

def extract_data_from_excel():
    try:
        # Open the workbook in read-only mode using openpyxl
        wb = openpyxl.load_workbook(file_path, read_only=True, data_only=True)
        sheet = wb['Sheet1']  # Assuming the data is in 'Sheet1'

        # Read the headers from the 9th row and the data starting from the 10th row
        headers = [cell.value for cell in sheet[1]]
        data_rows = sheet.iter_rows(min_row=2, max_col=len(headers), max_row=18)
        data = [[cell.value for cell in row] for row in data_rows]

        # Close the read-only workbook
        wb.close()

        # Create a pandas DataFrame from the rows
        df = pd.DataFrame(data, columns=headers)

        # Export to CSV file on the desktop in the same folder structure
        combined_csv_path = r'C:\Users\caden\Desktop\ScalpNetPrototype\data\options_data.csv'

        df.to_csv(combined_csv_path, index=False)

        print("Combined options data CSV file has been successfully created at:", combined_csv_path)

    except FileNotFoundError:
        print("Error: The file was not found. Please check the path:", file_path)

    except Exception as e:
        print(f"An error occurred: {e}")
