# I08 — Integración F25 de Bank 0x1D–0x1E

Fecha: 2026-09-26  
Estado: **DONE_WITH_DEFERRED_QA — integración cerrada; runtime/visual diferidos a I11**

## Resultado

Se integraron las 54 ocurrencias `0x0022` previstas: 32 de Bank `0x1D` y 22 de Bank `0x1E`. Todas quedan `FINAL`; no hubo exclusiones, colisiones ni japonés superviviente en los operandos.

El preflight físico determinó 44 variantes compactas y 10 formas I02 directas. Se evitó la colisión potencial entre Childe y Chicory mediante `Chd` y `Chc`. Las decisiones completas están en `I08_RECORD_DECISIONS.csv`.

## Controles preservados

- Consumidor `9000:3564`, máximo ocho palabras CP932.
- 54/54 opcodes `0x0022` y delimitadores `21 00 00 00` intactos.
- Campos compañeros sin cambios conforme a I01.
- Longitud inline, simulación del consumidor y round-trip CP932: PASS en 54/54.
- Diferencias frente a F24: 442 bytes, limitados a operandos y checksum.
- Offsets inesperados: 0.

## Binario y parches

- F25 SHA-256: `b9fef4f219daf66575f5c2e7c7666dff868f0013732ec8d5f75be4ba9e3d3dc1`.
- Checksum WonderSwan: `5EA1`.
- Reconstrucción desde ROM JP: idéntica byte a byte.
- BPS acumulativo JP → F25 e incremental F24 → F25: PASS independiente.
- `BUILD.bat` y `build.sh` apuntan al constructor acumulativo F25.

## Runtime y eficiencia

No se repitió Mesen sin una hipótesis nueva. Los 54 registros permanecen `NOT_VALIDATED_DEFERRED_I11_TOOL_BLOCKED`; no se declara PASS visual ni funcional.

I08 se cierra técnicamente y habilita I09. Esto no habilita RC.
