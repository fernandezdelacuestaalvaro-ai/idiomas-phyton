from database import vocabulary_collection


session = {
    "items": [],
    "index": 0,
    "showing_spanish": False,
    "correct_answers": 0,
    "answered_ids": set(),
    "finished": True
}


def start_or_next(nivel=None, categoria=None, bloque_examen=None, dificultad=None):
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
            "answered_ids": set(),
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
    current = get_current()

    if current is None:
        return build_response()

    current_id = current.get("id")

    if current_id not in session["answered_ids"]:
        session["answered_ids"].add(current_id)

        if correct:
            session["correct_answers"] += 1

    return build_response()


def score():
    total = len(session["items"])

    if total == 0:
        score_over_ten = 0
    else:
        score_over_ten = round((session["correct_answers"] / total) * 10, 2)

    return {
        "correctAnswers": session["correct_answers"],
        "totalQuestions": total,
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