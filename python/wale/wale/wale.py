import requests

from typing import Optional, TypedDict, Union

class ModelConfig(TypedDict):
    model: str
    provider: str
    temperature: float
    max_tokens: int

class EventType(TypedDict):
    api_key: str
    inputs: dict[str, str]
    output: str
    model_config: Optional[ModelConfig]
    task_id: str
    person_id: Optional[str]
    total_tokens: Optional[int]


class ResponseDict(TypedDict):
    id: str

class ErrorDict(TypedDict):
    error: str

class Wale:
    def __init__(self, api_key: str, api_root: str = None) -> None:
        if not api_root:
            api_root = "https://api.trywale.com"
        if not api_key:
            raise ValueError("api_key is required. Get one at https://ide.trywale.com/")
        self.api_root = api_root
        self.api_key = api_key

    def log(
        self, 
        inputs: dict[str, str], 
        output: str,
        task_id: str,
        model_config: Optional[ModelConfig] = None,
        person_id: Optional[str] = None,
        total_tokens: Optional[int] = None,
    ) -> Union[ResponseDict, ErrorDict]:
        data = {
            "api_key": self.api_key,
            "inputs": inputs,
            "output": output,
            "model_config": model_config,
            "task_id": task_id,
            "person_id": person_id,
            "total_tokens": total_tokens,
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(f"{self.api_root}/logger", json=data, headers=headers)
            response.raise_for_status()
            payload = response.json()
            return {
                "id": payload["id"],
            }
        except requests.exceptions.ConnectionError as error:
                return {
                    "error": "Network error occurred, please check your internet connection and try again."
                }
        except requests.exceptions.RequestException as error:
            if error.response is not None and hasattr(error.response, 'text'):
                return {
                    "error": error.response.text,
                }
            else:
                return {
                    "error": str(error),
                }
        except Exception as error:
            return {
                "error": str(error),
            }
        
