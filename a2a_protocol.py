from __future__ import annotations
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, Callable, Optional, List
import time
import uuid
import json
import threading
import queue

class A2AProtocolError(Exception):
    pass

class InvalidMessageError(A2AProtocolError):
    pass

@dataclass
class Message:
    id: str
    timestamp: float
    session_id: str
    sender: str
    receiver: str
    type: str
    content: Dict[str, Any] = field(default_factory=dict)
    meta: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

def _now_ts() -> float:
    return time.time()

def _new_uuid() -> str:
    return str(uuid.uuid4())

def create_message(
    sender: str,
    receiver: str,
    msg_type: str,
    content: Optional[Dict[str, Any]] = None,
    session_id: Optional[str] = None,
    meta: Optional[Dict[str, Any]] = None,
) -> Message:
    content = content or {}
    meta = meta or {}
    session_id = session_id or _new_uuid()

    msg = Message(
        id=_new_uuid(),
        timestamp=_now_ts(),
        session_id=session_id,
        sender=str(sender),
        receiver=str(receiver),
        type=str(msg_type),
        content=content,
        meta=meta,
    )

    validate_message(msg)
    return msg

def validate_message(msg: Message) -> None:
    if not isinstance(msg, Message):
        raise InvalidMessageError("msg must be Message instance")
    if not msg.sender or not isinstance(msg.sender, str):
        raise InvalidMessageError("sender must be non-empty string")
    if not msg.receiver or not isinstance(msg.receiver, str):
        raise InvalidMessageError("receiver must be non-empty string")
    if not msg.type or not isinstance(msg.type, str):
        raise InvalidMessageError("type must be non-empty string")
    try:
        json.dumps(msg.content)
    except (TypeError, ValueError) as e:
        raise InvalidMessageError(f"content must be JSON-serializable: {e}") from e
    try:
        json.dumps(msg.meta)
    except (TypeError, ValueError) as e:
        raise InvalidMessageError(f"meta must be JSON-serializable: {e}") from e

def serialize_message(msg: Message) -> str:
    validate_message(msg)
    return json.dumps(msg.to_dict(), separators=(",", ":"), ensure_ascii=False)

def deserialize_message(s: str) -> Message:
    try:
        obj = json.loads(s)
    except json.JSONDecodeError as e:
        raise InvalidMessageError(f"invalid JSON: {e}") from e
    required = {"id","timestamp","session_id","sender","receiver","type","content","meta"}
    if not required.issubset(set(obj.keys())):
        missing = required - set(obj.keys())
        raise InvalidMessageError(f"missing required fields: {missing}")
    msg = Message(
        id=str(obj["id"]),
        timestamp=float(obj["timestamp"]),
        session_id=str(obj["session_id"]),
        sender=str(obj["sender"]),
        receiver=str(obj["receiver"]),
        type=str(obj["type"]),
        content=obj.get("content", {}),
        meta=obj.get("meta", {}),
    )
    validate_message(msg)
    return msg

class A2ABroker:
    def __init__(self) -> None:
        self._queues: Dict[str, queue.Queue] = {}
        self._handlers: Dict[str, Callable[[Message], None]] = {}
        self._lock = threading.Lock()

    def _ensure_queue(self, receiver: str) -> queue.Queue:
        with self._lock:
            if receiver not in self._queues:
                self._queues[receiver] = queue.Queue()
            return self._queues[receiver]

    def register_handler(self, receiver: str, handler: Callable[[Message], None]) -> None:
        with self._lock:
            self._handlers[receiver] = handler
            self._ensure_queue(receiver)

    def unregister_handler(self, receiver: str) -> None:
        with self._lock:
            self._handlers.pop(receiver, None)

    def send(self, msg: Message) -> None:
        validate_message(msg)
        q = self._ensure_queue(msg.receiver)
        q.put(msg)
        handler = self._handlers.get(msg.receiver)
        if handler:
            threading.Thread(target=handler, args=(msg,), daemon=True).start()

    def poll(self, receiver: str, timeout: Optional[float] = None) -> Optional[Message]:
        q = self._ensure_queue(receiver)
        try:
            msg = q.get(timeout=timeout)
            return msg
        except queue.Empty:
            return None

    def start_worker_thread(self, receiver: str, handler: Callable[[Message], None]) -> threading.Thread:
        self.register_handler(receiver, handler)
        def _loop():
            q = self._ensure_queue(receiver)
            while True:
                try:
                    msg = q.get()
                    if msg is None:
                        continue
                    try:
                        handler(msg)
                    except Exception:
                        pass
                except Exception:
                    continue
        t = threading.Thread(target=_loop, daemon=True)
        t.start()
        return t

def ensure_session_id(session_id: Optional[str]) -> str:
    return session_id if session_id else _new_uuid()

def add_meta(msg: Message, key: str, value: Any) -> None:
    msg.meta[key] = value

def example_flow_demo() -> str:
    broker = A2ABroker()
    def worker_handler(msg: Message) -> None:
        msg.meta["processed_by"] = "worker_handler"
        print("Worker got message:", serialize_message(msg))
    broker.register_handler("worker", worker_handler)
    msg = create_message(sender="planner", receiver="worker", msg_type="plan", content={"plan": "do X"}, session_id=None)
    broker.send(msg)
    return serialize_message(msg)

if __name__ == "__main__":
    print("A2A demo:")
    print(example_flow_demo())
