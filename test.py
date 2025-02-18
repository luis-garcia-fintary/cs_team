import csv
import sys

def add_row_to_csv(input_csv, new_row_value, output_csv):
    """
    Adds a new row to the CSV file with the given value repeated for all columns.
    
    :param input_csv: Path to the input CSV file.
    :param new_row_value: The string to be repeated across the new row.
    :param output_csv: Path to save the modified CSV file.
    """
    try:
        # Read the CSV to determine the number of columns
        with open(input_csv, 'r', newline='') as file:
            reader = csv.reader(file)
            rows = list(reader)
            if not rows:
                print("Error: Input CSV is empty.")
                return
            num_columns = len(rows[0])
        
        # Create the new row
        new_row = [new_row_value] * num_columns
        
        # Write to the output CSV
        with open(output_csv, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)  # Write original data
            writer.writerow(new_row)  # Append new row
        
        print(f"Successfully added a new row to {output_csv}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python test.py <input_csv> <new_row_value> <output_csv>")
    else:
        add_row_to_csv(sys.argv[1], sys.argv[2], sys.argv[3])