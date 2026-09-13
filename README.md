<div align="center">

# gemixy

### Python SDK for Google Gemini - No API Key Needed

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-3776AB.svg)](https://www.python.org/)
[![PyPI](https://img.shields.io/badge/PyPI-gemixy-red.svg)](https://pypi.org/project/gemixy/)

---

Direct Gemini access via web scraping. No API key, no server, no setup.

[Installation](#installation) | [Quick Start](#quick-start) | [Deploy Server](#deploy-server) | [Docs](DOCS.md)

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

That's it. No API key. No server. No configuration.

---

## Features

- **Zero config** - just `pip install gemixy` and use
- **No API key** - uses Gemini web scraping
- **No server needed** - works directly in Python
- **OpenAI compatible** - drop-in replacement
- **Streaming support** - real-time responses

---

## SDK Usage

### Simple Chat

```python
from gemixy import GeminiClient

client = GeminiClient()
response = client.chat("What is AI?")
print(response)
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

## Deploy Server

Optional - if you want an OpenAI-compatible API server:

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

Server starts at `http://localhost:5000`

---

## API Server Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/v1/models` | List models |
| POST | `/v1/chat/completions` | Chat completions |

### cURL Examples

```bash
curl http://localhost:5000/v1/models

curl http://localhost:5000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model": "gemini", "messages": [{"role": "user", "content": "Hello!"}]}'
```

---

## OpenAI Client Library

Works with official OpenAI library (requires server):

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

## License

[MIT](LICENSE) - pooraddyy
