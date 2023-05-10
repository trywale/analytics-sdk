# Wale

Wale is a Python logging library for sending LLM logs to the Wale platform. With Wale, you can easily log events from your Python application and view them in the Wale web interface.

## Installation

You can install Wale using pip:

```
pip install wale
```

## Usage

To use Wale, you first need to create a `Wale` instance with your API key and API root:

```python
from wale import Wale

wale = Wale(api_root='https://api.trywale.com', api_key='your-api-key')
```

Then, you can log events using the `log` method:

```python
wale.log(inputs={'context': 'This is a test', 'mode': 'short'}, output='This is a test', model_config={'model': 'gpt-3.5-turbo', 'provider': 'openai', 'temperature': 0.5, 'max_tokens': 100}, task_id='tid-task123', person_id='pid-person123', total_tokens=100)
```

This logs an event with the specified inputs, output, and model configuration, along with some additional metadata.

For more information on using Wale, see the [Wale documentation](https://trywale.com/docs).

## Contributing

If you find a bug or have a feature request, please open an issue on GitHub. We welcome contributions from the community! See the [contributing guide](CONTRIBUTING.md) for more information.

## License

This library is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.