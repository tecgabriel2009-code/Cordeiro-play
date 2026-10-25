#!/bin/sh
echo "Reunindo partes do APK Cordeiro Play..."
cat app-debug.apk.part_* > app-debug.apk
chmod +x app-debug.apk
echo "Concluido com sucesso! O arquivo app-debug.apk foi gerado e esta pronto para instalar."
