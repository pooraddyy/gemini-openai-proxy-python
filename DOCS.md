# gemixy - Documentation

## Overview

Python SDK for Google Gemini. No API key, no server, no configuration needed.

- Direct Gemini web scraping
- Works out of the box
- Optional OpenAI-compatible API server

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

## SDK Methods

### chat(message)

Simple chat with Gemini.

```python
from gemixy import GeminiClient

client = GeminiClient()
response = client.chat("What is AI?")
print(response)
```

### chat_stream(message)

Streaming chat - yields words one by one.

```python
from gemixy import GeminiClient

client = GeminiClient()
for chunk in client.chat_stream("Tell me a story"):
    print(chunk, end="", flush=True)
```

### messages(messages)

Chat with message history (system, user, assistant roles).

```python
from gemixy import GeminiClient

client = GeminiClient()
messages = [
    {"role": "system", "content": "You are a helpful assistant"},
    {"role": "user", "content": "What is Python?"}
]
response = client.messages(messages)
print(response)
```

### messages_stream(messages)

Streaming chat with message history.

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

List available models.

```python
from gemixy import GeminiClient

client = GeminiClient()
print(client.models())
# {'object': 'list', 'data': [{'id': 'gemini', ...}]}
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

## Deploy Server (Optional)

If you need an OpenAI-compatible API server for other tools:

### Vercel

```bash
npm i -g vercel
vercel login
vercel --yes
```

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/pooraddyy/gemini-openai-proxy-python)

### Docker

```bash
docker build -t gemixy .
docker run -d -p 5000:5000 gemixy
```

### Local Server

```bash
git clone https://github.com/pooraddyy/gemini-openai-proxy-python.git
cd gemini-openai-proxy-python
pip install -r requirements.txt
python run.py
```

Server starts at `http://localhost:5000`

---

## Server API Endpoints

### List Models

```http
GET /v1/models
```

Response:
```json
{
  "object": "list",
  "data": [
    {"id": "gemini", "object": "model", "owned_by": "google"}
  ]
}
```

### Chat Completions

```http
POST /v1/chat/completions
Content-Type: application/json
```

Body:
```json
{
  "model": "gemini",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "stream": false
}
```

Response:
```json
{
  "id": "chatcmpl-abc123",
  "object": "chat.completion",
  "model": "gemini",
  "choices": [
    {
      "index": 0,
      "message": {"role": "assistant", "content": "Hello!"},
      "finish_reason": "stop"
    }
  ]
}
```

---

## OpenAI Client Library

Works with official OpenAI library (requires server running):

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:5000/v1",
    api_key="any-key"
)

response = client.chat.completions.create(
    model="gemini",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
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

## Project Structure

```
gemixy/
├── gemixy/
│   ├── __init__.py       # SDK (no server needed)
├── gemini/
│   ├── __init__.py
│   └── core.py           # Gemini scraping logic
├── api/
│   └── index.py          # Vercel serverless function
├── run.py                # Local dev server
├── setup.py              # PyPI package
├── Dockerfile
├── vercel.json
├── requirements.txt
├── DOCS.md
└── README.md
```

---

## License

[MIT](LICENSE) - pooraddyy
