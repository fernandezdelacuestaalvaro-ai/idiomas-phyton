async function startNext() {
    const nivel = document.getElementById("nivel").value;
    const bloqueExamen = document.getElementById("bloqueExamen").value;
    const dificultad = document.getElementById("dificultad").value;

    let url = "/api/vocabulary/start?";
    const params = new URLSearchParams();

    if (nivel) params.append("nivel", nivel);
    if (bloqueExamen) params.append("bloqueExamen", bloqueExamen);
    if (dificultad) params.append("dificultad", dificultad);

    url += params.toString();

    const response = await fetch(url, {
        method: "POST"
    });

    const data = await response.json();

    render(data);
}


async function markAnswer(correct) {
    const response = await fetch("/api/vocabulary/answer", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            correct: correct
        })
    });

    const data = await response.json();

    render(data);
}


function render(data) {
    if (data.finished) {
        document.getElementById("counter").innerText = "Test terminado";
        document.getElementById("language").innerText = "FIN";
        document.getElementById("text").innerText = "Nota final: " + data.score.scoreOverTen + " / 10";
        updateScore(data);
        return;
    }

    document.getElementById("counter").innerText =
        data.currentQuestion + " / " + data.totalQuestions;

    document.getElementById("language").innerText =
        data.languageShown === "ENGLISH" ? "INGLÉS" : "ESPAÑOL";

    document.getElementById("text").innerText = data.text;

    document.getElementById("level").innerText =
        "Nivel: " + data.level;

    document.getElementById("category").innerText =
        "Categoría: " + data.category;

    document.getElementById("difficulty").innerText =
        "Dificultad: " + data.difficulty;

    updateScore(data);
}


function updateScore(data) {
    document.getElementById("correctAnswers").innerText =
        data.score.correctAnswers;

    document.getElementById("totalQuestions").innerText =
        data.score.totalQuestions;

    document.getElementById("scoreOverTen").innerText =
        data.score.scoreOverTen;
}


function resetSession() {
    location.reload();
}