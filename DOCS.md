# gemixy - Documentation

## Overview

Python SDK for Google Gemini. No API key, no server, no configuration needed.

- Direct Gemini web scraping
- Works out of the box
- Live API on Vercel

---

## Live API

**Base URL:** `https://gemini-openai-proxy-python.vercel.app/v1`

Works with any OpenAI-compatible client.

### cURL

```bash
curl https://gemini-openai-proxy-python.vercel.app/v1/models

curl https://gemini-openai-proxy-python.vercel.app/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini", "messages": [{"role": "user", "content": "Hello!"}]}'
```

### Python (OpenAI Library)

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

## Installation

```bash
pip install gemixy
```

---

## Quick Start

### Python SDK (Direct Gemini - No Server)

```python
from gemixy import GeminiClient

client = GeminiClient()
print(client.chat("Hello!"))
```

### Live API (OpenAI Compatible)

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

---

## SDK Methods (Direct Gemini)

### chat(message)

```python
from gemixy import GeminiClient

client = GeminiClient()
response = client.chat("What is AI?")
print(response)
```

### chat_stream(message)

```python
from gemixy import GeminiClient

client = GeminiClient()
for chunk in client.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

### messages(messages)

```python
from gemixy import GeminiClient

client = GeminiClient()
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is Python?"}
]
print(client.messages(messages))
```

### messages_stream(messages)

```python
from gemixy import GeminiClient

client = GeminiClient()
messages = [
    {"role": "system", "content": "You are a pirate"},
    {"role": "user", "content": "Tell me about treasure"}
]
for chunk in client.messages_stream(messages):
    print(chunk, end="", flush=True)
```

### models()

```python
from gemixy import GeminiClient

client = GeminiClient()
print(client.models())
```

---

## API Reference

| Method | Parameters | Returns | Description |
|--------|-----------|---------|-------------|
| `chat(message)` | `str` | `str` | Simple chat |
| `chat_stream(message)` | `str` | `Iterator[str]` | Streaming chat |
| `messages(messages)` | `List[dict]` | `str` | Chat with history |
| `messages_stream(messages)` | `List[dict]` | `Iterator[str]` | Streaming with history |
| `models()` | `None` | `dict` | List models |

---

## Server API Endpoints

Live: `https://gemini-openai-proxy-python.vercel.app/v1`

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/models` | List models |
| POST | `/v1/chat/completions` | Chat completions |

---

## Deploy Your Own

### Vercel

```bash
vercel --yes
```

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/pooraddyy/gemini-openai-proxy-python)

### Docker

```bash
docker build -t gemixy .
docker run -d -p 5000:5000 gemixy
```

### Local

```bash
git clone https://github.com/pooraddyy/gemini-openai-proxy-python.git
cd gemini-openai-proxy-python
pip install -r requirements.txt
python run.py
```

---

## Error Handling

SDK raises `RuntimeError` if Gemini doesn't respond:

```python
from gemixy import GeminiClient

client = GeminiClient()
try:
    response = client.chat("Hello!")
except RuntimeError as e:
    print(f"Error: {e}")
```

---

## License

[MIT](LICENSE) - pooraddyy
