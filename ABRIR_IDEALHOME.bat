@echo off
setlocal
cd /d "%~dp0"
title IDEALHOME - Abrir site

where py >nul 2>nul
if %errorlevel%==0 (set "PY=py") else (set "PY=python")

if not exist ".venv\Scripts\python.exe" (
    echo [1/4] A instalar o ambiente Python...
    %PY% -m venv .venv
    if errorlevel 1 goto ERRO
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 goto ERRO
)

set "PYTHON=.venv\Scripts\python.exe"

echo [2/4] A preparar a base de dados...
%PYTHON% manage.py migrate --noinput
if errorlevel 1 goto ERRO

echo [3/4] A carregar os anuncios rapidamente...
%PYTHON% manage.py import_properties --clear
if errorlevel 1 goto ERRO

echo [4/4] A iniciar o servidor na rede local...

start "IDEALHOME SERVER" /min cmd /c "cd /d ""%~dp0"" && "%~dp0.venv\Scripts\python.exe" manage.py runserver 0.0.0.0:8000"

timeout /t 3 /nobreak >nul
start "" "http://127.0.0.1:8000/"

echo.
echo ==========================================
echo IDEALHOME ABERTO EM http://127.0.0.1:8000/
echo Pode fechar esta janela. O servidor fica ativo.
echo ==========================================
echo.
endlocal
exit /b 0

:ERRO
echo.
echo ==========================================
echo ERRO AO PREPARAR O IDEALHOME.
echo ==========================================
echo Verifique a mensagem acima.
pause
exit /b 1
