from flask import Flask, jsonify
from capp import add


app = Flask(__name__)


@app.route("/add/<int:x>/<int:y>")
def add_numbers(x, y):
    # instead of doing the task right there
    # we let celery handle it
    task = add.delay(x, y)  # Send task to Celery
    return jsonify({"task_id": task.id, "status": "Task submitted!"})


@app.route("/status/<task_id>")
def task_status(task_id):
    result = add.AsyncResult(task_id)
    if result.ready():
        return jsonify({"status": "Completed", "result": result.result})
    return jsonify({"status": "Pending"})


if __name__ == "__main__":
    app.run(debug=True)