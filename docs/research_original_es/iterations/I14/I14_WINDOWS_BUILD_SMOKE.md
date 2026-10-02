> HISTÓRICO: fuera del alcance desde I14-P6 por instrucción del usuario: no intentar BAT y usar el entorno GPT compatible. Esta guía F31 no certifica F32 ni constituye un bloqueo del build Linux solicitado.

# I14-P5 — smoke nativo de `BUILD.bat` para F31

Esta confirmación no puede ejecutarse en el entorno Linux actual porque no dispone de Windows `cmd` ni Wine. El wrapper fue validado estructuralmente y delega los mismos argumentos al núcleo Python que ya reconstruyó F31 byte a byte.

En Windows, con Python 3 disponible, colocar la ROM japonesa junto a una copia de `iterations/I14/F31_SOURCE/` y ejecutar:

```bat
BUILD.bat "Star_Hearts_JP_ORIGINAL_REFERENCE.wsc" -o "StarHearts_EN_phase13BG_F31_windows.wsc"
certutil -hashfile "StarHearts_EN_phase13BG_F31_windows.wsc" SHA256
```

Resultado requerido:

- tamaño: `4194304` bytes;
- SHA-256: `fbf949271412eb023cb94765782126a689eead61e8c6a56b2a12b85ed23acd52`;
- checksum WonderSwan almacenado/recalculado: `4EA7`.

Este smoke es recomendable antes de publicación pública para confirmar el host Windows. No cambia el binario ni sustituye las seis pruebas de juego real que bloquean el RC.
