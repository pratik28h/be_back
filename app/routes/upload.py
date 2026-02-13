from fastapi import APIRouter, UploadFile, File, HTTPException
import pandas as pd
import io
from app.utils.storage import storage

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are allowed.")
    
    try:
        content = await file.read()
        df = pd.read_csv(io.BytesIO(content))
        
        # Store in global storage under default key
        storage.save("current", df)
        
        columns = df.columns.tolist()
        rows = len(df)
        # Replace NaN with empty string for JSON serialization
        preview = df.head(5).fillna("").to_dict(orient="records")
        
        return {
            "columns": columns,
            "rows": rows,
            "preview": preview
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
