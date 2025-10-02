// quizzes/static/quizzes/js/main.js

document.addEventListener("DOMContentLoaded", function () {
    // --- INDEX (Lista de Quizzes) ---
    const quizList = document.getElementById("quizzes-list");
    if (quizList) {
        fetch("/api/v1/quizzes/")
            .then(r => r.json())
            .then(data => {
                if (data.results.length === 0) {
                    quizList.innerHTML = "<p class='text-muted'>No hay quizzes disponibles.</p>";
                    return;
                }
                data.results.forEach(q => {
                    const item = document.createElement("a");
                    item.href = `/quiz/${q.id}/`;
                    item.className = "list-group-item list-group-item-action";
                    item.innerHTML = `
                        <h5 class="mb-1">${q.title}</h5>
                        <p>${q.description}</p>
                    `;
                    quizList.appendChild(item);
                });
            })
            .catch(err => {
                quizList.innerHTML = `<p class="text-danger">❌ Error cargando quizzes: ${err.message}</p>`;
            });
    }

    // --- QUIZ FORM (crear/editar) ---
    const quizForm = document.getElementById("quiz-form");
    if (quizForm) {
        quizForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const id = document.getElementById("quiz_id")?.value;
            const payload = {
                title: document.getElementById("title").value,
                description: document.getElementById("description").value
            };

            fetch(`/api/v1/quizzes/${id ? id + "/" : ""}`, {
                method: id ? "PUT" : "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify(payload)
            })
            .then(r => r.json())
            .then(data => {
                alert("✅ Quiz guardado correctamente");
                window.location.href = "/";
            });
        });
    }

    // --- QUIZ DETAIL (mostrar preguntas y opciones) ---
    const quizDetail = document.getElementById("quiz-detail");
    if (quizDetail) {
        const quizId = quizDetail.dataset.quizId;

        // cargar preguntas
        fetch(`/api/v1/questions/?quiz=${quizId}`)
            .then(r => r.json())
            .then(data => {
                const qContainer = document.getElementById("questions-list");
                if (data.results.length === 0) {
                    qContainer.innerHTML = "<p class='text-muted'>No hay preguntas.</p>";
                    return;
                }

                data.results.forEach(question => {
                    const card = document.createElement("div");
                    card.className = "card mb-2";
                    card.innerHTML = `
                        <div class="card-body">
                            <h5>${question.text}</h5>
                            <div id="choices-${question.id}" class="ms-3"></div>
                            <a href="/choice/new/${question.id}/" class="btn btn-sm btn-outline-primary mt-2">➕ Añadir opción</a>
                        </div>
                    `;
                    qContainer.appendChild(card);

                    // cargar choices
                    fetch(`/api/v1/choices/?question=${question.id}`)
                        .then(r => r.json())
                        .then(choices => {
                            const cContainer = document.getElementById(`choices-${question.id}`);
                            choices.results.forEach(c => {
                                const li = document.createElement("div");
                                li.innerHTML = `
                                    - ${c.text} ${c.is_correct ? "✅" : ""}
                                `;
                                cContainer.appendChild(li);
                            });
                        });
                });
            });
    }

    // --- QUESTION FORM ---
    const questionForm = document.getElementById("question-form");
    if (questionForm) {
        questionForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const quizId = document.getElementById("quiz_id").value;
            fetch("/api/v1/questions/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    quiz: quizId,
                    text: document.getElementById("text").value
                })
            })
            .then(r => r.json())
            .then(data => {
                alert("✅ Pregunta creada");
                window.location.href = `/quiz/${quizId}/`;
            });
        });
    }

    // --- CHOICE FORM ---
    const choiceForm = document.getElementById("choice-form");
    if (choiceForm) {
        choiceForm.addEventListener("submit", function (e) {
            e.preventDefault();
            const questionId = document.getElementById("question_id").value;
            fetch("/api/v1/choices/", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({
                    question: questionId,
                    text: document.getElementById("text").value,
                    is_correct: document.getElementById("is_correct").checked
                })
            })
            .then(r => r.json())
            .then(data => {
                alert("✅ Opción creada");
                window.history.back();
            });
        });
    }
});
