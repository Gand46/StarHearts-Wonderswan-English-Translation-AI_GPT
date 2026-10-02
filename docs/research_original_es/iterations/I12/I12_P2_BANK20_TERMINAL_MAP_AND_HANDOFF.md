# I12-P2 — mapa terminal Bank 20 y traspaso de QA real

Fecha: 2026-09-27  
ROM activa: F30 (`17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`)  
Resultado técnico I12: `DONE_WITH_DEFERRED_QA`  
Cambio binario: no

## Resultado demostrable

La sonda reproducible `scripts/i12_p2_bank20_terminal_map.py` recorre la tabla completa del último banco normal de escenas:

- 30 escenas globales, `01C1–01DE`;
- 515 filas de evento y 515 inicios de script distintos;
- 515/515 scripts con terminador `1FFF` dentro de su límite;
- último script referenciado en `0x20A43C`, con terminador en `0x20A4A4`;
- desde `0x20A4AE` hasta el fin de Bank `0x20` hay 23.378 bytes `FF`.

La escena de índice más alto, `01DE`, contiene dos scripts normales. El primero incluye una concesión nativa única del objeto `0189` en `0x20A3E0`; esto la conserva como candidata terminal de mapa, pero no demuestra que sea el consumidor del ending o de los créditos. Bank `0x20` no contiene las cadenas CP932 `エンディング` ni `スタッフロール`.

P1 ya probó que los cuatro indicios históricos eran descripciones de objeto o títulos BGM. P2 descarta además que exista un bloque de créditos como cola no referenciada del banco normal de scripts. Los créditos pueden pertenecer a una ruta terminal fuera de estas tablas, a gráficos o a recursos comprimidos.

## Límite de la evidencia

No se declara `PASS` visual para `G13_ENDING` ni `G14_CREDITS`. Identificar su consumidor real exige observar la transición terminal durante una partida avanzada; los checkpoints disponibles no alcanzan ese estado y otro desvío sintético no demostraría la ruta real.

Los dos casos de `manual_playtest/MANUAL_PLAYTEST_REQUIRED.csv` son obligatorios antes del RC. Exigen una partida válida, continuidad desde el final hasta el staff roll y capturas completas. Esta deuda bloquea I14/RC, no la regresión técnica I13.

## Decisión de etapa

I12 queda cerrada técnicamente como `DONE_WITH_DEFERRED_QA`: el universo normal de scripts tardíos está acotado, los falsos positivos se eliminaron y la única evidencia que falta requiere juego real. I13 queda habilitada. F30, checksum y BPS no cambian.

Evidencia:

- `runtime/bank20_terminal_map/bank20_scene_map.csv`;
- `runtime/bank20_terminal_map/bank20_terminal_map.json`;
- `scripts/i12_p2_bank20_terminal_map.py`;
- `manual_playtest/MANUAL_PLAYTEST_REQUIRED.csv`.

Ahorro exacto de tokens: `NOT_MEASURED`.
