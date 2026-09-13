from flask import Flask, request, Response, stream_with_context, jsonify
import json
import uuid
import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gemini.core import chat_with_gemini, messages_to_prompt, ok_response, chunk_response, chunk_done

app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "message": "Gemini OpenAI Proxy",
        "endpoints": [
            "GET  /v1/models",
            "GET  /v1/models/<model>",
            "POST /v1/chat/completions"
        ]
    })


@app.route('/v1/models')
def list_models():
    return jsonify({
        "object": "list",
        "data": [
            {
                "id": "gemini",
                "object": "model",
                "created": 1686935002,
                "owned_by": "google"
            }
        ]
    })


@app.route('/v1/models/<model_id>')
def retrieve_model(model_id):
    return jsonify({
        "id": model_id,
        "object": "model",
        "created": 1686935002,
        "owned_by": "google"
    })


@app.route('/v1/chat/completions', methods=['POST'])
def chat_completions():
    body = request.get_json(force=True)
    messages = body.get("messages", [])
    model = body.get("model", "gemini")
    stream = body.get("stream", False)

    if not messages:
        return jsonify({"error": {"message": "messages is required", "type": "invalid_request_error"}}), 400

    prompt = messages_to_prompt(messages)
    if not prompt.strip():
        return jsonify({"error": {"message": "empty prompt", "type": "invalid_request_error"}}), 400

    resp_id = f"chatcmpl-{uuid.uuid4().hex}"
    created = int(time.time())

    result = chat_with_gemini(prompt)
    if not result:
        return jsonify({"error": {"message": "Gemini did not respond", "type": "server_error"}}), 500

    if stream:
        def generate():
            for word in result.split():
                chunk = chunk_response(word + " ", resp_id, created, model)
                yield f"data: {json.dumps(chunk)}\n\n"
                time.sleep(0.01)
            done = chunk_done(resp_id, created, model)
            yield f"data: {json.dumps(done)}\n\n"
            yield "data: [DONE]\n\n"

        return Response(
            stream_with_context(generate()),
            content_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "X-Accel-Buffering": "no"
            }
        )

    return jsonify(ok_response(result, model, resp_id))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, threaded=True)
