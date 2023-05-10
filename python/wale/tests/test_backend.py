import pytest
import requests

@pytest.fixture
def api_root(request):
    return request.config.getoption("--api-root")


def test_logger_endpoint_with_valid_payload(api_root):
    url = f"{api_root}/logger"
    data = {
        "api_key": "qwerty",
        "inputs": {"input1": "value1", "input2": "value2"},
        "output": "output_value",
        "task_id": "task_123",
        "model_config": {
            "model": "gpt-2",
            "provider": "openai",
            "temperature": 0.7,
            "max_tokens": 50,
        },
        "person_id": "person_123",
        "total_tokens": 100,
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert "id" in response.json()

def test_logger_endpoint_with_missing_required_fields(api_root):
    url = f"{api_root}/logger"
    data = {"inputs": {}, "output": "output_value", "task_id": "task_123"}
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()

def test_logger_endpoint_with_invalid_api_key(api_root):
    url = f"{api_root}/logger"
    data = {
        "api_key": "invalid_key",
        "inputs": {"input1": "value1", "input2": "value2"},
        "output": "output_value",
        "task_id": "task_123",
    }
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"] == "Invalid api_key"

def test_logger_endpoint_with_empty_inputs(api_root):
    url = f"{api_root}/logger"
    data = {
        "api_key": "qwerty",
        "inputs": {},
        "output": "output_value",
        "task_id": "task_123",
    }
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert response.json()["error"]["name"] == "ValidationError"
    assert "Inputs object must not be empty" in response.json()["error"]["errors"]


def test_logger_endpoint_with_negative_tokens(api_root):
    url = f"{api_root}/logger"
    data = {
        "api_key": "qwerty",
        "inputs": {"input1": "value1", "input2": "value2"},
        "output": "output_value",
        "task_id": "task_123",
        "model_config": {
            "model": "gpt-2",
            "provider": "openai",
            "temperature": 0.7,
            "max_tokens": 10,
        },
        "person_id": "person_123",
        "total_tokens": -100,
    }
    response = requests.post(url, json=data)
    assert response.status_code == 400
    assert "error" in response.json()
    assert "total_tokens" in response.json()["error"]['errors'][0]
    
def test_logger_endpoint_with_extra_fields(api_root):
    url = f"{api_root}/logger"
    data = {
        "api_key": "qwerty",
        "inputs": {"input1": "value1", "input2": "value2"},
        "output": "output_value",
        "task_id": "task_123",
        "model_config": {
            "model": "gpt-2",
            "provider": "openai",
            "temperature": 0.7,
            "max_tokens": 50,
        },
        "person_id": "person_123",
        "total_tokens": 100,
        "extra_field": "extra_value"
    }
    response = requests.post(url, json=data)
    assert response.status_code == 200
    assert "id" in response.json()
    assert "extra_field" not in response.json()
