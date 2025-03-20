import pandas as pd
import numpy as np
import re


def read_data(file_path):
    """
    Reads data from a CSV file.

    Parameters:
    file_path (str): Path to the CSV file.

    Returns:
    pd.DataFrame: Dataframe containing the read data.
    """
    return pd.read_csv(file_path, sep=",", encoding="latin1", nrows=500)


def check_missing_values(df):
    """
    Checks for missing values and fills them with 'unknown'.

    Parameters:
    df (pd.DataFrame): Input dataframe.

    Returns:
    pd.DataFrame: Dataframe with missing values handled.
    """
    missing_values = df.isnull().sum()
    print(f"Missing values:\n{missing_values[missing_values > 0]}")
    return df.fillna("unknown")


def check_duplicates(df):
    """
    Identifies and removes duplicate records.

    Parameters:
    df (pd.DataFrame): Input dataframe.

    Returns:
    pd.DataFrame: Dataframe with duplicates removed.
    """
    duplicates = df[df.duplicated()]
    if not duplicates.empty:
        print(f"Found {len(duplicates)} duplicate rows. Removing...")
        df = df.drop_duplicates()
    return df


def check_data_types(df, expected_dtypes):
    """
    Validates the datatypes of the dataframe columns against the expected datatypes.

    Parameters:
    df (pd.DataFrame): Input dataframe.
    expected_dtypes (dict): Dictionary with column names as keys and expected data types as values.

    Returns:
    bool: True if all column types match, False otherwise.
    dict: Dictionary of mismatched columns with actual and expected data types.
    """
    mismatches = {
        col: (df[col].dtype, expected_dtypes[col])
        for col in expected_dtypes
        if col in df.columns and df[col].dtype != expected_dtypes[col]
    }
    return len(mismatches) == 0, mismatches


def check_outliers(df, column_name, min_val, max_val):
    """
    Identifies and removes outliers in a specified column.

    Parameters:
    df (pd.DataFrame): Input dataframe.
    column_name (str): Column to check for outliers.
    min_val (float): Minimum acceptable value.
    max_val (float): Maximum acceptable value.

    Returns:
    pd.DataFrame: Dataframe with outliers removed.
    """
    outliers = df[(df[column_name] < min_val) | (df[column_name] > max_val)]
    if not outliers.empty:
        print(f"Outliers detected in column {column_name}. Removing...")
        df = df[~df[column_name].isin(outliers[column_name])]
    return df


def validate_signature(df, column_name, pattern):
    """
    Validates column values based on a regex pattern.

    Parameters:
    df (pd.DataFrame): Input dataframe.
    column_name (str): Column to validate.
    pattern (str): Regular expression pattern.

    Returns:
    pd.DataFrame: Dataframe with invalid entries removed.
    """
    invalid_entries = df[~df[column_name].astype(str).str.match(pattern, na=False)]
    if not invalid_entries.empty:
        print(f"Invalid entries in {column_name}:\n{invalid_entries}")
        df = df[~df[column_name].isin(invalid_entries[column_name])]
    return df


def check_cross_column_dependency(df):
    """
    Checks cross-column dependency where 'whisky' should always be less than 'spirits'.

    Parameters:
    df (pd.DataFrame): Input dataframe.

    Returns:
    pd.DataFrame: Dataframe with invalid dependencies removed.
    """
    if "whisky" in df.columns and "spirits" in df.columns:
        invalid_rows = df[df["whisky"] > df["spirits"]]
        if not invalid_rows.empty:
            print(
                f"Invalid cross-column dependency in whisky and spirits:\n{invalid_rows}"
            )
            df = df[~df["whisky"].isin(invalid_rows["whisky"])]
    return df


def check_inconsistent_data_entry(df):
    """
    Checks for inconsistent data entries in 'SAPPHL6Description'.

    Parameters:
    df (pd.DataFrame): Input dataframe.

    Returns:
    pd.DataFrame: Dataframe with inconsistent entries removed.
    """
    inconsistent = df[~df["SAPPHL6Description"].isin(["litres", "ml"])]
    if not inconsistent.empty:
        print(f"Inconsistent entries in SAPPHL6Description:\n{inconsistent}")
        df = df[~df["SAPPHL6Description"].isin(inconsistent["SAPPHL6Description"])]
    return df


def standardize_data(df):
    """
    Standardizes dataframe column names.

    Parameters:
    df (pd.DataFrame): Input dataframe.

    Returns:
    pd.DataFrame: Dataframe with standardized column names.
    """
    df.columns = [col.strip().lower() for col in df.columns]
    return df


def write_to_destination(df, output_file):
    """
    Writes cleaned data to a CSV file.

    Parameters:
    df (pd.DataFrame): Dataframe to be written.
    output_file (str): Destination file path.
    """
    df.to_csv(output_file, index=False)
    print(f"Cleaned data written to {output_file}")
