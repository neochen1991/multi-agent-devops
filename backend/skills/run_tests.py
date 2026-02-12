from __future__ import annotations

import subprocess

from backend.core.skill_loader import skill


@skill
def run_pytest(path: str) -> dict:
    proc = subprocess.run(["pytest", path, "-q"], capture_output=True, text=True)
    return {"returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr}
