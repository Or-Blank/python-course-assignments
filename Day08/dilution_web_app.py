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


@app.get("/", response_class=HTMLResponse)
def root():
    return """<!DOCTYPE html><html><head><title>Dilution Calculator</title><style>body{font-family:Arial;background:#667eea;min-height:100vh;display:flex;justify-content:center;align-items:center}.container{background:white;padding:40px;border-radius:10px;box-shadow:0 10px 40px rgba(0,0,0,0.2);max-width:400px}h1{color:#333;text-align:center}div{margin:10px 0}.tab-btn{width:48%;padding:10px;margin:5px 1%;border:2px solid #ddd;background:white;cursor:pointer;border-radius:5px}.tab-btn.active{background:#667eea;color:white}.tab{display:none}.tab.active{display:block}input{width:100%;padding:10px;margin:10px 0;border:1px solid #ddd;border-radius:5px;box-sizing:border-box}button{width:100%;padding:10px;background:#667eea;color:white;border:none;border-radius:5px;cursor:pointer;margin-top:10px}.result{margin-top:20px;padding:15px;background:#f0f4ff;border-radius:5px;display:none}.result.show{display:block}</style></head><body><div class="container"><h1>⚗️ Dilution Calculator</h1><div><button class="tab-btn active" onclick="switchTab('c1')">C₁</button><button class="tab-btn" onclick="switchTab('v1')">V₁</button><button class="tab-btn" onclick="switchTab('c2')">C₂</button><button class="tab-btn" onclick="switchTab('v2')">V₂</button></div><div id="c1" class="tab active"><input type="number" id="c1_c2" placeholder="C2" step="0.0001"><input type="number" id="c1_v2" placeholder="V2" step="0.0001"><input type="number" id="c1_v1" placeholder="V1" step="0.0001"><button onclick="calculate('c1')">Calculate</button><div id="c1_result" class="result"></div></div><div id="v1" class="tab"><input type="number" id="v1_c1" placeholder="C1" step="0.0001"><input type="number" id="v1_c2" placeholder="C2" step="0.0001"><input type="number" id="v1_v2" placeholder="V2" step="0.0001"><button onclick="calculate('v1')">Calculate</button><div id="v1_result" class="result"></div></div><div id="c2" class="tab"><input type="number" id="c2_c1" placeholder="C1" step="0.0001"><input type="number" id="c2_v1" placeholder="V1" step="0.0001"><input type="number" id="c2_v2" placeholder="V2" step="0.0001"><button onclick="calculate('c2')">Calculate</button><div id="c2_result" class="result"></div></div><div id="v2" class="tab"><input type="number" id="v2_c1" placeholder="C1" step="0.0001"><input type="number" id="v2_v1" placeholder="V1" step="0.0001"><input type="number" id="v2_c2" placeholder="C2" step="0.0001"><button onclick="calculate('v2')">Calculate</button><div id="v2_result" class="result"></div></div></div><script>function switchTab(t){document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.querySelectorAll('.tab-btn').forEach(x=>x.classList.remove('active'));document.getElementById(t).classList.add('active');event.target.classList.add('active')}async function calculate(type){let data={};if(type==='c1'){data.C2=+document.getElementById('c1_c2').value;data.V2=+document.getElementById('c1_v2').value;data.V1=+document.getElementById('c1_v1').value}else if(type==='v1'){data.C1=+document.getElementById('v1_c1').value;data.C2=+document.getElementById('v1_c2').value;data.V2=+document.getElementById('v1_v2').value}else if(type==='c2'){data.C1=+document.getElementById('c2_c1').value;data.V1=+document.getElementById('c2_v1').value;data.V2=+document.getElementById('c2_v2').value}else if(type==='v2'){data.C1=+document.getElementById('v2_c1').value;data.V1=+document.getElementById('v2_v1').value;data.C2=+document.getElementById('v2_c2').value}const resp=await fetch(`/api/calculate/${type}`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(data)});const res=await resp.json();const el=document.getElementById(type+'_result');if(res.success)el.innerHTML=`<strong>${res.result.toFixed(6)}</strong><br>${res.interpretation}`;else el.innerHTML=`<strong style="color:red">${res.error}</strong>`;el.classList.add('show')}</script></body></html>"""


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
