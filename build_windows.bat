@echo off
REM ALLOH UCHUN — Windows 10/11 da ALLOH_UCHUN.exe yig'ish skripti
setlocal
cd /d "%~dp0"

where python >nul 2>nul || (echo Python 3 topilmadi. https://www.python.org dan o'rnating. & exit /b 1)

if not exist .venv (
    python -m venv .venv || exit /b 1
)
call .venv\Scripts\activate.bat || exit /b 1

python -m pip install --upgrade pip || exit /b 1
python -m pip install -r requirements.txt || exit /b 1

echo === Testlar ===
set QT_QPA_PLATFORM=offscreen
python -m pytest -q || (echo Testlar muvaffaqiyatsiz. Yig'ish to'xtatildi. & exit /b 1)
set QT_QPA_PLATFORM=

echo === PyInstaller ===
python -m PyInstaller --noconfirm --clean ALLOH_UCHUN.spec || exit /b 1

if exist dist\ALLOH_UCHUN.exe (
    echo.
    echo TAYYOR: %cd%\dist\ALLOH_UCHUN.exe
) else (
    echo Xato: dist\ALLOH_UCHUN.exe yaratilmadi. & exit /b 1
)
endlocal
