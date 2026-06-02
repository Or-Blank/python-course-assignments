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

### 2. Start the web server
```bash
python -m uvicorn dilution_web_app:app --reload
```

### 3. Run tests (not needed everytime)
```bash
pytest -v
```

### 4. Enter the app
Open your browser and go to: **http://localhost:8000**


## AI: ##
I used for this task the built in Copilot of VS and ChatGPT:
* My main prompt in ChatGPT was: "I want to create an app based on my Day04 core code (I will provide after that).Do not use Flask and reccommend on another tool to accomplish this task and the diffrences. Also add tests for the core code and the app and make sure to not change anything on the orignial one and use it as the source/import for the web app".
* After that I used the Copilot in order to fix problems I had: The "cosmetics" of the app and problems I had with the loading of the web server.
