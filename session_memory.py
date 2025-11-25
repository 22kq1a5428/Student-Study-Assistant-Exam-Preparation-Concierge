from typing import Dict, Any
import json
import os

class SessionMemory:
    def __init__(self, filepath: str = 'project_full/memory/_memory.json'):
        self.filepath = filepath
        self.store: Dict[str, Any] = {}
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, 'r', encoding='utf-8') as f:
                    self.store = json.load(f)
            except Exception:
                self.store = {}
        else:
            self.store = {}

    def _save(self):
        try:
            os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
            with open(self.filepath, 'w', encoding='utf-8') as f:
                json.dump(self.store, f, indent=2)
        except Exception:
            pass

    def get(self, key: str, default=None):
        return self.store.get(key, default)

    def set(self, key: str, value):
        self.store[key] = value
        self._save()

    def update_nested(self, section: str, key: str, value):
        sec = self.store.get(section, {})
        sec[key] = value
        self.set(section, sec)

    def to_dict(self):
        return dict(self.store)
