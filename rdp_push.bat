@echo off
chcp 65001 > nul
cd /d "E:\ЕГ\принтер\keys GitHub"

echo === ПОДГОТОВКА СЕРТИФИКАТОВ ===
git config --global http.sslBackend schannel

echo === ОТПРАВКА НА GITHUB ===
:: Добавляем ВСЕ новые и измененные файлы
git add .
git commit -m "Auto-update: %date% %time%"

:: Пробуем отправить
git push origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ Ошибка при отправке! Проверьте интернет или SSL-настройки.
) else (
    echo.
    echo ✅ Все улетело на GitHub!
)
pause