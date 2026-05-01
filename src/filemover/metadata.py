from __future__ import annotations
import json
import os
from json.decoder import JSONDecodeError

SCHEMA_VERSION = 1

class ExecutionResults:
    def __init__(self, executions: int = 1, copied: int = 0, moved: int = 0, deleted: int = 0, skipped: int = 0, errors: int = 0) -> None:
        self._executions = executions
        self._copied = copied
        self._moved = moved
        self._deleted = deleted
        self._skipped = skipped
        self._errors = errors
    
    @property
    def executions(self) -> int:
        return self._executions
    @property
    def copied(self) -> int:
        return self._copied
    @property
    def moved(self) -> int:
        return self._moved
    @property
    def deleted(self) -> int:
        return self._deleted
    @property
    def skipped(self) -> int:
        return self._skipped
    @property
    def errors(self) -> int:
        return self._errors
    
    def increment_copied(self, amount: int = 1):
        self._copied += amount
    def increment_moved(self, amount: int = 1):
        self._moved += amount
    def increment_deleted(self, amount: int = 1):
        self._deleted += amount
    def increment_skipped(self, amount: int = 1):
        self._skipped += amount
    def increment_errors(self, amount: int = 1):
        self._errors += amount
    
    def get_dict(self) -> dict:
        return {
            "executions": self._executions,
            "copied": self._copied,
            "moved": self._moved,
            "deleted": self._deleted,
            "skipped": self._skipped,
            "errors": self._errors,
        }

class Metadata:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        if not os.path.exists(file_path):
            try:
                with open(file_path, 'w') as f:
                    f.close()
            except BaseException as e:
                print(f"Failed to open provided metadata file")
                raise e

    def _is_data_valid(self, data: dict):
        if data is None:
            return False
        if data.get("_version") != SCHEMA_VERSION:
            return False
        return True

    def _validate_data(self, data: dict | None) -> dict:
        if data is None:
            return {"_version": SCHEMA_VERSION}
        if not data.get("_version") == SCHEMA_VERSION:
            # Add migrations here in the future... for now uhhhhh deal with it
            raise Exception(f"Metadata file has unknown schema version {data.get('_version')}. Current version: {SCHEMA_VERSION}")
        return data

    def _load_data(self) -> dict:
        data = None
        with open(self.file_path, "r") as f:
            try:
                data = json.load(f)
            except JSONDecodeError:
                pass
        return self._validate_data(data)
    
    def _save_data(self, data: dict):
        if not self._is_data_valid(data):
            return
        validated = self._validate_data(data)
        with open(self.file_path, "w") as f:
            f.write(json.dumps(validated, indent=4, sort_keys=True))
        

    def update(self, mover_id: str, results: ExecutionResults):
        data = self._load_data()
        if not data.get(mover_id):
            data[mover_id] = ExecutionResults(executions=0).get_dict()
        data[mover_id]["executions"] += results.executions
        data[mover_id]["copied"] += results.copied
        data[mover_id]["moved"] += results.moved
        data[mover_id]["deleted"] += results.deleted
        data[mover_id]["skipped"] += results.skipped
        data[mover_id]["errors"] += results.errors
        self._save_data(data)


    def get_data(self, mover_id: str):
        data = self._load_data()
        if not data.get(mover_id):
            return ExecutionResults(executions=0)
        return ExecutionResults(
            executions=data.get("executions", 0), 
            copied=data.get("copied", 0),
            moved=data.get("moved", 0),
            deleted=data.get("deleted", 0),
            skipped=data.get("skipped", 0),
            errors=data.get("errors", 0),
        )

    def get_execution_count(self, mover_id: str):
        data = self._load_data()
        if not data.get(mover_id):
            return 0
        return data[mover_id]["executions"]

    def get_moved_count(self, mover_id: str):
        data = self._load_data()
        if not data.get(mover_id):
            return 0
        return data[mover_id]["moved"]

    def get_copied_count(self, mover_id: str):
        data = self._load_data()
        if not data.get(mover_id):
            return 0
        return data[mover_id]["copied"]
    
    def get_deleted_count(self, mover_id: str):
        data = self._load_data()
        if not data.get(mover_id):
            return 0
        return data[mover_id]["deleted"]
    
    def get_skipped_count(self, mover_id: str):
        data = self._load_data()
        if not data.get(mover_id):
            return 0
        return data[mover_id]["skipped"]

    def get_error_count(self, mover_id: str):
        data = self._load_data()
        if not data.get(mover_id):
            return 0
        return data[mover_id]["errors"]
