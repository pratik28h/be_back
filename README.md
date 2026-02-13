# Data Cleaning Backend

## Overview
A rule-based data cleaning and insights generation backend using FastAPI, Pandas, and Matplotlib.

## Setup

1.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```

2.  Activate the virtual environment:
    - Windows: `venv\Scripts\activate`
    - Unix/MacOS: `source venv/bin/activate`

3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  Navigate to the `backend` directory:
    ```bash
    cd backend
    ```

2.  Start the server:
    ```bash
    uvicorn app.main:app --reload
    ```

## API Endpoints

-   `POST /upload`: Upload a CSV file.
-   `POST /chat`: Send cleaning commands.

## Architecture
-   **No AI/LLM**: All logic is rule-based.
-   **Modular Design**: Services, Routes, Models, Utils separated.
