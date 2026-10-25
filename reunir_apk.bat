@echo off
echo Reunindo partes do APK Cordeiro Play...
copy /b app-debug.apk.part_* app-debug.apk
echo Concluido com sucesso! O arquivo app-debug.apk foi gerado e esta pronto para instalar.
pause
