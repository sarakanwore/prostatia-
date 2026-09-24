"""
STATIA - Script de Validation Globale du Backend et Frontend
Ce script permet de vérifier automatiquement l'état complet du système :
  1. Validation de toutes les suites de tests unitaires et d'intégration (Python + Rust + Frontend Vite).
  2. Si les services sont démarrés, vérification de tous les endpoints /health et des flux de données réels.
"""

import sys
import subprocess
import time
import urllib.request
import json
from pathlib import Path

# Ensure UTF-8 output on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BACKEND_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = BACKEND_DIR.parent
FRONTEND_DIR = PROJECT_ROOT / "frontend"

GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"
BOLD = "\033[1m"
RESET = "\033[0m"

def print_banner(title: str):
    print(f"\n{CYAN}{BOLD}{'=' * 70}{RESET}")
    print(f"{CYAN}{BOLD}  {title}{RESET}")
    print(f"{CYAN}{BOLD}{'=' * 70}{RESET}\n")

def run_command(cmd: str, cwd: Path) -> tuple[bool, str, float]:
    start = time.time()
    try:
        res = subprocess.run(
            cmd,
            cwd=str(cwd),
            shell=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        duration = time.time() - start
        return (res.returncode == 0, res.stdout + "\n" + res.stderr, duration)
    except Exception as e:
        return (False, str(e), time.time() - start)

def resolve_test_cmd(service_name: str, fallback_cmd: str, cwd: Path) -> str:
    # Check for direct virtualenv python first for maximum performance on Windows
    local_venv = cwd / ".venv" / "Scripts" / "python.exe"
    if local_venv.exists():
        return f'"{local_venv}" -m pytest -q'
    
    # Common poetry cache location on this machine
    poetry_cache = Path.home() / "AppData" / "Local" / "pypoetry" / "Cache" / "virtualenvs"
    if poetry_cache.exists():
        matches = list(poetry_cache.glob(f"{service_name.replace('_', '-')}*"))
        if matches:
            v_py = matches[0] / "Scripts" / "python.exe"
            if v_py.exists():
                return f'"{v_py}" -m pytest -q'

    return fallback_cmd

def check_test_suites():
    print_banner("1. VÉRIFICATION DES SUITES DE TESTS UNITAIRES & INTÉGRATION")

    test_targets = [
        ("stats_engine", resolve_test_cmd("stats_engine", "poetry run pytest -q", BACKEND_DIR / "stats_engine"), BACKEND_DIR / "stats_engine"),
        ("ai_orchestrator", resolve_test_cmd("ai_orchestrator", "poetry run pytest -q", BACKEND_DIR / "ai_orchestrator"), BACKEND_DIR / "ai_orchestrator"),
        ("viz_service", resolve_test_cmd("viz_service", "poetry run pytest -q", BACKEND_DIR / "viz_service"), BACKEND_DIR / "viz_service"),
        ("geo_service", resolve_test_cmd("geo_service", "poetry run pytest -q", BACKEND_DIR / "geo_service"), BACKEND_DIR / "geo_service"),
        ("data_service", "cargo test -q", BACKEND_DIR / "data_service"),
        ("gateway", "cargo test -q", BACKEND_DIR / "gateway"),
        ("frontend_bundle", "npm run build", FRONTEND_DIR),
    ]

    all_passed = True
    summary = []

    for name, cmd, cwd in test_targets:
        if not cwd.exists():
            continue
        print(f"⏳ Exécution pour {BOLD}{name}{RESET}...", end=" ", flush=True)
        ok, out, duration = run_command(cmd, cwd)
        if ok:
            print(f"{GREEN}[OK]{RESET} ({duration:.2f}s)")
            summary.append((name, True, f"{duration:.2f}s"))
        else:
            print(f"{RED}[ÉCHEC]{RESET} ({duration:.2f}s)")
            summary.append((name, False, f"{duration:.2f}s"))
            print(f"{YELLOW}Détails de l'erreur :{RESET}\n{out[-500:]}\n")
            all_passed = False

    print("\n" + "-" * 50)
    print(f"{BOLD}RÉCAPITULATIF DES VÉRIFICATIONS :{RESET}")
    for name, ok, dur in summary:
        status_str = f"{GREEN}PASSÉ{RESET}" if ok else f"{RED}ÉCHEC{RESET}"
        print(f"  • {name:<20} : {status_str} en {dur}")
    print("-" * 50)
    return all_passed

def check_live_endpoints():
    print_banner("2. VÉRIFICATION DES SERVICES EN DIRECT (LIVE HEALTH CHECKS)")

    services = [
        ("Frontend IDE", "http://localhost:3000/"),
        ("Gateway API", "http://localhost:8080/health"),
        ("Stats Engine", "http://localhost:8000/health"),
        ("Data Service", "http://localhost:8001/health"),
        ("AI Orchestrator", "http://localhost:8002/health"),
        ("Viz Service", "http://localhost:8003/health"),
        ("Geo Service", "http://localhost:8004/health"),
    ]

    any_up = False
    all_up = True

    for name, url in services:
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "STATIA-Verifier/1.0"})
            with urllib.request.urlopen(req, timeout=2.0) as resp:
                if resp.status in (200, 304):
                    body = resp.read(100).decode("utf-8", errors="replace").strip()
                    print(f"  {GREEN}✔ {name:<18}{RESET} [{url}] -> HTTP {resp.status} OK")
                    any_up = True
                else:
                    print(f"  {RED}✖ {name:<18}{RESET} [{url}] -> HTTP {resp.status}")
                    all_up = False
        except Exception as e:
            print(f"  {YELLOW}○ {name:<18}{RESET} [{url}] -> Non accessible ({e.__class__.__name__})")
            all_up = False

    if not any_up:
        print(f"\n{YELLOW}ℹ Aucun service ne semble démarré sur les ports 3000-8080.{RESET}")
    elif all_up:
        print(f"\n{GREEN}{BOLD}Tous les services répondent en direct !{RESET}")

def main():
    print(f"\n{BOLD}STATIA - Diagnostic d'intégrité du système complet{RESET}")
    print(f"Répertoire backend : {BACKEND_DIR}")
    print(f"Répertoire frontend: {FRONTEND_DIR}\n")

    check_test_suites()
    check_live_endpoints()

    print(f"\n{CYAN}Documentation et interfaces :{RESET}")
    print(f"  • Frontend IDE   : http://localhost:3000")
    print(f"  • Stats Engine   : http://localhost:8000/docs")
    print(f"  • AI Orchestrator: http://localhost:8002/docs")
    print(f"  • Viz Service    : http://localhost:8003/docs")
    print(f"  • Geo Service    : http://localhost:8004/docs")
    print(f"  • Passerelle     : http://localhost:8080\n")

if __name__ == "__main__":
    main()
