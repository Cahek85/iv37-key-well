@echo off
:: Устанавливаем кодировку UTF-8
chcp 65001 > nul

:: Указываем прямой путь к вашему Python
set "PY_BIN=C:\Windows\py.exe"
set "WORK_DIR=E:\ЕГ\принтер\keys GitHub"

cd /d "%WORK_DIR%"

echo === СБОР КЛЮЧЕЙ НА RDP ===
echo Использую Python по пути: %PY_BIN%

:: Запуск скрипта
%PY_BIN% fetch_and_dedup.py

echo.
echo ✅ Сбор завершен. Проверьте файл configs.txt.
echo Теперь можно запускать тест на локальной машине через диск Z:.
echo.
timeout /t 15