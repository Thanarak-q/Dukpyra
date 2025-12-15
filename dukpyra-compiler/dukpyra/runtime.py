"""
Dukpyra Runtime Shim - Collects types during execution
"""
import json
import os
import inspect
from pathlib import Path
from functools import wraps
from typing import Optional, Any, Callable

try:
    from fastapi import FastAPI
except ImportError:
    FastAPI = None

class DukpyraRuntime:
    def __init__(self):
        self.app = FastAPI() if FastAPI else None
        self.collected_types = {}
        self.types_file = Path(".dukpyra/types.json")

    def _collect_type(self, func_name: str, arg_name: str, value: Any):
        """Record the type of an argument."""
        # Simple type mapping
        if isinstance(value, bool):
            type_name = "bool"
        elif isinstance(value, int):
            type_name = "int"
        elif isinstance(value, float):
            type_name = "float"
        elif isinstance(value, str):
            type_name = "str"
        else:
            type_name = "dynamic" # fallback

        # Initialize structure
        if func_name not in self.collected_types:
            self.collected_types[func_name] = {}
        
        # Only update if we don't have a specific type yet or if we see a conflict?
        # For now, last writer wins, or stick to first observed type.
        # Let's simple overwrite for now.
        self.collected_types[func_name][arg_name] = type_name
        
        # Save to file immediately (for simplicity in this proof of concept)
        self._save_types()

    def _save_types(self):
        self.types_file.parent.mkdir(exist_ok=True, parents=True)
        with open(self.types_file, "w") as f:
            json.dump(self.collected_types, f, indent=2)

    def _wrap_handler(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Inspect signature to map args/kwargs to parameter names
            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()
            
            for name, value in bound.arguments.items():
                self._collect_type(func.__name__, name, value)
            
            if inspect.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            return func(*args, **kwargs)
        return wrapper

    def get(self, path: str):
        def decorator(func):
            if self.app:
                self.app.get(path)(self._wrap_handler(func))
            return func
        return decorator

    def post(self, path: str):
        def decorator(func):
            if self.app:
                self.app.post(path)(self._wrap_handler(func))
            return func
        return decorator

    def put(self, path: str):
        def decorator(func):
            if self.app:
                self.app.put(path)(self._wrap_handler(func))
            return func
        return decorator
        
    def delete(self, path: str):
        def decorator(func):
            if self.app:
                self.app.delete(path)(self._wrap_handler(func))
            return func
        return decorator

    def patch(self, path: str):
        def decorator(func):
            if self.app:
                self.app.patch(path)(self._wrap_handler(func))
            return func
        return decorator

# Global instance
_runtime = DukpyraRuntime()

def app():
    """Factory function to get the FastAPI app (or the shim)"""
    return _runtime

# Raw C# decorator (Pass-through for runtime)
def raw_csharp(code: str):
    def decorator(func):
        return func
    return decorator
