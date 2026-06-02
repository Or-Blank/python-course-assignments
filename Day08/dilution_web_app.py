import sys
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional

sys.path.insert(0, str(Path(__file__).parent.parent / "Day04"))

from dilution_lib import Calculation_of_C1, Calculation_of_V1, Calculation_of_C2, Calculation_of_V2

app = FastAPI(title="Dilution Calculator", version="1.0.0")


class CalcRequest(BaseModel):
    C1: Optional[float] = Field(None, gt=0)
    V1: Optional[float] = Field(None, gt=0)
    C2: Optional[float] = Field(None, gt=0)
    V2: Optional[float] = Field(None, gt=0)


class CalcResponse(BaseModel):
    success: bool
    result: Optional[float] = None
    error: Optional[str] = None
    formula: str = ""
    interpretation: str = ""

#From here is only the "cosmetics" of the web app, the rest is the API logic and the functional code.
@app.get("/", response_class=HTMLResponse)
def root():
    return """ 
<!DOCTYPE html>
<html>
<head>
<title>Dilution Calculator</title>

<style>
    body {
        font-family: 'Segoe UI', Arial;
        background: linear-gradient(135deg, #667eea, #764ba2);
        min-height: 100vh;
        margin: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        color: #333;
    }

    .container {
        background: white;
        padding: 35px;
        border-radius: 14px;
        width: 420px;
        box-shadow: 0 12px 45px rgba(0,0,0,0.25);
        animation: fadeIn 0.4s ease-out;
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    h1 {
        text-align: center;
        margin-bottom: 10px;
        color: #444;
    }

    .note {
        text-align:center;
        font-size:14px;
        color:#666;
        margin-bottom:20px;
    }

    .tabs {
        display: flex;
        justify-content: space-between;
        margin-bottom: 15px;
    }

    .tab-btn {
        flex: 1;
        padding: 10px;
        margin: 0 4px;
        border: 2px solid #ddd;
        background: #fafafa;
        cursor: pointer;
        border-radius: 6px;
        transition: 0.2s;
        font-weight: 600;
    }

    .tab-btn:hover {
        background: #eef0ff;
    }

    .tab-btn.active {
        background: #667eea;
        color: white;
        border-color: #667eea;
    }

    .tab {
        display: none;
        animation: fadeIn 0.3s ease-out;
    }

    .tab.active {
        display: block;
    }

    input {
        width: 100%;
        padding: 12px;
        margin: 8px 0;
        border: 1px solid #ccc;
        border-radius: 6px;
        font-size: 15px;
    }

    button.calc-btn {
        width: 100%;
        padding: 12px;
        background: #667eea;
        color: white;
        border: none;
        border-radius: 6px;
        cursor: pointer;
        margin-top: 10px;
        font-size: 16px;
        transition: 0.2s;
    }

    button.calc-btn:hover {
        background: #5568d8;
    }

    .result {
        margin-top: 18px;
        padding: 15px;
        background: #eef2ff;
        border-left: 4px solid #667eea;
        border-radius: 6px;
        display: none;
        font-size: 15px;
    }

    .result.show {
        display: block;
    }
</style>
</head>

<body>
<div class="container">
    <h1>⚗️ Dilution Calculator</h1>
    <p class="note">Use µL for volume and mg/µL for concentration. Units must match.</p>

    <div class="tabs">
        <button class="tab-btn active" onclick="switchTab('c1')">C₁</button>
        <button class="tab-btn" onclick="switchTab('v1')">V₁</button>
        <button class="tab-btn" onclick="switchTab('c2')">C₂</button>
        <button class="tab-btn" onclick="switchTab('v2')">V₂</button>
    </div>

    <!-- C1 -->
    <div id="c1" class="tab active">
        <input type="number" id="c1_c2" placeholder="C₂ (final concentration)">
        <input type="number" id="c1_v2" placeholder="V₂ (final volume)">
        <input type="number" id="c1_v1" placeholder="V₁ (initial volume)">
        <button class="calc-btn" onclick="calculate('c1')">Calculate C₁</button>
        <div id="c1_result" class="result"></div>
    </div>

    <!-- V1 -->
    <div id="v1" class="tab">
        <input type="number" id="v1_c1" placeholder="C₁ (initial concentration)">
        <input type="number" id="v1_c2" placeholder="C₂ (final concentration)">
        <input type="number" id="v1_v2" placeholder="V₂ (final volume)">
        <button class="calc-btn" onclick="calculate('v1')">Calculate V₁</button>
        <div id="v1_result" class="result"></div>
    </div>

    <!-- C2 -->
    <div id="c2" class="tab">
        <input type="number" id="c2_c1" placeholder="C₁ (initial concentration)">
        <input type="number" id="c2_v1" placeholder="V₁ (initial volume)">
        <input type="number" id="c2_v2" placeholder="V₂ (final volume)">
        <button class="calc-btn" onclick="calculate('c2')">Calculate C₂</button>
        <div id="c2_result" class="result"></div>
    </div>

    <!-- V2 -->
    <div id="v2" class="tab">
        <input type="number" id="v2_c1" placeholder="C₁ (initial concentration)">
        <input type="number" id="v2_v1" placeholder="V₁ (initial volume)">
        <input type="number" id="v2_c2" placeholder="C₂ (final concentration)">
        <button class="calc-btn" onclick="calculate('v2')">Calculate V₂</button>
        <div id="v2_result" class="result"></div>
    </div>

</div>

<script>
function switchTab(tab) {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));

    document.getElementById(tab).classList.add('active');
    event.target.classList.add('active');
}

async function calculate(type) {
    let data = {};

    if (type === 'c1') {
        data.C2 = +document.getElementById('c1_c2').value;
        data.V2 = +document.getElementById('c1_v2').value;
        data.V1 = +document.getElementById('c1_v1').value;
    } else if (type === 'v1') {
        data.C1 = +document.getElementById('v1_c1').value;
        data.C2 = +document.getElementById('v1_c2').value;
        data.V2 = +document.getElementById('v1_v2').value;
    } else if (type === 'c2') {
        data.C1 = +document.getElementById('c2_c1').value;
        data.V1 = +document.getElementById('c2_v1').value;
        data.V2 = +document.getElementById('c2_v2').value;
    } else if (type === 'v2') {
        data.C1 = +document.getElementById('v2_c1').value;
        data.V1 = +document.getElementById('v2_v1').value;
        data.C2 = +document.getElementById('v2_c2').value;
    }

    const resp = await fetch(`/api/calculate/${type}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    });

    const res = await resp.json();
    const box = document.getElementById(type + '_result');

    if (res.success) {
        let pretty = Number(res.result.toFixed(6)).toString();

        if (type === 'v1') {
            let solvent = Number((data.V2 - res.result).toFixed(6)).toString();
            box.innerHTML = `
                <strong>${pretty} µL</strong><br>
                Add <strong>${pretty} µL</strong> of stock to <strong>${solvent} µL</strong> of solvent.
            `;
        } else {
            box.innerHTML = `<strong>${pretty}</strong><br>${res.interpretation}`;
        }
    } else {
        box.innerHTML = `<strong style="color:red">${res.error}</strong>`;
    }

    box.classList.add('show');
}
</script>

</body>
</html>
"""
#Up to here is only the "cosmetics" of the web app, the rest is the API logic and the functional code.

