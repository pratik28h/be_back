import pandas as pd
from typing import Dict, Optional, Any
from datetime import datetime

class DataFrameStorage:
    def __init__(self):
        # Stores DataFrames: {"filename": dataframe}
        self._store: Dict[str, pd.DataFrame] = {}
        # Stores Metadata: {"filename": {"rows": int, "cols": int, "size": int, "uploaded_at": str}}
        self._metadata: Dict[str, Dict[str, Any]] = {}

    def save(self, key: str, df: pd.DataFrame, file_size: int = 0):
        self._store[key] = df
        self._metadata[key] = {
            "rows": len(df),
            "columns": df.columns.tolist(),
            "column_count": len(df.columns),
            "size": file_size,
            "uploaded_at": datetime.now().isoformat()
        }

    def get(self, key: str) -> Optional[pd.DataFrame]:
        return self._store.get(key)
    
    def get_metadata(self, key: str) -> Optional[Dict[str, Any]]:
        return self._metadata.get(key)

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        return self._metadata
    
    def exists(self, key: str) -> bool:
        return key in self._store

# Global instance
storage = DataFrameStorage()
