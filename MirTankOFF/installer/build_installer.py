#!/usr/bin/env python3
"""Сборка установщика игры через PyInstaller."""

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DIST_DIR = ROOT / "dist"
BUILD_DIR = ROOT / "build"


def main():
    try:
        import PyInstaller  # noqa: F401
    except ImportError:
        print("Устанавливаю PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)

    command = [
        sys.executable,
        "-m",
        "PyInstaller",
        "--noconfirm",
        "--onefile",
        "--windowed",
        "--name",
        "MirTankoff",
        "--add-data",
        f"assets{';' if sys.platform == 'win32' else ':'}assets",
        str(ROOT / "main.py"),
    ]

    print("Запуск сборки:", " ".join(command))
    subprocess.check_call(command, cwd=ROOT)
    print(f"\nГотово! Исполняемый файл: {DIST_DIR / 'MirTankoff'}")


if __name__ == "__main__":
    main()
