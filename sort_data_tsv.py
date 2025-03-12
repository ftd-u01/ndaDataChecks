#!/usr/bin/env python

import pandas as pd
import sys

def sort_ndar_tsv(input_file, output_file):
    # Load TSV file with all columns as strings
    df = pd.read_csv(input_file, sep='\t', dtype=str)

    # Keep the secondary header row as-is
    secondary_header = df.iloc[0]
    df = df.iloc[1:]

    # Ensure date parsing with the specified format "mm/dd/YYYY"
    df['interview_date'] = pd.to_datetime(df['interview_date'], format='%m/%d/%Y', errors='coerce')

    # Sort by "src_subject_id" first, then "interview_date"
    df = df.sort_values(by=['src_subject_id', 'interview_date'])

    # Convert date back to string in the original format
    df['interview_date'] = df['interview_date'].dt.strftime('%m/%d/%Y')

    # Reinsert the secondary header row at the top
    df = pd.concat([secondary_header.to_frame().T, df], ignore_index=True)

    # Write output TSV with quoted strings for all columns
    df.to_csv(output_file, sep='\t', index=False, quoting=1)

    print(f"Sorting completed. Output saved to {output_file}.")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python sort_ndar.py <input_file.tsv> <output_file.tsv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    sort_ndar_tsv(input_file, output_file)
