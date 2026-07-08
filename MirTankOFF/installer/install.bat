@echo off
chcp 65001 >nul
echo === Установка игры "Мир Танкофф" ===

python --version >nul 2>&1
if errorlevel 1 (
    echo Python не найден. Установите Python 3.9+ с https://python.org
    pause
    exit /b 1
)

python -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

echo.
echo Установка завершена.
echo Запуск: run_game.bat
pause
