"""Optional adapter for a real OpenAI-compatible chat endpoint.

NOT required by any lab, test, or validate.py. It exists so that, after the
offline labs, you can point the *same* agent code at a real model by setting
environment variables:

  HF_MODEL_ENDPOINT   e.g. https://api.openai.com/v1/chat/completions
  HF_MODEL_NAME       e.g. gpt-4o-mini
  HF_MODEL_API_KEY    your key (read from the environment only)

The adapter asks the model to reply with one JSON action object and parses
it. A malformed reply is converted into a "say" action, never an exception
that escapes the loop.
"""
import json
import os
import urllib.request


class HttpModel:
    def __init__(self, endpoint=None, api_key=None, model_name=None, timeout=30):
        self.endpoint = endpoint or os.environ.get("HF_MODEL_ENDPOINT", "")
        self.api_key = api_key or os.environ.get("HF_MODEL_API_KEY", "")
        self.model_name = model_name or os.environ.get("HF_MODEL_NAME", "")
        self.timeout = timeout
        self.name = "http:" + (self.model_name or "unnamed")

    def respond(self, history, tool_names):
        if not self.endpoint:
            return {"type": "say", "text": "[http model: no endpoint configured]"}
        system = (
            "You are an agent. Reply with exactly one JSON object: "
            '{"type":"tool_call","name":<tool>,"args":{...}} or '
            '{"type":"final","text":<answer>}. Tools: ' + ", ".join(tool_names)
        )
        messages = [{"role": "system", "content": system}] + list(history)
        body = json.dumps({"model": self.model_name, "messages": messages}).encode()
        req = urllib.request.Request(
            self.endpoint, data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + self.api_key})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            data = json.loads(resp.read().decode())
        text = data["choices"][0]["message"]["content"]
        try:
            action = json.loads(text)
            if isinstance(action, dict) and action.get("type") in ("tool_call", "final", "say"):
                return action
        except (ValueError, TypeError):
            pass
        return {"type": "say", "text": text}
