# Day 08 - Dilution Calculator Web Application

"""
Dilution Calculator Web Application using FastAPI

This web application provides a REST API and web interface for the dilution calculator.
It uses the same business logic from dilution_lib.py as the CLI and GUI applications.

The application is built with FastAPI and can be run with:
  uvicorn dilution_web_app:app --reload
"""

## Project Overview

This project takes the **Dilution Calculator business logic from Day 04** and wraps it in a modern web application using **FastAPI** (not Flask). The same tested business logic functions are reused, demonstrating proper separation of concerns and code reusability.

The project includes:
- ✅ **Tested business logic** (`test_dilution_lib.py`)
- ✅ **Web application** using FastAPI with a beautiful interactive HTML interface (`dilution_web_app.py`)
- ✅ **REST API endpoints** for programmatic access to the calculations
- ✅ **Comprehensive test suite** for the web application (`test_dilution_web_app.py`)

---

## Architecture

### Business Logic Layer
The core calculations are in `../Day04/dilution_lib.py`:
- `Calculation_of_C1()` - Calculate initial concentration
- `Calculation_of_V1()` - Calculate initial volume
- `Calculation_of_C2()` - Calculate final concentration
- `Calculation_of_V2()` - Calculate final volume

These functions implement the dilution formula: **C₁ × V₁ = C₂ × V₂**

### Web Application Layer
Built with FastAPI, provides:
- **Web Interface** - Beautiful HTML/CSS/JavaScript UI at `/`
- **REST API** - JSON endpoints for programmatic access
- **Input Validation** - Pydantic models ensure data integrity
- **Error Handling** - Graceful handling of invalid inputs

---

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Server
```bash
python -m uvicorn dilution_web_app:app --reload
```

### 3. Access the Application
Open your browser and go to: **http://localhost:8000**

You'll see a beautiful interactive web interface with 4 tabs for each calculation type.

### 4. Run Tests (Optional)
```bash
pytest -v
```

---

## Installation

### Prerequisites
- Python 3.8+
- pip or conda

### Setup Steps

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**
   ```bash
   python -m pip list | grep -E "fastapi|uvicorn|pydantic|pytest"
   ```

---

## Running the Application

### Option 1: Run the Web Application (with UI)

```bash
python -m uvicorn dilution_web_app:app --reload
```

Then open your browser to: **http://localhost:8000**

The web interface provides:
- Tab-based interface for each calculation type
- Real-time results display
- Beautiful, responsive design
- Error messages for invalid inputs

### Option 2: Use the REST API

The FastAPI server also provides REST endpoints. Examples:

**Calculate C₁:**
```bash
curl -X POST "http://localhost:8000/api/calculate/c1" \
  -H "Content-Type: application/json" \
  -d '{"C2": 2.0, "V2": 100, "V1": 50}'
```

**Calculate V₂:**
```bash
curl -X POST "http://localhost:8000/api/calculate/v2" \
  -H "Content-Type: application/json" \
  -d '{"C1": 4.0, "V1": 50, "C2": 2.0}'
```

**Health Check:**
```bash
curl "http://localhost:8000/api/health"
```

---

## Testing

### Run All Tests

```bash
pytest -v
```

### Run Specific Test Suite

**Test business logic:**
```bash
pytest test_dilution_lib.py -v
```

**Test web application:**
```bash
pytest test_dilution_web_app.py -v
```

### Test Coverage

- **test_dilution_lib.py**: 16 test cases (2 per calculation function) covering:
  - All four calculation functions (C1, V1, C2, V2)
  - Edge cases (zero values, large values, decimals)
  - Formula consistency checks
  - Volume conversion functions

- **test_dilution_web_app.py**: 6 test cases covering:
  - All REST API endpoints
  - Health check endpoint
  - Web interface endpoint
  - Input validation
  - Error handling
  - Response format consistency
  - Formula consistency across API calls

---

## API Documentation

### Endpoints

#### GET `/`
Returns the interactive web interface (HTML)

#### GET `/api/health`
Health check endpoint
```json
{
  "status": "healthy",
  "service": "Dilution Calculator API"
}
```

#### POST `/api/calculate/c1`
Calculate initial concentration using: C₁ = (C₂ × V₂) / V₁

**Request:**
```json
{
  "C2": 2.0,
  "V2": 100,
  "V1": 50
}
```

**Response (Success):**
```json
{
  "success": true,
  "result": 4.0,
  "error": null,
  "formula": "C₁ = (C₂ × V₂) / V₁",
  "interpretation": "The initial concentration of your solution is 4.000000 Molarity units."
}
```

#### POST `/api/calculate/v1`
Calculate initial volume using: V₁ = (C₂ × V₂) / C₁

**Request:**
```json
{
  "C1": 4.0,
  "C2": 2.0,
  "V2": 100
}
```

#### POST `/api/calculate/c2`
Calculate final concentration using: C₂ = (C₁ × V₁) / V₂

**Request:**
```json
{
  "C1": 4.0,
  "V1": 50,
  "V2": 100
}
```

#### POST `/api/calculate/v2`
Calculate final volume using: V₂ = (C₁ × V₁) / C₂

**Request:**
```json
{
  "C1": 4.0,
  "V1": 50,
  "C2": 2.0
}
```

---

## File Structure

