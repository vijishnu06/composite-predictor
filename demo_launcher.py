"""Create a local environment once, prepare the saved model, and launch the demo."""
from pathlib import Path
import os
import subprocess
import sys

ROOT = Path(__file__).resolve().parent

def run(*args):
    subprocess.run([str(x) for x in args], cwd=ROOT, check=True)

def main():
    os.chdir(ROOT)
    executable = ROOT / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not executable.exists():
        print('Creating the project Python environment...', flush=True)
        run(sys.executable, '-m', 'venv', ROOT / '.venv')
    check = subprocess.run([str(executable), '-c', 'import streamlit, sklearn, pandas, matplotlib, joblib'], cwd=ROOT)
    if check.returncode:
        print('Installing dependencies. Internet access is needed for this first setup.', flush=True)
        run(executable, '-m', 'pip', 'install', '-r', 'requirements.txt')
    # Local artifacts are trusted project outputs. Version or integrity failure
    # triggers rebuilding from the supplied simulated CSV, never a downloaded model.
    check = subprocess.run([str(executable), '-c', 'from src.train import load_model; load_model()'], cwd=ROOT)
    if check.returncode:
        print('Rebuilding the simulated-data model for this Python environment...', flush=True)
        if not (ROOT / 'data/simulated/simulated_e_glass_epoxy.csv').exists():
            run(executable, '-m', 'src.simulate_data')
        run(executable, '-m', 'src.train')
    print('Opening the dashboard. Keep this window open; use Ctrl+C to stop.', flush=True)
    run(executable, '-m', 'streamlit', 'run', 'app.py', '--browser.gatherUsageStats=false')

if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError as exc:
        print(f'Setup or launch failed (exit {exc.returncode}). See the error above and DEMO_START_HERE.md.')
        sys.exit(exc.returncode)
