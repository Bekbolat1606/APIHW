from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI()
elements = []
global_list = []

@app.get("/sum1n/{n}")
async def sum_n(n: int):
    result = sum(range(1, n + 1))
    return {"result": result}

@app.get("/fibo")
def fibonacci(n: int):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return {"result": a}

class Element(BaseModel):
    element: str
    
@app.post("/reverse")
async def reverse_string(string: str = Header(...)):
    reversed_string = string[::-1]
    return JSONResponse(content={"result": reversed_string})    

@app.put("/list")
async def add_to_list(item: Element):
    elements.append(item.element)  # Добавляем элемент в массив
    return JSONResponse(content={"result": elements})

@app.get("/list")
async def get_list():
    return JSONResponse(content={"result": elements})

class CalculatorRequest(BaseModel):
    expr: str

@app.post("/calculator")
def calculator(request: CalculatorRequest):
    try:
        num1, operator, num2 = request.expr.split(",")
        num1, num2 = float(num1), float(num2)
        if operator == "+":
            result = num1 + num2
        elif operator == "-":
            result = num1 - num2
        elif operator == "*":
            result = num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise HTTPException(status_code=403, detail={"error": "zerodiv"})
            result = num1 / num2
        else:
            raise ValueError
        return {"result": result}
    except ValueError:
        raise HTTPException(status_code=400, detail={"error": "invalid"})
