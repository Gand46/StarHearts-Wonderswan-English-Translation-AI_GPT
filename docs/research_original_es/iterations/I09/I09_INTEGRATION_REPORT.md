# I09 — Integración F26 de Bank 0x1F–0x20

Fecha: 2026-09-26  
Estado: **DONE_WITH_DEFERRED_QA — integración cerrada; runtime/visual diferidos a I11**

## Resultado

Se integraron las 52 ocurrencias `0x0022` previstas: 37 de Bank `0x1F` y 15 de Bank `0x20`. Todas quedan `FINAL`; no hubo exclusiones, colisiones entre nombres ni japonés superviviente en los operandos.

El preflight físico determinó 37 variantes compactas y 15 formas I02 directas. Las decisiones completas están en `I09_RECORD_DECISIONS.csv`.

## Controles preservados

- Consumidor `9000:3564`, máximo ocho palabras CP932.
- 52/52 opcodes `0x0022` y delimitadores `21 00 00 00` intactos.
- Campos compañeros sin cambios conforme a I01.
- Longitud inline, simulación del consumidor y round-trip CP932: PASS en 52/52.
- Diferencias frente a F25: 409 bytes, limitados a operandos y checksum.
- Offsets inesperados: 0.

## Binario y parches

- F26 SHA-256: `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`.
- Checksum WonderSwan: `6ABA`.
- Reconstrucción desde ROM JP: idéntica byte a byte.
- BPS acumulativo JP → F26 e incremental F25 → F26: PASS independiente.
- `BUILD.bat` y `build.sh` apuntan al constructor acumulativo F26.

## Runtime y eficiencia

No se repitió Mesen sin una hipótesis nueva. Los 52 registros permanecen `NOT_VALIDATED_DEFERRED_I11_TOOL_BLOCKED`; no se declara PASS visual ni funcional.

I09 se cierra técnicamente y habilita I10. Esto no habilita RC.
