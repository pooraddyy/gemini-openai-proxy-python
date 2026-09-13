<div align="center">

# gemixy

### Python SDK for Google Gemini - No API Key Needed

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-gemixy-red.svg)](https://pypi.org/project/gemixy/)

---

Direct Gemini access via web scraping. No API key, no server, no setup.

**Live API:** `https://gemini-openai-proxy-python.vercel.app/v1`

[Installation](#installation) | [Quick Start](#quick-start) | [Docs](DOCS.md)

</div>

---

## Installation

```bash
pip install gemixy
```

---

## Quick Start

```python
from gemixy import GeminiClient

client = GeminiClient()
print(client.chat("Hello!"))
```

---

## Features

- **Zero config** - just `pip install gemixy` and use
- **No API key** - uses Gemini web scraping
- **No server needed** - works directly in Python
- **OpenAI compatible** - drop-in replacement
- **Streaming support** - real-time responses
- **Live API** - deployed on Vercel

---

## Usage

### Simple Chat

```python
from gemixy import GeminiClient

client = GeminiClient()
print(client.chat("What is AI?"))
```

### Streaming

```python
from gemixy import GeminiClient

client = GeminiClient()
for chunk in client.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

### Message History

```python
from gemixy import GeminiClient

client = GeminiClient()
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is Python?"}
]
print(client.messages(messages))
```

### List Models

```python
from gemixy import GeminiClient

client = GeminiClient()
print(client.models())
```

---

## Live API

**Base URL:** `https://gemini-openai-proxy-python.vercel.app/v1`

### cURL

```bash
curl https://gemini-openai-proxy-python.vercel.app/v1/models

curl https://gemini-openai-proxy-python.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### OpenAI Library

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://gemini-openai-proxy-python.vercel.app/v1",
    api_key="any-key"
)

response = client.chat.completions.create(
    model="gemini",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Streaming

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://gemini-openai-proxy-python.vercel.app/v1",
    api_key="any-key"
)

stream = client.chat.completions.create(
    model="gemini",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/models` | List models |
| POST | `/v1/chat/completions` | Chat completions |

---

## License

[MIT](LICENSE) - pooraddyy
