import pandas as pd
import sys

def check_consistency(reference_file, file_to_check, output_file='output.csv'):
    # Load the CSV files into pandas DataFrames
    reference_df = pd.read_csv(reference_file)
    check_df = pd.read_csv(file_to_check)

    # Define the columns to check for consistency
    columns_to_check = ["subjectkey", "src_subject_id", "interview_date", "interview_age", "sex"]

    # Create a set of tuples for quick lookup
    reference_set = set([tuple(row) for row in reference_df[columns_to_check].values])

    # Function to check if row exists in reference set
    def is_consistent(row):
        return tuple(row) in reference_set

    # Apply the consistency check
    check_df["info_consistent"] = check_df[columns_to_check].apply(is_consistent, axis=1)

    # Save the result to a new CSV file
    check_df.to_csv(output_file, index=False)
    print(f"Consistency check completed. Results saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_demographics.py <reference_file.csv> <file_to_check.csv>")
        sys.exit(1)

    reference_file = sys.argv[1]
    file_to_check = sys.argv[2]

    check_consistency(reference_file, file_to_check)

