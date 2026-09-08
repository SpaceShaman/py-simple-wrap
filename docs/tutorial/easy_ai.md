# Easy AI

Working with artificial intelligence models often requires managing multiple vendor-specific libraries, API keys, and initialization parameters. Whether you're connecting to cloud providers like OpenAI or running models locally with Ollama, `easy_ai` provides a beginner-friendly helper function that unifies model creation across different AI providers.

## A small real-world example

Imagine you're building an application that needs to interact with AI models. Depending on your environment, you might want to use a cloud provider like OpenAI for production or a local model with Ollama for offline testing, without rewriting your model initialization logic.

```python
from py_simple import get_model

# Initialize a cloud model using OpenAI
openai_model = get_model(provider="openai", model_name="gpt-4o", api_key="your-api-key")

# Initialize a local model using Ollama
ollama_model = get_model(provider="ollama", model_name="llama3")

# Generate a response using the initialized model
response = ollama_model.invoke("Hello, world!")
print(response.content)
```

Example output:

```text
Hello! How can I assist you today?
```

## What happened?

`get_model()` provides a single, unified function to instantiate chat models from popular AI providers including OpenAI, Ollama, Anthropic, Google, and Mistral.

When `provider="openai"` is passed, `get_model()` imports and returns a `ChatOpenAI` instance configured with the specified model name and API key.

When `provider="ollama"` is passed, `get_model()` connects to your local Ollama server (defaulting to `http://localhost:11434`) and returns a `ChatOllama` instance ready to execute prompts locally.

You can also pass `provider="anthropic"`, `provider="google"`, or `provider="mistral"` to initialize `ChatAnthropic`, `ChatGoogleGenerativeAI`, or `ChatMistralAI` models with optional parameters like `api_key`, `base_url`, and `timeout`.

## Why use these helpers?

Instead of installing and importing separate provider libraries (`langchain_openai`, `langchain_ollama`, `langchain_anthropic`, etc.) and writing different initialization code for each platform, you can simply write:

```python
model = get_model(provider="openai", model_name="gpt-4o", api_key="your-api-key")
```

This keeps AI model setup simple, readable, and beginner-friendly while allowing you to easily switch between cloud and local AI providers with a single function call.
