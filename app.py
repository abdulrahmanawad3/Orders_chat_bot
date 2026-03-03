from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from tools import menu
from states import States
from models import mess
from loader_hf import load_chain,load_judge
from helper import run_judge


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    if States.chain is None:
        load_chain()
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
def chatting(data: mess):
    if not States.chain_loaded:
        load_chain()

    if "menu" in data.message.lower():
        return JSONResponse({"reply": menu.run("")})

    States.chat_history.append("Human: " + data.message)
    response = States.chain.invoke(States.chat_history)
    States.chat_history.append("AI: " + response)

    return JSONResponse({"reply": response})


@app.post("/evaluate")
def evaluate():
    if not States.chain_loaded:
        load_chain()

    if not States.judge_chain_loaded:
        load_judge()

    history = States.chat_history
    if len(history) < 2:
        return JSONResponse({"error": "No response to evaluate yet."}, status_code=400)

    last_question = history[-2].removeprefix("Human: ").strip()
    last_answer   = history[-1].removeprefix("AI: ").strip()

    result = run_judge(last_question, last_answer)

    return JSONResponse({
        "question":  last_question,
        "answer":    last_answer,
        "score":     result.get("score"),
        "reasoning": result.get("comment", ""),
    })