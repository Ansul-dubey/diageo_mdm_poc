import sys
import os

# Add parent direcotry to search path
CURRENT_DIR = os.getcwd()
PARENT_DIR = os.path.abspath(os.path.join(CURRENT_DIR))
sys.path.append(PARENT_DIR)

from src.config import *
from src.utility import *


def main():
    """Main function to execute data processing pipeline."""
    file1 = INPUT_PATH_FILE_FRB  # Input file 1
    file2 = INPUT_PATH_FILE_MARKETING  # Input file 2
    output_file = OUTPUT_FILE_PATH  # Output file for cleaned data

    df_frbv = read_data(os.path.join(PARENT_DIR, file1))
    df_marketing = read_data(os.path.join(PARENT_DIR, file2))

    # Data quality checks
    df_frbv = check_missing_values(df_frbv)
    df_marketing = check_missing_values(df_marketing)

    df_frbv = check_duplicates(df_frbv)
    df_marketing = check_duplicates(df_marketing)

    # Validate schema
    frb_is_valid, frb_mismatched = check_data_types(df_frbv, FRB_SCHEMA_SOURCE)
    print(
        f"FRB data type validation: {frb_is_valid}, Mismatched columns: {frb_mismatched}"
    )

    m_is_valid, m_mismatched = check_data_types(df_marketing, MARKETING_SCHEMA_SOURCE)
    print(
        f"Marketing data type validation: {m_is_valid}, Mismatched columns: {m_mismatched}"
    )

    # Standardize data
    df_frbv = standardize_data(df_frbv)
    df_marketing = standardize_data(df_marketing)

    # Write cleaned data to output destination
    write_to_destination(df_frbv, output_file)
    write_to_destination(df_marketing, output_file.replace(".csv", "_marketing.csv"))


if __name__ == "__main__":
    main()
