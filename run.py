"""
run.py — Single-Command Launcher
AI-Powered Resume & ATS Optimizer

Author:
  • Vinayak Mamtani

Checks for required dependencies, installs any missing packages,
then launches the Streamlit application on port 8501.

Usage:
    python run.py
"""

import subprocess
import sys
import importlib
import os

# ──────────────────────────────────────────────────────────────
# REQUIRED PACKAGES
# Mapping: import_name -> pip_package_name
# ──────────────────────────────────────────────────────────────
REQUIRED_PACKAGES = {
    "streamlit":        "streamlit",
    "pdfplumber":       "pdfplumber",
    "thefuzz":          "thefuzz",
    "Levenshtein":      "python-Levenshtein",
    "plotly":           "plotly",
    "requests":         "requests",
    "pandas":           "pandas",
    "dotenv":           "python-dotenv",
}


def check_and_install():
    """Check each dependency and install if missing."""
    missing = []

    for import_name, pip_name in REQUIRED_PACKAGES.items():
        try:
            importlib.import_module(import_name)
        except ImportError:
            missing.append(pip_name)

    if missing:
        print("\n[*] Installing missing packages: {}\n".format(", ".join(missing)))
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "--quiet"] + missing
        )
        print("[OK] All packages installed successfully.\n")
    else:
        print("[OK] All dependencies are already installed.\n")


def launch_app():
    """Launch the Streamlit application."""
    app_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "app.py")

    if not os.path.exists(app_path):
        print("[ERROR] app.py not found at {}".format(app_path))
        sys.exit(1)

    print("[*] Launching ATS Resume Optimizer on http://localhost:8501 ...\n")

    subprocess.call([
        sys.executable, "-m", "streamlit", "run", app_path,
        "--server.port=8501",
        "--server.headless=true",
        "--browser.gatherUsageStats=false",
    ])


if __name__ == "__main__":
    print("=" * 60)
    print("  AI-Powered Resume & ATS Optimizer")
    print("  Author: Vinayak Mamtani")
    print("=" * 60)
    print()

    check_and_install()
    launch_app()
