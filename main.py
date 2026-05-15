from fastapi import FastAPI, Query
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
from pydantic import BaseModel

from service import start_or_next, answer, score


app = FastAPI(
    title="English B2 Trainer",
    version="1.0.0"
)

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class AnswerRequest(BaseModel):
    correct: bool


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.post("/api/vocabulary/start")
def start(
    nivel: str | None = Query(default=None),
    categoria: str | None = Query(default=None),
    bloqueExamen: str | None = Query(default=None),
    dificultad: str | None = Query(default=None)
):
    return start_or_next(
        nivel=nivel,
        categoria=categoria,
        bloque_examen=bloqueExamen,
        dificultad=dificultad
    )


@app.post("/api/vocabulary/answer")
def answer_question(request: AnswerRequest):
    return answer(request.correct)


@app.get("/api/vocabulary/score")
def get_score():
    return score()

@app.get("/api/vocabulary/test")
def test():
    return start_or_next()    