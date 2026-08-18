@echo off
setlocal
cd /d "%~dp0"
title IDEALHOME - Abrir site

echo ==========================================
echo       IDEALHOME - PREPARAR E ABRIR
 echo ==========================================

where py >nul 2>nul
if %errorlevel%==0 (set "PY=py") else (set "PY=python")

if not exist ".venv\Scripts\python.exe" (
    echo [1/4] A instalar o ambiente...
    %PY% -m venv .venv
    if errorlevel 1 goto ERRO
    .venv\Scripts\python.exe -m pip install -r requirements.txt
    if errorlevel 1 goto ERRO
)

set "PYTHON=.venv\Scripts\python.exe"

echo [2/4] A atualizar a estrutura da base de dados...
%PYTHON% manage.py migrate --noinput
if errorlevel 1 goto ERRO

echo [3/4] A carregar a base organizada de 3.081 anuncios...
%PYTHON% manage.py import_properties --clear
if errorlevel 1 goto ERRO

echo [4/4] A abrir o navegador...
start "" http://127.0.0.1:8000/

echo.
echo ==========================================
echo  IDEALHOME ABERTO
 echo  NAO FECHE ESTA JANELA
 echo ==========================================
echo.
%PYTHON% manage.py runserver 127.0.0.1:8000
goto FIM

:ERRO
echo.
echo ERRO AO PREPARAR O IDEALHOME.
echo Verifique se o Python esta instalado.
pause
exit /b 1

:FIM
endlocal
