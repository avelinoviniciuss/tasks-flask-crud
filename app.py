from typing import List

from flask import Flask, request, jsonify

from models.task import Task

# __name__ == __main__
app = Flask(__name__)

tasks: List = []
task_id_control = 1


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data.get('title'), description=data.get('description', ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    return jsonify({"message": "Nova tarefa criada com sucesso", "id": new_task.id})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks_list = [task.to_dict() for task in tasks]
    output = {"tasks": tasks_list, "total_tasks": len(tasks_list)}
    return jsonify(output)


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task_by_id(task_id):
    for task in tasks:
        if task.id == task_id:
            return jsonify(task.to_dict())
    return jsonify({"message": "Não foi possível encontrar a task"}), 404


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task.id == task_id:
            data = request.get_json()
            task.title = data.get('title')
            task.description = data.get('description')
            task.completed = data.get('completed')
            return jsonify({"message": "Task atualizada com sucesso"})
    return jsonify({"message": "Não foi possível encontrar a task"}), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    for task in tasks:
        if task_id == task.id:
            tasks.remove(task)
            return jsonify({"message": "Task deletada com sucesso"})
    return jsonify({"message": "Não foi possível encontrar a task"}), 404


if __name__ == "__main__":
    app.run(debug=True)
