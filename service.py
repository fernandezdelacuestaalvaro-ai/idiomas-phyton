from database import vocabulary_collection

session = {
    "items": [],
    "index": 0,
    "showing_spanish": False,
    "correct_answers": 0,
    "wrong_answers": 0,
    "finished": True
}


def start_or_next(
        nivel=None,
        categoria=None,
        bloque_examen=None,
        dificultad=None
):
    global session

    if session["finished"]:
        query = {}

        if nivel:
            query["nivel"] = nivel

        if categoria:
            query["categoria"] = categoria

        if bloque_examen:
            query["bloqueExamen"] = bloque_examen

        if dificultad:
            query["dificultad"] = dificultad

        items = list(
            vocabulary_collection
            .find(query, {"_id": 0})
            .sort("id", 1)
        )

        session = {
            "items": items,
            "index": 0,
            "showing_spanish": False,
            "correct_answers": 0,
            "wrong_answers": 0,
            "finished": len(items) == 0
        }

        return build_response()

    if session["showing_spanish"]:
        session["showing_spanish"] = False
        session["index"] += 1

        if session["index"] >= len(session["items"]):
            session["finished"] = True
    else:
        session["showing_spanish"] = True

    return build_response()


def answer(correct: bool):
    global session

    current = get_current()

    if current is None:
        return build_response()

    if correct:
        session["correct_answers"] += 1
    else:
        session["wrong_answers"] += 1

    return build_response()


def score():
    total_answered = (
        session["correct_answers"] +
        session["wrong_answers"]
    )

    if total_answered == 0:
        score_over_ten = 0
    else:
        score_over_ten = round(
            (session["correct_answers"] / total_answered) * 10,
            2
        )

    return {
        "correctAnswers": session["correct_answers"],
        "wrongAnswers": session["wrong_answers"],
        "totalQuestions": len(session["items"]),
        "answeredQuestions": total_answered,
        "scoreOverTen": score_over_ten,
        "approved": score_over_ten >= 5
    }


def build_response():
    current = get_current()

    if current is None:
        return {
            "id": None,
            "text": None,
            "languageShown": None,
            "category": None,
            "level": None,
            "difficulty": None,
            "examBlock": None,
            "currentQuestion": session["index"],
            "totalQuestions": len(session["items"]),
            "finished": True,
            "score": score()
        }

    if session["showing_spanish"]:
        text = current.get("castellano")
        language = "SPANISH"
    else:
        text = current.get("traduccion")
        language = "ENGLISH"

    return {
        "id": current.get("id"),
        "text": text,
        "languageShown": language,
        "category": current.get("categoria"),
        "level": current.get("nivel"),
        "difficulty": current.get("dificultad"),
        "examBlock": current.get("bloqueExamen"),
        "currentQuestion": session["index"] + 1,
        "totalQuestions": len(session["items"]),
        "finished": False,
        "score": score()
    }


def get_current():
    if session["finished"]:
        return None

    if session["index"] >= len(session["items"]):
        return None

    return session["items"][session["index"]]


def reset_session():
    global session

    session = {
        "items": [],
        "index": 0,
        "showing_spanish": False,
        "correct_answers": 0,
        "wrong_answers": 0,
        "finished": True
    }

    return {
        "message": "Session reset"
    }