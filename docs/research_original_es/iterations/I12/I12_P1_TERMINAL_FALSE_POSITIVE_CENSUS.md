# I12-P1 — depuración de falsos positivos de ending y credits

Fecha: 2026-09-27  
ROM: F30, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, checksum `9487`  
Estado I12: `IN_PROGRESS`  
Cambio binario: ninguno

## Resultado

Los cuatro términos que la línea base había aislado como “credit-like” no forman un corpus de créditos:

| Término | Offset | Registro contenedor | Clasificación |
| --- | --- | --- | --- |
| `プログラム` | `0x382820` | `虫ロボットのプログラムができそう` | descripción de objeto |
| `開発` | `0x384095` | `開発用セーブのタイコだ！` | descripción del Save Drum de desarrollo |
| `エンディング` | `0x38432F` | `エンディング` | título BGM |
| `スタッフ` | `0x38433D` | `スタッフロール` | título BGM |

Los dos últimos registros están dentro de la secuencia de nombres musicales `平和な世界`, `エンディング`, `スタッフロール`, `冒険の始まり`, `ゲームイズオーバー`, `イベント発生`. Esto prueba contexto de BGM, no texto mostrado durante ending o staff roll.

## Método reproducible

`scripts/i12_p1_terminal_candidate_census.py` exige el SHA-256 F30, localiza cada término CP932 una sola vez, reconstruye su registro contenedor y cruza su offset contra las cinco tablas activas conocidas de Bank 38: objetos/descripciones, nombres Magic, descripciones Magic, nombres de entidad y nombres de mapa. Los cuatro obtienen cero referencias desde esas tablas.

La evidencia pública está en `runtime/terminal_census/terminal_candidate_census.json` y `terminal_candidate_contexts.csv`.

## Límite y siguiente tarea

Esta clasificación elimina cuatro falsos positivos; no identifica todavía el consumidor real del final ni los créditos, que podrían estar en scripts tardíos, gráficos o recursos comprimidos. `G13_ENDING` y `G14_CREDITS` permanecen `OPEN`, y una reproducción final real continúa siendo obligatoria antes de RC.

La siguiente búsqueda I12 debe partir de productores de transición terminal, rutinas de vídeo/scroll o recursos gráficos, no de estos cuatro términos. No se declara porcentaje ni cierre global. Ahorro exacto de tokens: `NOT_MEASURED`.
