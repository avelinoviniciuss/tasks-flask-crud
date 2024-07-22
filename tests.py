import pytest, requests

BASE_URL = 'http://127.0.0.1:5000'
tasks =[]


def test_create_task():
    response = requests.post(f'{BASE_URL}/tasks', json={"title": "Nova tarefa", "description": "Descrição de uma nova tarefa"})
    assert response.status_code == 200
    assert "message" in response.json()
    assert "id" in response.json()
    tasks.append(response.json()['id'])


def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    assert response.status_code == 200
    response_json = response.json()
    assert "tasks" in response_json
    assert "total_tasks" in response_json


def test_get_task_by_id():
    if tasks:
        task_id = tasks[0]
        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert "id" in response_json
        assert "title" in response_json
        assert "description" in response_json
        assert "completed" in response_json
        assert response_json['id'] == task_id


def test_update_task():
    if tasks:
        task_id = tasks[0]
        response = requests.put(f"{BASE_URL}/tasks/{task_id}", json={"title": "Tarefa atualizada", "description": "Descrição atualizada", "completed": True})
        assert response.status_code == 200
        assert "message" in response.json()

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200
        response_json = response.json()
        assert response_json['title'] == "Tarefa atualizada"
        assert response_json['description'] == "Descrição atualizada"
        assert response_json['completed'] == True


def test_delete_task():
    if tasks:
        task_id = tasks[0]
        response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 200

        response = requests.get(f"{BASE_URL}/tasks/{task_id}")
        assert response.status_code == 404
        assert "message" in response.json()
        assert response.json()['message'] == "Não foi possível encontrar a task"