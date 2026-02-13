import matplotlib.pyplot as plt
import pandas as pd
import os
import uuid

OUTPUT_DIR = "outputs"

def generate_charts(df: pd.DataFrame) -> list[str]:
    """
    Generates histograms for numeric columns and bar charts for categorical columns.
    Saves images to 'outputs/' and returns list of filenames.
    """
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    chart_files = []
    
    # Numeric columns - Histograms
    numeric_cols = df.select_dtypes(include=['number']).columns
    for col in numeric_cols:
        plt.figure()
        df[col].hist()
        plt.title(f"Distribution of {col}")
        plt.xlabel(col)
        plt.ylabel("Frequency")
        
        filename = f"{uuid.uuid4()}_{col}_hist.png"
        filepath = os.path.join(OUTPUT_DIR, filename)
        plt.savefig(filepath)
        plt.close()
        chart_files.append(filepath)

    # Categorical columns - Bar/Count plots
    # Limit to top 10 categories to avoid clutter
    cat_cols = df.select_dtypes(include=['object', 'category']).columns
    for col in cat_cols:
        # Check unique count. If too many, maybe skip or take top 10
        validation_counts = df[col].value_counts().nlargest(10)
        
        if not validation_counts.empty:
            plt.figure()
            validation_counts.plot(kind='bar')
            plt.title(f"Top 10 categories in {col}")
            plt.xlabel(col)
            plt.ylabel("Count")
            plt.tight_layout() # Adjust layout to make room for labels
            
            filename = f"{uuid.uuid4()}_{col}_bar.png"
            filepath = os.path.join(OUTPUT_DIR, filename)
            plt.savefig(filepath)
            plt.close()
            chart_files.append(filepath)
            
    return chart_files