@app.get("/api/health")
def health():
    return {"status": "healthy"}


@app.post("/api/calculate/c1", response_model=CalcResponse)
def calc_c1(req: CalcRequest):
    result = Calculation_of_C1(req.C2, req.V2, req.V1)
    if result is None:
        return CalcResponse(success=False, error="V1 cannot be zero", formula="C1=(C2*V2)/V1")
    return CalcResponse(success=True, result=result, formula="C1=(C2*V2)/V1", interpretation=f"C1={result:.6f}")


@app.post("/api/calculate/v1", response_model=CalcResponse)
def calc_v1(req: CalcRequest):
    result = Calculation_of_V1(req.C1, req.C2, req.V2)
    if result is None:
        return CalcResponse(success=False, error="C1 cannot be zero", formula="V1=(C2*V2)/C1")
    return CalcResponse(success=True, result=result, formula="V1=(C2*V2)/C1", interpretation=f"V1={result:.6f}")


@app.post("/api/calculate/c2", response_model=CalcResponse)
def calc_c2(req: CalcRequest):
    result = Calculation_of_C2(req.C1, req.V1, req.V2)
    if result is None:
        return CalcResponse(success=False, error="V2 cannot be zero", formula="C2=(C1*V1)/V2")
    return CalcResponse(success=True, result=result, formula="C2=(C1*V1)/V2", interpretation=f"C2={result:.6f}")


@app.post("/api/calculate/v2", response_model=CalcResponse)
def calc_v2(req: CalcRequest):
    result = Calculation_of_V2(req.C1, req.V1, req.C2)
    if result is None:
        return CalcResponse(success=False, error="C2 cannot be zero", formula="V2=(C1*V1)/C2")
    return CalcResponse(success=True, result=result, formula="V2=(C1*V1)/C2", interpretation=f"V2={result:.6f}")
