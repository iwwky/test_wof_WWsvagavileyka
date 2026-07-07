#!/bin/bash
set -e

echo "=== Установка игры «Мир Танкофф» ==="

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python 3 не найден. Установите Python 3.9+"
  exit 1
fi

python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo
echo "Установка завершена."
echo "Запуск: ./run_game.sh"
