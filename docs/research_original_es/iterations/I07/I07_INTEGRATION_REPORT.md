# I07 — Integración F24 de Bank 0x1B–0x1C

Fecha: 2026-09-26  
Estado: **DONE_WITH_DEFERRED_QA — integración cerrada; runtime/visual diferidos a I11**

## Resultado

Se integraron las 63 ocurrencias `0x0022` previstas: 31 de Bank `0x1B` y 32 de Bank `0x1C`. Todas quedan `FINAL`; no hubo exclusiones, colisiones de nombres ni caracteres japoneses supervivientes en los operandos del lote.

El preflight físico determinó que 47 ocurrencias requerían una variante compacta por capacidad inline; 16 admitían directamente la forma I02. Las decisiones se documentan en `I07_RECORD_DECISIONS.csv`. Todos los operandos usan CP932 fullwidth y conservan su longitud original mediante relleno fullwidth cuando corresponde.

## Controles preservados

- Consumidor probado: `9000:3564`, máximo ocho palabras CP932.
- Los 63 opcodes `0x0022` permanecen en su offset.
- Los 63 delimitadores `21 00 00 00` permanecen byte a byte.
- Los campos compañeros se conservaron sin cambios conforme a I01.
- Capacidad inline, simulación del consumidor y round-trip CP932: PASS en 63/63.
- Diferencias frente a F23: 563 bytes, limitados a operandos y checksum.
- Offsets inesperados: 0.

## Binario y parches

- F24 SHA-256: `3db95bd8c4935d262939acd253ea9428bf9131c0e3af35b0b858ea383cd0ea80`.
- Checksum WonderSwan: `4E47`.
- Reconstrucción acumulativa desde ROM JP: idéntica byte a byte.
- BPS acumulativo JP → F24: PASS con herramienta independiente.
- BPS incremental F23 → F24: PASS con herramienta independiente.
- `BUILD.bat` y `build.sh` apuntan al constructor acumulativo F24.

## Runtime y eficiencia

No se repitió Mesen porque el bloqueo `std::bad_cast` no tiene hipótesis o corrección nueva. Los 63 registros permanecen `NOT_VALIDATED_DEFERRED_I11_TOOL_BLOCKED`; no se declara PASS visual ni funcional.

I07 se cierra técnicamente y habilita I08. Esto no habilita RC.
