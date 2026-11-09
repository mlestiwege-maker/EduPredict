"""ML runtime wrapper. Uses in-venv deps if available, else calls system python ML runner."""
from __future__ import annotations
import json, subprocess, sys
from pathlib import Path
from typing import Dict, Any

ROOT = Path(__file__).resolve().parents[3]
RUNNER = ROOT / 'ml' / 'run_ml.py'

def _sys_call(cmd: str, checkpoint: str) -> Dict[str, Any]:
    p = subprocess.run(['/usr/bin/python3', str(RUNNER), cmd, checkpoint], capture_output=True, text=True, cwd=str(ROOT), timeout=300)
    if p.returncode != 0:
        return {'status':'error','error': (p.stderr or p.stdout)[-1200:]}
    try:
        return json.loads(p.stdout)
    except Exception:
        # find last json object
        s=p.stdout.strip(); i=s.rfind('{');
        return json.loads(s[i:]) if i>=0 else {'status':'error','error':'Invalid ML output','raw':s[-800:]}

def status() -> Dict[str,Any]:
    try:
        return _sys_call('status','week_4')
    except Exception as e:
        return {'dataset_exists': (ROOT/'ml/data/sample/buse').exists(), 'models':[], 'reports':[], 'error': str(e)}

def train(checkpoint='week_4') -> Dict[str, Any]:
    return _sys_call('train', checkpoint)

def predict(checkpoint='week_4') -> Dict[str, Any]:
    return _sys_call('predict', checkpoint)
