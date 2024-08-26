#!/usr/bin/env python

import sys
import pandas as pd

def check_data(file_path):
    # Step 1: Read CSV file into a DataFrame
    df = pd.read_csv(file_path)

    # Step 2: Sort by src_subject_id, then interview_date in ascending order
    df['interview_date'] = pd.to_datetime(df['interview_date'], format='%m/%d/%y')
    df = df.sort_values(by=['src_subject_id', 'interview_date'])

    current_row = df.iloc[0]

    # Check if interview_age / 12 is an integer
    if current_row['interview_age'] % 12 != 0:
        print(f"Error in row {i}: interview_age {current_row['interview_age']} is not divisible by 12")

    # Step 3: Iterate over the rows and perform checks
    for i in range(1, len(df)):
        current_row = df.iloc[i]
        previous_row = df.iloc[i - 1]

        # Check if interview_age / 12 is an integer
        if current_row['interview_age'] % 12 != 0:
            print(f"Error in row {i}: interview_age {current_row['interview_age']} is not divisible by 12")

        # Check if src_subject_id is the same as the previous row
        if current_row['src_subject_id'] != previous_row['src_subject_id']:
            continue

        # Check if interview_age is the same for this row and the previous row
        if current_row['interview_age'] != previous_row['interview_age']:
            print(f"Error in row {i}: interview_age {current_row['interview_age']} differs from previous row's {previous_row['interview_age']} for src_subject_id {current_row['src_subject_id']}")

            # correct the interview_age such that it agrees with the first row
            df.at[i, 'interview_age'] = previous_row['interview_age']

        # Check if site starts with the same character as the previous row's site
        if current_row['site'] != previous_row['site']:
            print(f"Error in row {i}: site {current_row['site']} does not match previous row {previous_row['site']} for src_subject_id {current_row['src_subject_id']}")

    # write the corrected DataFrame to a new CSV file
    corrected_csv_file_path = file_path.replace(".csv", "_corrected.csv")
    df.to_csv(corrected_csv_file_path, index=False)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python check_data.py <csv_file_path>")
        sys.exit(1)

    csv_file_path = sys.argv[1]
    check_data(csv_file_path)

