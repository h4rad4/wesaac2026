"""Disk-backed response cache keyed by (prompt version, model, messages, kwargs).

Wraps OpenRouterProvider so every ``llm(role, ...).ainvoke(messages)`` first
checks ``results/cache/llm/<sha256>.json``.  Identical prompts (including the
base64 slide images) hit the cache instead of paying tokens/latency again --
this makes retries, resume runs and ablations nearly free.
"""

import hashlib
import json
import os
import threading
from pathlib import Path

from langchain_core.messages import AIMessage

from pipeline.llm import OpenRouterProvider

CACHE_VERSION = 1

def default_cache_dir():
    root = Path(__file__).resolve().parent.parent
    return root / "results" / "cache" / "llm"

def message_to_key(msg):
    """Reduce a message to plain data so it can be hashed. ToolMessage etc.
    carry tool_call_id / name which matter for the prompt."""
    content = getattr(msg, "content", msg)
    msg_type = getattr(msg, "type", "unknown")
    extra = {}
    for attr in ("tool_call_id", "name"):
        if getattr(msg, attr, None):
            extra[attr] = getattr(msg, attr)
    return {"type": msg_type, "content": content, **extra}

def cache_key(role, model, messages, kwargs, salt=""):
    payload = {
        "v": CACHE_VERSION,
        "role": role,
        "model": model,
        "salt": salt,
        "kwargs": {k: v for k, v in kwargs.items() if k != "callbacks"},
        "messages": [message_to_key(m) for m in messages],
    }
    blob = json.dumps(payload, sort_keys=True, ensure_ascii=False, default=str)
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()

class CachedLLM:
    """Drop-in stand-in for ChatOpenAI: supports .ainvoke and .bind_tools."""

    def __init__(self, inner, provider, role, salt=""):
        self._inner = inner
        self._provider = provider
        self._role = role
        self._salt = salt

    def bind_tools(self, tools, **kwargs):
        try:
            tool_salt = json.dumps([getattr(t, "name", str(t)) for t in tools], sort_keys=True)
        except TypeError:
            tool_salt = repr(tools)
        return CachedLLM(self._inner.bind_tools(tools, **kwargs),
                         self._provider, self._role, salt=self._salt + tool_salt)

    async def ainvoke(self, messages, **kwargs):
        model = getattr(self._inner, "model_name", None) or "unknown"
        key = cache_key(self._role, model, messages, kwargs, salt=self._salt)

        cached = self._provider.load(key)
        if cached and str(cached.get("content", "")).strip():
            return AIMessage(content=cached.get("content", ""),
                             tool_calls=cached.get("tool_calls") or [])

        reply = await self._inner.ainvoke(messages, **kwargs)

        has_content = isinstance(getattr(reply, "content", None), (str, list)) \
            and str(reply.content).strip()
        if has_content:
            self._provider.store(key, {
                "role": self._role,
                "model": model,
                "content": reply.content,
                "tool_calls": [
                    {"name": c["name"], "args": c["args"], "id": c.get("id"), "type": "tool_call"}
                    for c in (getattr(reply, "tool_calls", None) or [])
                ],
            })
        return reply

class CachingProvider(OpenRouterProvider):

    def __init__(self, *args, cache_dir=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_dir = Path(cache_dir) if cache_dir else default_cache_dir()
        self._lock = threading.Lock()

    def llm(self, role, **kwargs):
        return CachedLLM(super().llm(role, **kwargs), self, role)

    def _path(self, key):
        shard = self.cache_dir / key[:2]
        return shard / f"{key}.json"

    def load(self, key):
        path = self._path(key)
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            return None

    def store(self, key, data):
        with self._lock:
            path = self._path(key)
            path.parent.mkdir(parents=True, exist_ok=True)
            tmp = path.with_suffix(".tmp")
            tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            os.replace(tmp, path)

__all__ = ["CachingProvider", "CachedLLM", "cache_key"]
