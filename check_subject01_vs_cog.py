#!/usr/bin/env python

import pandas as pd
import sys
from datetime import datetime, timedelta

def check_consistency(reference_file, file_to_check, output_file='consistency.csv'):
    # Load CSV files with all columns as strings to preserve formatting
    reference_df = pd.read_csv(reference_file, dtype=str)
    check_df = pd.read_csv(file_to_check, dtype=str)


    date_format = "%m/%d/%Y"
    reference_df['interview_date'] = pd.to_datetime(reference_df['interview_date'], format=date_format, errors='coerce')
    check_df['interview_date'] = pd.to_datetime(check_df['interview_date'], format=date_format, errors='coerce')

    columns_to_check = ["subjectkey", "src_subject_id", "interview_age", "sex"]

    # Extract unique subjects
    subjects = reference_df['subjectkey'].unique()
    results = []

    for subject in subjects:
        subj_ref_df = reference_df[reference_df['subjectkey'] == subject].sort_values(by='interview_date')
        subj_check_df = check_df[check_df['subjectkey'] == subject].sort_values(by='interview_date')

        src_subject_id = subj_ref_df['src_subject_id'].iloc[0]

        # If the number of rows doesn't match, check internal consistency of subj_check_df
        if len(subj_ref_df) != len(subj_check_df):

            # Missing cog
            if len(subj_check_df) == 0:
                results.append(f"{subject},{src_subject_id},NoCogSession")
                continue

            internal_mismatches = []
            for col in columns_to_check:
                if subj_check_df[col].nunique() > 1:
                    internal_mismatches.append(col)

            if internal_mismatches:
                results.append(f"{subject},{subj_check_df['src_subject_id'].iloc[0]},InternalDemogError:{'/'.join(internal_mismatches)}")
                continue

            # Compare the first row of subj_check_df with the first row of subj_ref_df
            first_row_mismatches = []
            for col in columns_to_check:
                if subj_ref_df[col].iloc[0] != subj_check_df[col].iloc[0]:
                    first_row_mismatches.append(col)

            if first_row_mismatches:
                results.append(f"{subject},{subj_check_df['src_subject_id'].iloc[0]},FirstRowDemogError:{'/'.join(first_row_mismatches)}")
            else:
                results.append(f"{subject},{subj_check_df['src_subject_id'].iloc[0]},MissingOrExtraCogSessions")
            continue

        # Compare non-date fields individually
        mismatches = []
        for col in columns_to_check:
            if not subj_ref_df[col].reset_index(drop=True).equals(subj_check_df[col].reset_index(drop=True)):
                mismatches.append(col)

        if mismatches:
            results.append(f"{subject},{subj_ref_df['src_subject_id'].iloc[0]},DemogError:{'/'.join(mismatches)}")
            continue

        # Check interview_date within nine months
        max_diff = timedelta(days=9 * 30)  # Approximate nine months
        date_diffs = (subj_check_df['interview_date'].reset_index(drop=True) -
                      subj_ref_df['interview_date'].reset_index(drop=True)).abs()
        if (date_diffs > max_diff).any():
            results.append(f"{subject},{src_subject_id},CogDateOutOfRange")
        else:
            results.append(f"{subject},{src_subject_id},OK")

    # Write results to output file
    with open(output_file, 'w') as f:
        f.write("subjectkey,src_subject_id,status\n")
        f.write("\n".join(results) + "\n")

    print(f"Consistency check completed. Results saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python check_demographics.py <reference_file.csv> <file_to_check.csv>")
        sys.exit(1)

    reference_file = sys.argv[1]
    file_to_check = sys.argv[2]

    check_consistency(reference_file, file_to_check)

