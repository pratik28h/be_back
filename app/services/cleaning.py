import pandas as pd

def remove_null_rows(df: pd.DataFrame) -> pd.DataFrame:
    """Removes rows with any missing values."""
    return df.dropna().copy()

def fill_missing_mean(df: pd.DataFrame) -> pd.DataFrame:
    """Fills missing values with the mean of the column (numeric only)."""
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=['number']).columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].mean())
    return df_clean

def fill_missing_median(df: pd.DataFrame) -> pd.DataFrame:
    """Fills missing values with the median of the column (numeric only)."""
    df_clean = df.copy()
    numeric_cols = df_clean.select_dtypes(include=['number']).columns
    df_clean[numeric_cols] = df_clean[numeric_cols].fillna(df_clean[numeric_cols].median())
    return df_clean

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Removes duplicate rows."""
    return df.drop_duplicates().copy()

def drop_column(df: pd.DataFrame, column_name: str) -> pd.DataFrame:
    """Drops a specific column if it exists."""
    if column_name in df.columns:
        return df.drop(columns=[column_name]).copy()
    return df.copy()
