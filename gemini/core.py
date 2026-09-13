import json
import re
import uuid
import time
import requests

def extract_snlm0e_token(html):
    for pattern in [r'"SNlM0e":"([^"]+)"', r'"FdrFJe":"([^"]+)"', r'"cfb2h":"([^"]+)"']:
        match = re.search(pattern, html)
        if match and len(match.group(1)) > 20:
            return match.group(1)
    return None

def extract_build_params(html):
    params = {}
    bl = re.search(r'boq[_-]assistant[^"\']*_(\d+\.\d+[^"\']*)', html)
    if bl:
        params['bl'] = f'boq_assistant-bard-web-server_{bl.group(1)}'
    fsid = re.search(r'f\.sid["\']?\s*[:=]\s*["\']?([^"\'&\s]+)', html)
    if fsid:
        params['fsid'] = fsid.group(1)
    reqid = re.search(r'_reqid["\']?\s*[:=]\s*["\']?(\d+)', html)
    if reqid:
        params['reqid'] = int(reqid.group(1))
    params.setdefault('bl', 'boq_assistant-bard-web-server_20251217.07_p5')
    params.setdefault('fsid', str(-1 * int(time.time() * 1000)))
    params.setdefault('reqid', int(time.time() * 1000) % 1000000)
    return params

def get_session():
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
    }
    resp = session.get('https://gemini.google.com/app', headers=headers, timeout=30)
    snlm0e = extract_snlm0e_token(resp.text)
    if not snlm0e:
        return None
    params = extract_build_params(resp.text)
    return {'session': session, 'snlm0e': snlm0e, **params}

def build_payload(prompt, snlm0e):
    escaped = prompt.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n')
    rid = str(uuid.uuid4()).upper()
    payload = [
        [escaped, 0, None, None, None, None, 0],
        ["en-US"],
        ["", "", "", None, None, None, None, None, None, ""],
        snlm0e, uuid.uuid4().hex, None, [0], 1,
        None, None, 1, 0, None, None, None, None, None,
        [[0]], 0, None, None, None, None, None, None, None, None, 1, None, None,
        [4], None, None, None, None, None, None, None, None, None, None,
        [2], None, None, None, None, None, None, None, None, None, None, None,
        0, None, None, None, None, None, rid, None, []
    ]
    p = json.dumps(payload, separators=(',', ':')).replace('\\', '\\\\').replace('"', '\\"')
    return {'f.req': f'[null,"{p}"]', '': ''}

def parse_response(text):
    full = ""
    for line in text.strip().split('\n'):
        if not line or line.startswith(')]}'):
            continue
        try:
            data = json.loads(line)
            if isinstance(data, list) and data[0][0] == "wrb.fr" and len(data[0]) > 2:
                inner = data[0][2]
                if inner:
                    parsed = json.loads(inner)
                    if isinstance(parsed, list) and len(parsed) > 4:
                        content = parsed[4]
                        if isinstance(content, list) and len(content) > 0:
                            item = content[0]
                            if isinstance(item, list) and len(item) > 1:
                                arr = item[1]
                                if isinstance(arr, list) and len(arr) > 0 and isinstance(arr[0], str):
                                    if len(arr[0]) > len(full):
                                        full = arr[0]
        except Exception:
            continue
    return full.replace('\\n', '\n').replace('\\"', '"').replace('\\\\', '\\') if full else None

def chat_with_gemini(prompt):
    data = get_session()
    if not data:
        return None
    sess = data['session']
    url = (f"https://gemini.google.com/_/BardChatUi/data/assistant.lamda.BardFrontendService/StreamGenerate"
           f"?bl={data['bl']}&f.sid={data['fsid']}&hl=en-US&_reqid={data['reqid']}&rt=c")
    cookie = '; '.join(f"{k}={v}" for k, v in sess.cookies.items())
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
        'x-same-domain': '1',
        'origin': 'https://gemini.google.com',
        'referer': 'https://gemini.google.com/',
        'Cookie': cookie,
    }
    resp = sess.post(url, data=build_payload(prompt, data['snlm0e']), headers=headers, timeout=60)
    if resp.status_code != 200:
        return None
    return parse_response(resp.text)

def messages_to_prompt(messages):
    parts = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if isinstance(content, str):
            if role == "system":
                parts.append(f"[System]: {content}")
            elif role == "assistant":
                parts.append(f"[Assistant]: {content}")
            else:
                parts.append(content)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict) and item.get("type") == "text":
                    parts.append(item.get("text", ""))
    return "\n".join(parts)

def ok_response(text, model, req_id=None):
    return {
        "id": req_id or f"chatcmpl-{uuid.uuid4().hex}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": model,
        "choices": [{
            "index": 0,
            "message": {"role": "assistant", "content": text},
            "finish_reason": "stop"
        }],
        "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
    }

def chunk_response(text, resp_id, created, model):
    return {
        "id": resp_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {"content": text},
            "finish_reason": None
        }]
    }

def chunk_done(resp_id, created, model):
    return {
        "id": resp_id,
        "object": "chat.completion.chunk",
        "created": created,
        "model": model,
        "choices": [{
            "index": 0,
            "delta": {},
            "finish_reason": "stop"
        }]
    }
