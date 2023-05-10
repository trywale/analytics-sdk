import pytest
from wale import Wale

import logging
logger = logging.getLogger(__name__)

@pytest.fixture
def api_root(request):
    return request.config.getoption("--api-root")

@pytest.fixture
def wale_local_client(api_root):
    return Wale(api_root=api_root, api_key='qwerty')

@pytest.fixture
def wale_offline_client():
    return Wale(api_root='http://127.0.0.1:5001/wale-ide-dev/offline/logger', api_key='qwerty')


# Testing remote client
@pytest.fixture
def wale_remote_client(api_root):
    return Wale(api_key='qwerty')

def test_wale_remote_log(wale_remote_client):
    inputs = {
        'context': 'This is a test',
        'mode': 'short',
    }
    output = "This is a test"
    model_config = {
        "model": "gpt-3.5-turbo",
        "provider": "openai",
        "temperature": 0.5,
        "max_tokens": 100,
    }
    task_id = "tid-task123"
    person_id = "pid-person123"
    total_tokens = 100

    res = wale_remote_client.log(
        inputs=inputs,
        output=output,
        model_config=model_config,
        task_id=task_id,
        person_id=person_id,
        total_tokens=total_tokens,
    )
    assert res is not None and res['id'] is not None

def test_wale_local_log(wale_local_client):
    inputs = {
        'context': 'This is a test',
        'mode': 'short',
    }
    output = "This is a test"
    model_config = {
        "model": "gpt-3.5-turbo",
        "provider": "openai",
        "temperature": 0.5,
        "max_tokens": 100,
    }
    task_id = "tid-task123"
    person_id = "pid-person123"
    total_tokens = 100

    res = wale_local_client.log(
        inputs=inputs,
        output=output,
        model_config=model_config,
        task_id=task_id,
        person_id=person_id,
        total_tokens=total_tokens,
    )

    assert res is not None and res['id'] is not None


def test_wale_offline_log(wale_offline_client):
    inputs = {
        'context': 'This is a test',
        'mode': 'short',
    }
    output = "This is a test"
    model_config = {
        "model": "gpt-3.5-turbo",
        "provider": "openai",
        "temperature": 0.5,
        "max_tokens": 100,
    }
    task_id = "tid-task123"
    person_id = "pid-person123"
    total_tokens = 100

    res = wale_offline_client.log(
        inputs=inputs,
        output=output,
        model_config=model_config,
        task_id=task_id,
        person_id=person_id,
        total_tokens=total_tokens,
    )
    logger.error(res)
    assert res is not None and res['error'] is not None
