"""Data preprocessing utilities"""

import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List


def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV or Excel file"""
    if file_path.endswith('.csv'):
        return pd.read_csv(file_path)
    elif file_path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(file_path)
    else:
        raise ValueError(f"Unsupported file format: {file_path}")


def validate_data(df: pd.DataFrame, required_columns: List[str]) -> Dict[str, Any]:
    """Validate data and return quality report"""
    report = {
        "total_rows": len(df),
        "missing_columns": [col for col in required_columns if col not in df.columns],
        "missing_values": df.isna().sum().to_dict(),
        "duplicates": df.duplicated().sum(),
        "validation_errors": [],
    }

    # Check for missing required columns
    if report["missing_columns"]:
        report["validation_errors"].append({
            "type": "missing_columns",
            "columns": report["missing_columns"],
        })

    return report


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean data by handling missing values and inconsistencies"""
    # Remove duplicates
    df = df.drop_duplicates()

    # Standardize string columns
    for col in df.select_dtypes(include=['object']).columns:
        df[col] = df[col].str.strip().str.lower()

    return df


def split_data(
    df: pd.DataFrame,
    train_ratio: float = 0.8,
    random_state: int = 42
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Split data into train and test sets"""
    train = df.sample(frac=train_ratio, random_state=random_state)
    test = df.drop(train.index)
    return train, test