from flask import Flask, jsonify, request, render_template

def create_app():
    app = Flask(__name__)

    # In-memory "database" — cukup untuk tujuan praktikum ini.
    # Fokus tugas adalah integrasi Docker/Compose/CI-CD, bukan kompleksitas data.
    tasks = [
        {"id": 1, "title": "Belajar Docker", "done": False},
        {"id": 2, "title": "Belajar Docker Compose", "done": False},
        {"id": 3, "title": "Belajar GitHub Actions", "done": False},
    ]
    state = {"next_id": 4}

    @app.get("/health")
    def health():
        return jsonify(status="healthy"), 200

    @app.get("/")
    def index():
        return render_template("index.html")

    @app.get("/api")
    def api_info():
        return jsonify(
            message="Simple Task API sedang berjalan",
            endpoints=[
                "GET /health", "GET /tasks", "POST /tasks",
                "GET /tasks/<id>", "PUT /tasks/<id>", "DELETE /tasks/<id>",
            ],
        ), 200

    @app.get("/tasks")
    def get_tasks():
        return jsonify(tasks), 200

    @app.get("/tasks/<int:task_id>")
    def get_task(task_id):
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task is None:
            return jsonify(error="Task tidak ditemukan"), 404
        return jsonify(task), 200

    @app.post("/tasks")
    def create_task():
        data = request.get_json(silent=True) or {}
        title = data.get("title")
        if not title or not isinstance(title, str) or not title.strip():
            return jsonify(error='Field "title" wajib diisi'), 400
        new_task = {"id": state["next_id"], "title": title.strip(), "done": False}
        state["next_id"] += 1
        tasks.append(new_task)
        return jsonify(new_task), 201

    @app.put("/tasks/<int:task_id>")
    def update_task(task_id):
        task = next((t for t in tasks if t["id"] == task_id), None)
        if task is None:
            return jsonify(error="Task tidak ditemukan"), 404
        data = request.get_json(silent=True) or {}
        if "title" in data:
            task["title"] = data["title"]
        if "done" in data:
            task["done"] = data["done"]
        return jsonify(task), 200

    @app.delete("/tasks/<int:task_id>")
    def delete_task(task_id):
        index = next((i for i, t in enumerate(tasks) if t["id"] == task_id), None)
        if index is None:
            return jsonify(error="Task tidak ditemukan"), 404
        tasks.pop(index)
        return "", 204

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000)
