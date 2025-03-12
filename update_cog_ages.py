#!/usr/bin/env python

import pandas as pd
import sys

def fix_tsv_file(ndar_subject01, file_to_fix, output_file, log_file):
    # Load TSV files
    ndar_df = pd.read_csv(ndar_subject01, sep='\t', dtype=str)
    fix_df = pd.read_csv(file_to_fix, sep='\t', dtype=str)

    # Extract unique reference interview ages
    ref_ages = ndar_df.groupby("subjectkey")[["interview_age"]].first().to_dict()["interview_age"]

    log_entries = []

    # Iterate over file_to_fix and correct interview_age if needed
    for index, row in fix_df.iterrows():
        subject = row["subjectkey"]
        if subject in ref_ages:
            ref_interview_age = ref_ages[subject]
            if row["interview_age"] != ref_interview_age:
                fix_df.at[index, "interview_age"] = ref_interview_age
                log_entries.append(f'"{subject}"\t"Updated"')
            else:
                log_entries.append(f'"{subject}"\t"NotUpdated"')

    # Write output TSV with quotes
    fix_df.to_csv(output_file, sep='\t', index=False, quoting=1)

    # Write log file with quotes
    with open(log_file, 'w') as log_f:
        log_f.write("\"subjectkey\"\t\"status\"\n")
        log_f.write("\n".join(log_entries) + "\n")

    print(f"File correction completed. Output saved to {output_file}, log saved to {log_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage: python fix_tsv.py <ndar_subject01.tsv> <file_to_fix.tsv> <output_file.tsv> <log_file.tsv>")
        sys.exit(1)

    ndar_subject01 = sys.argv[1]
    file_to_fix = sys.argv[2]
    output_file = sys.argv[3]
    log_file = sys.argv[4]

    fix_tsv_file(ndar_subject01, file_to_fix, output_file, log_file)

