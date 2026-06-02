# Dilution Calculator Web App (FastAPI) #

This web application provides a REST API and web interface for the dilution calculator.
It uses the same business logic from dilution_lib.py as the CLI and GUI applications.

This project takes the: Dilution Calculator "business logic" from Day 04, and expand it into a web based application using FastAPI.

## The project includes: ##
* **Web application** (`dilution_web_app.py`)
* **The original, "business logic" file** (`dilution_lib.py`) - the core calculations of Day04, based on the **C₁ × V₁ = C₂ × V₂** formula.
* **Test for the business logic** (`test_dilution_lib.py`)
* **Test for the app** (`test_dilution_web_app.py`)
* **The required installation** (`requirements.txt`)

## How to run: ##
### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Server
```bash
python -m uvicorn dilution_web_app:app --reload
```

### 3. Run Tests (Optional)
```bash
pytest -v
```

### 4. Access the Application
Open your browser and go to: **http://localhost:8000**


## AI: ##
