from __future__ import annotations

import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Any, Callable, Dict


class SkillLoader:
    """Dynamically load python skill scripts and expose a callable registry."""

    def __init__(self, skill_dir: str) -> None:
        self.skill_dir = Path(skill_dir)
        self.registry: Dict[str, Callable[..., Any]] = {}

    def load_all(self) -> Dict[str, Callable[..., Any]]:
        for file in self.skill_dir.glob("*.py"):
            if file.name.startswith("_"):
                continue
            self._load_file(file)
        return self.registry

    def _load_file(self, file: Path) -> None:
        spec = importlib.util.spec_from_file_location(file.stem, file)
        if not spec or not spec.loader:
            raise RuntimeError(f"Unable to load skill: {file}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self._register_module(module)

    def _register_module(self, module: ModuleType) -> None:
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if callable(attr) and getattr(attr, "is_skill", False):
                self.registry[attr.__name__] = attr


def skill(func: Callable[..., Any]) -> Callable[..., Any]:
    func.is_skill = True
    return func
