# I06 — Integración F23 de Bank 0x19–0x1A

Fecha: 2026-09-26  
Estado: **DONE_WITH_DEFERRED_QA — integración cerrada; runtime/visual diferidos a I11**

## Resultado

Se integraron las 45 ocurrencias `0x0022` previstas: 24 de Bank `0x19` y 21 de Bank `0x1A`. Todas quedan `FINAL`; no hubo exclusiones y no sobreviven caracteres japoneses en los operandos del lote.

El preflight físico mostró que 31 traducciones I02 excedían el tamaño inline original. Para evitar repaquetar scripts, se documentaron variantes de pantalla compactas en `I06_RECORD_DECISIONS.csv`. Las otras 14 usan directamente la forma I02. Todos los operandos se codificaron en CP932 fullwidth y se rellenaron con espacios fullwidth hasta conservar exactamente su longitud original.

## Controles preservados

- Consumidor probado: `9000:3564`, máximo ocho palabras CP932.
- Los 45 opcodes `0x0022` permanecen en su offset.
- Los 45 delimitadores `21 00 00 00` permanecen byte a byte.
- Los campos compañeros se conservaron sin cambios, conforme a la regla I01.
- Capacidad inline original: preservada en 45/45 registros.
- Simulación del consumidor y round-trip CP932: PASS en 45/45.
- Diferencias frente a F22: 371 bytes, limitados a los 45 operandos y el checksum.
- Offsets inesperados: 0.

## Binario y parches

- F23 SHA-256: `48238577e0e8ea736f4809621dc045369b4674a91fc06975c1f552b7cb958f28`.
- Checksum WonderSwan: `34B3`.
- Reconstrucción acumulativa desde ROM JP: idéntica byte a byte.
- BPS acumulativo JP → F23: PASS con herramienta independiente.
- BPS incremental F22 → F23: PASS con herramienta independiente.
- `BUILD.bat` y `build.sh` apuntan al constructor acumulativo F23.

## Runtime y eficiencia

No se repitió Mesen: en I05 abortó antes de emular con `std::bad_cast` tanto sobre F22 como sobre el control F21, y no existe una hipótesis nueva. Conforme a `EFICIENCIA_OPERATIVA_v1.1.md`, los 45 registros quedan `NOT_VALIDATED_DEFERRED_I11_TOOL_BLOCKED`; no se declara PASS visual ni funcional.

I06 se cierra técnicamente y habilita I07. Esto no habilita RC.
