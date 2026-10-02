# I14-P1 — cierre técnico pre‑RC

Fecha: 2026-09-27  
Estado: `PRE_RC_TECHNICAL_PASS_MANUAL_QA_BLOCKED`  
RC: `NOT_AUTHORIZED`

## Resultado

La fuente acumulativa F30 fue copiada a un directorio temporal limpio y reconstruida mediante `build.sh`. El núcleo Python que usa también `BUILD.bat` se ejecutó por separado. El BPS acumulativo se aplicó directamente sobre la ROM japonesa. Las tres salidas son byte a byte idénticas y producen SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, tamaño 4 MiB y checksum WonderSwan `9487`.

El árbol `F30_SOURCE` contiene 133 archivos, 0 ROM/SRAM/savestates y 35 fuentes Python que compilan. El BPS distribuible conserva SHA-256 `61966d6adacf0fe4d9c97938be9809df2a5b3ab3313dad6036a732868e998baf`. Las reglas universales y el protocolo de eficiencia adjuntos coinciden byte a byte con las copias del proyecto.

`BUILD.bat` y `build.sh` delegan al mismo constructor acumulativo y reenvían todos los argumentos. El wrapper POSIX se ejecutó realmente; el wrapper Windows se validó estructuralmente y su núcleo fue ejecutado, pero no se afirma una ejecución nativa con `cmd` porque este entorno no ofrece Windows/Wine. Se adjunta una prueba de un solo comando para realizarla sin repetir toda la auditoría.

## Estado de cierre

No quedan iteraciones técnicas reproducibles por GPT: `technical_iterations_remaining = 0`. I14 permanece activa exclusivamente como compuerta de aprobación. Hay 0 defectos críticos y 0 altos confirmados; quedan seis deudas de evidencia real —tienda, Magic, Link, Holy Temple, ending y credits— que bloquean RC. El smoke nativo de Windows es además obligatorio antes de una publicación pública, pero no crea una nueva fase binaria.

No se genera un parche “pre‑RC” duplicado: el BPS F30 ya es directo JP→F30, está hashado y reproduce exactamente el candidato técnico. Cambiarle el nombre sin cambiar bytes solo aumentaría el paquete y la confusión.

## Eficiencia

- Rutas de juego repetidas: 0.
- Cambios binarios: 0.
- Métodos nuevos: build limpio, ejecución independiente del núcleo, roundtrip BPS y auditoría de wrappers/fuentes.
- Artefactos binarios duplicados: 0.
- Ahorro exacto de tokens: `NOT_MEASURED`.
