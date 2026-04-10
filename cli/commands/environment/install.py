import os
import subprocess
import sys
from infrastructure.persistence.lock.lock_reader import read_lock


ENV_PATH = ".mypm/venv"


def create_venv():
    if not os.path.exists(ENV_PATH):
        print("Creating virtual environment...")
        subprocess.run([sys.executable, "-m", "venv", ENV_PATH], check=True)


def get_pip_path():
    if os.name == "nt":
        return os.path.join(ENV_PATH, "Scripts", "pip")
    else:
        return os.path.join(ENV_PATH, "bin", "pip")


def run(args):
    if not os.path.exists("mypm.lock"):
        print("❌ No lock file found. Run resolve first.")
        return

    lock = read_lock()

    print("=== Installing Packages (REAL) ===")

    create_venv()
    pip_path = get_pip_path()

    for pkg, ver in lock.items():
        print(f"Installing {pkg}=={ver} ...")
        subprocess.run(
    [pip_path, "install", f"{pkg}=={ver}", "--only-binary=:all:"],
    check=True
)

    print("✔ Install complete (real environment)")