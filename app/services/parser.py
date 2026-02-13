from typing import Dict, Any
import re

def parse_user_command(message: str) -> Dict[str, Any]:
    """
    Parses natural language commands using rule-based logic.
    Returns a dictionary with 'action' and optionally 'column'.
    """
    msg = message.lower().strip()

    if "remove" in msg and "null" in msg:
        return {"action": "remove_nulls"}

    if "fill" in msg and "mean" in msg:
        return {"action": "fill_mean"}

    if "fill" in msg and "median" in msg:
        return {"action": "fill_median"}

    if "duplicate" in msg:
        return {"action": "remove_duplicates"}

    if "drop column" in msg or "remove column" in msg:
        # Simplistic extraction: look for words after "column"
        # Example: "drop column age" -> "age"
        # We might need to be a bit smarter or just take the last word.
        # Let's try to find the word after "column "
        match = re.search(r"(?:drop|remove)\s+column\s+(\w+)", msg)
        if match:
            column_name = match.group(1)
            return {"action": "drop_column", "column": column_name}
        
        # Fallback if regex fails but command is present
        # logic: split by space, find 'column', take next word
        parts = msg.split()
        try:
            col_idx = parts.index("column") + 1
            if col_idx < len(parts):
                return {"action": "drop_column", "column": parts[col_idx]}
        except ValueError:
            pass

    return {"action": "unknown"}
