from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from typing import List, Optional
import pandas as pd
import io
from app.utils.storage import storage
from app.models.schemas import (
    DataSourceListResponse, DataSourceMeta, 
    PreviewRequest, PreviewResponse,
    PreprocessRequest, PreprocessResponse
)
from app.services import cleaning
from app.services.parser import parse_user_command

router = APIRouter(prefix="/api/v1/data_sources", tags=["Data Sources"])

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.xlsx', '.xls')):
        raise HTTPException(status_code=400, detail="Only CSV/Excel files are allowed.")
    
    try:
        content = await file.read()
        file_size = len(content)
        
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        else:
            df = pd.read_excel(io.BytesIO(content))
        
        storage.save(file.filename, df, file_size)
        
        return {"message": "File uploaded successfully", "filename": file.filename}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/all", response_model=DataSourceListResponse)
def list_files():
    metadata_map = storage.list_all()
    files = []
    for filename, meta in metadata_map.items():
        files.append(DataSourceMeta(
            filename=filename,
            rows=meta["rows"],
            column_count=meta["column_count"],
            size=meta["size"],
            uploaded_at=meta["uploaded_at"]
        ))
    return DataSourceListResponse(files=files)

@router.get("/get-file/{filename}")
def get_file(filename: str):
    df = storage.get(filename)
    if df is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    # Return full data as JSON for the preview page table
    # Replace NaN with empty string
    data = df.fillna("").to_dict(orient="records")
    return {"filename": filename, "data": data}

@router.post("/preview", response_model=PreviewResponse)
def preview_preprocessing(request: PreviewRequest):
    df = storage.get(request.filename)
    if df is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    original_preview = df.head(5).fillna("").to_dict(orient="records")
    
    if not request.command:
        return PreviewResponse(
            original_preview=original_preview,
            preview=original_preview,
            metrics={"rows": len(df), "columns": len(df.columns)},
            diff_summary="No command provided."
        )

    # Apply command to a copy
    df_copy = df.copy()
    command = parse_user_command(request.command)
    action = command.get("action")
    
    diff_msg = "No styling applied."
    
    if action == "remove_nulls":
        df_copy = cleaning.remove_null_rows(df_copy)
        diff_msg = f"Removed {len(df) - len(df_copy)} rows with null values."
    elif action == "fill_mean":
        df_copy = cleaning.fill_missing_mean(df_copy)
        diff_msg = "Filled missing values with mean."
    elif action == "fill_median":
        df_copy = cleaning.fill_missing_median(df_copy)
        diff_msg = "Filled missing values with median."
    elif action == "remove_duplicates":
        df_copy = cleaning.remove_duplicates(df_copy)
        diff_msg = f"Removed {len(df) - len(df_copy)} duplicate rows."
    elif action == "drop_column":
        col_name = command.get("column")
        if col_name:
            df_copy = cleaning.drop_column(df_copy, col_name)
            diff_msg = f"Dropped column '{col_name}'."
    
    preview = df_copy.head(5).fillna("").to_dict(orient="records")
    
    return PreviewResponse(
        original_preview=original_preview,
        preview=preview,
        metrics={"rows": len(df_copy), "columns": len(df_copy.columns)},
        diff_summary=diff_msg
    )

@router.post("/preprocess", response_model=PreprocessResponse)
def apply_preprocessing(request: PreprocessRequest):
    df = storage.get(request.filename)
    if df is None:
        raise HTTPException(status_code=404, detail="File not found")
    
    command = parse_user_command(request.command)
    action = command.get("action")
    
    updated_df = df # Default if no action
    msg = "No action applied."
    
    if action == "remove_nulls":
        updated_df = cleaning.remove_null_rows(df)
        msg = "Removed null rows."
    elif action == "fill_mean":
        updated_df = cleaning.fill_missing_mean(df)
        msg = "Filled missing with mean."
    elif action == "fill_median":
        updated_df = cleaning.fill_missing_median(df)
        msg = "Filled missing with median."
    elif action == "remove_duplicates":
        updated_df = cleaning.remove_duplicates(df)
        msg = "Removed duplicates."
    elif action == "drop_column":
        col_name = command.get("column")
        if col_name:
            updated_df = cleaning.drop_column(df, col_name)
            msg = f"Dropped column {col_name}."
    
    # Save updated dataframe (overwriting for now, or could create new version)
    # Re-calculating size is approximate since we don't have bytes
    storage.save(request.filename, updated_df, file_size=0) 
    
    return PreprocessResponse(
        message=msg,
        rows=len(updated_df),
        columns=updated_df.columns.tolist(),
        preview=updated_df.head(5).fillna("").to_dict(orient="records")
    )
