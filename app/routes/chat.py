from fastapi import APIRouter, HTTPException
from app.models.schemas import ChatRequest, ChatResponse
from app.utils.storage import storage
from app.services.parser import parse_user_command
from app.services import cleaning
from app.services.insights import generate_insights
from app.services.charts import generate_charts

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    df = storage.get("current")
    if df is None:
        raise HTTPException(status_code=400, detail="No CSV file uploaded. Please upload a file first.")
    
    command = parse_user_command(request.message)
    action = command.get("action")
    
    response_msg = ""
    updated_df = df
    
    # Execute Action
    if action == "remove_nulls":
        updated_df = cleaning.remove_null_rows(df)
        response_msg = "Removed rows with null values."
    elif action == "fill_mean":
        updated_df = cleaning.fill_missing_mean(df)
        response_msg = "Filled missing values with column mean."
    elif action == "fill_median":
        updated_df = cleaning.fill_missing_median(df)
        response_msg = "Filled missing values with column median."
    elif action == "remove_duplicates":
        updated_df = cleaning.remove_duplicates(df)
        response_msg = "Removed duplicate rows."
    elif action == "drop_column":
        col_name = command.get("column")
        if col_name:
            updated_df = cleaning.drop_column(df, col_name)
            response_msg = f"Dropped column '{col_name}'."
        else:
            response_msg = "Column name not specified."
    elif action == "unknown":
        return ChatResponse(message="I didn't understand that command. Try 'remove nulls', 'fill mean', 'drop column [name]', etc.")
    
    # Save updated dataframe
    storage.save("current", updated_df)
    
    # Generate Insights & Charts
    # Insights implementation returns a string, but the schema has strict fields.
    # The user asked for "insights as plain English text". 
    # But the ChatResponse schema in request description didn't strictly require an 'insights' field,
    # just {"message": "Cleaning applied", "preview": ..., "rows": ..., "columns": ...}
    # However, Requirement 5 says "Return insights as plain English text generated manually".
    # I should probably append insights to the message or add an insights field.
    # The requirement 4 "Chat Endpoint" return structure didn't show 'insights' field explicitly but requirement 5 implies it.
    # I will append it to the 'message' or add it to the schema.
    # Let's append to message for now to match the "Return... as text" request and keep schema simple as per Req 4 example.
    # Wait, Req 4 example: {"message": "Cleaning applied", ...}
    # Req 5 example: "Return insights as plain English text... for example 'Column age has...'"
    # I'll append it to the message.
    
    insights_text = generate_insights(updated_df)
    chart_paths = generate_charts(updated_df)
    
    full_message = f"{response_msg}\n\nInsights:\n{insights_text}"
    
    return ChatResponse(
        message=full_message,
        preview=updated_df.head(5).to_dict(orient="records"),
        rows=len(updated_df),
        columns=updated_df.columns.tolist(),
        charts=chart_paths
    )
