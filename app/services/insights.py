import pandas as pd
import numpy as np

def generate_insights(df: pd.DataFrame) -> str:
    """
    Generates plain English insights about the DataFrame.
    """
    insights = []
    
    # Basic info
    num_rows, num_cols = df.shape
    insights.append(f"The dataset contains {num_rows} rows and {num_cols} columns.")
    
    # Missing values
    missing_counts = df.isnull().sum()
    missing_cols = missing_counts[missing_counts > 0]
    
    if not missing_cols.empty:
        insights.append("Missing values found:")
        for col, count in missing_cols.items():
            insights.append(f"- Column '{col}' has {count} missing values.")
    else:
        insights.append("No missing values found in the dataset.")
        
    # Numeric column stats
    numeric_df = df.select_dtypes(include=[np.number])
    if not numeric_df.empty:
        insights.append("\nNumeric Column Statistics:")
        for col in numeric_df.columns:
            mean_val = numeric_df[col].mean()
            min_val = numeric_df[col].min()
            max_val = numeric_df[col].max()
            insights.append(f"- '{col}': Mean = {mean_val:.2f}, Range = [{min_val}, {max_val}].")
            
        # Correlation (if > 1 numeric col)
        if len(numeric_df.columns) > 1:
            corr_matrix = numeric_df.corr()
            # simple logic: find high correlations
            high_corr = []
            for i in range(len(corr_matrix.columns)):
                for j in range(i+1, len(corr_matrix.columns)):
                    val = corr_matrix.iloc[i, j]
                    if abs(val) > 0.7:
                        col1 = corr_matrix.columns[i]
                        col2 = corr_matrix.columns[j]
                        high_corr.append(f"{col1} and {col2} ({val:.2f})")
            
            if high_corr:
                insights.append(f"\nStrong correlations found between: {', '.join(high_corr)}.")
    
    return "\n".join(insights)