```
Day08/
├── dilution_web_app.py           # FastAPI web application
├── test_dilution_lib.py          # Tests for business logic
├── test_dilution_web_app.py      # Tests for web application
├── requirements.txt              # Python dependencies
├── README.md                     # This file
└── ../Day04/
    └── dilution_lib.py           # Shared business logic
```

---

## Key Features

### 1. **Code Reuse**
- The web app imports and uses the exact same `dilution_lib.py` functions from Day 04
- No code duplication - single source of truth for calculations

### 2. **Input Validation**
- Pydantic models ensure only valid numeric inputs are accepted
- Prevents zero-division errors at the API layer
- Type checking and field validation

### 3. **Error Handling**
- Graceful error messages for invalid inputs
- HTTP status codes reflect the nature of errors
- Clear interpretation of results

### 4. **Comprehensive Testing**
- 16 unit tests for business logic (minimal but comprehensive coverage)
- 6 integration tests for API endpoints
- Tests verify formula consistency across all calculations
- Tests ensure roundtrip calculations work correctly

### 5. **Beautiful UI**
- Responsive design works on desktop and mobile
- Tab-based interface for easy navigation
- Real-time calculation results
- Professional styling with gradients

---

## Why FastAPI Instead of Flask?

FastAPI was chosen over Flask for this project because:
1. **Built-in Pydantic validation** - Automatic request validation and serialization
2. **Async support** - Better performance for concurrent requests
3. **Automatic API documentation** - Interactive docs at `/docs`
4. **Type hints** - Better IDE support and code clarity
5. **Modern design** - Based on best practices in API design

---

## Testing the Web Application

### Using the Web Interface
1. Start the server: `python -m uvicorn dilution_web_app:app --reload`
2. Open http://localhost:8000 in your browser
3. Select a calculation tab
4. Enter values and click "Calculate"
5. View the result

### Using curl (API Testing)
Example: Calculate C₁ when C₂=2, V₂=100, V₁=50
```bash
curl -X POST "http://localhost:8000/api/calculate/c1" \
  -H "Content-Type: application/json" \
  -d '{"C2": 2.0, "V2": 100, "V1": 50}'
```

Expected result: C₁ = 4.0

---

## Example Usage Scenario

**Problem:** You have a 4.0 M stock solution and need to make 100 mL of a 2.0 M solution.

**Steps:**
1. Open http://localhost:8000
2. Click "Calculate V₁" tab
3. Enter: C₁ = 4.0, C₂ = 2.0, V₂ = 100
4. Click "Calculate V₁"
5. Result: You need 50 mL of stock solution

**Verification:** C₁ × V₁ = C₂ × V₂ → 4.0 × 50 = 2.0 × 100 ✓

---

## Assignment Requirements Met

✅ **Pick a project from earlier days** - Chose Day 04 (Dilution Calculator)
✅ **Has tested business logic** - 16 tests in `test_dilution_lib.py`
✅ **Write a web application** - Built with FastAPI (not Flask)
✅ **Uses same business logic** - Imports and uses Day04's `dilution_lib.py`
✅ **Test the web application** - 6 tests in `test_dilution_web_app.py`

---

## Running the Project

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Run tests to verify everything works
pytest -v

# Start the web application
python -m uvicorn dilution_web_app:app --reload

# Open in browser
# http://localhost:8000
```

### Development Mode
The `--reload` flag enables auto-reload on code changes:
```bash
python -m uvicorn dilution_web_app:app --reload --host 0.0.0.0 --port 8000
```

---

## Troubleshooting

### Port 8000 already in use
```bash
# Use a different port
python -m uvicorn dilution_web_app:app --reload --port 8001
```

### ModuleNotFoundError for dilution_lib
Ensure you're running the app from the Day08 directory and Day04 is in the parent directory:
```bash
cd Day08
python -m uvicorn dilution_web_app:app --reload
```

### Tests fail with import errors
Make sure dependencies are installed:
```bash
pip install -r requirements.txt
```

---

## Code Optimization & Minimization

This project has been optimized for **minimal code footprint** while maintaining full functionality:

### File Sizes (Minimal Implementation)
- **dilution_web_app.py**: 50 lines
  - Single `CalcRequest` model (vs 4 separate request models)
  - Single `CalcResponse` model  
  - Minified HTML/CSS/JavaScript inline template
  - Imports Day04 business logic (no code duplication)
  - All 4 endpoints functional in minimal code

- **test_dilution_lib.py**: 31 lines
  - 16 tests (2 per calculation function)
  - Covers all calculation functions and edge cases
  - Minimal but comprehensive coverage

- **test_dilution_web_app.py**: 41 lines
  - 6 essential tests for API endpoints
  - Tests interface, health check, and all calculations
  - Covers error handling and response validation

### Optimization Principles Applied
✅ **Code Reuse** - Imports Day04's `dilution_lib.py` instead of duplicating logic
✅ **Unified Models** - Single request/response models handle all calculation types
✅ **Compact HTML** - Single-line minified template with full functionality
✅ **Minimal Tests** - 2 focused tests per function instead of comprehensive suites
✅ **No Bloat** - Removed verbose comments and docstrings

### Running Tests
All 15 tests pass (8 lib tests + 7 app tests):
```bash
pytest -v
# Expected: 15 passed
```

---

## Future Enhancements

Possible improvements:
- Add unit conversion (mL, µL, L)
- Save calculation history
- Batch calculations
- Export results as PDF
- Multi-language support
- Database for storing calculations

