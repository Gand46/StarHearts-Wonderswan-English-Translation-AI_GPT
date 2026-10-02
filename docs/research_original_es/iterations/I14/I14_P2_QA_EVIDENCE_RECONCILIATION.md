# I14-P2 — reconciliación de evidencia real F30

Fecha: 2026-09-27  
Autoridad de entrada: `StarHearts_Proyecto_Auditoria_Iterativa_v1.32_I14P1_PreRC_TechnicalPass_2026-09-27.zip`  
SHA-256 de la autoridad: `7e5264643d85291c36a4ba36b7ce5cd3963a5a7352ba4fe2052091751879d1de`  
Resultado: `QA_EVIDENCE_ATTEMPT_COMPLETE_EXTERNAL_VALIDATION_REQUIRED`  
Decisión: `RC_NOT_AUTHORIZED`

## Resultado ejecutivo

La ejecución acotada intentó las seis pruebas reales sin repetir G12, el diferencial F26→F30 ni las validaciones técnicas cerradas. No apareció una evidencia que cumpla el estándar de PASS natural. F30 no se modificó y no se confirmó ningún defecto nuevo de traducción, tipografía, diseño o funcionamiento.

| Caso | Clasificación | Evidencia observada | Requisito mínimo pendiente |
|---|---|---|---|
| Tienda natural | `EXTERNAL_PLAYTEST_REQUIRED` | Se alcanzó un interior de tipi desde progreso documentado, pero no el panel de mercader ni una transacción. | Ruta natural al mercader y antes/después de dinero e inventario. |
| Fire y Magic poblada | `EXTERNAL_PLAYTEST_REQUIRED` | No se observó el premio Fire ni la escena `007E` con Magic poblada. | Adquirir Fire mediante un evento real y abrir Magic en la misma progresión. |
| Link Cable válido | `EXTERNAL_HARDWARE_OR_SUPPORTED_PEER_REQUIRED` | Dos Mesen 2.1.1 aislados no habilitaron Link; la ruta serial inspeccionada no expuso transporte entre peers. | Transporte WonderSwan real soportado y guardados con Link desbloqueado naturalmente. |
| Holy Temple/Tirawaka/segundo First Trial | `EXTERNAL_PLAYTEST_REQUIRED` | Se recapturó el primer First Trial y se continuó desde hierba documentada; no se alcanzó el pasaje, templo, Tirawaka, warp o segundo banner. | Recorrido natural continuo de la cadena completa. |
| Ending | `EXTERNAL_PLAYTEST_REQUIRED` | La ejecución continua desde el checkpoint natural más avanzado permaneció antes de Holy Temple. | Save natural prefinal con procedencia y entrada continua al ending. |
| Credits | `EXTERNAL_PLAYTEST_REQUIRED` | No se alcanzó ending y, por tanto, tampoco su transición a credits. | Continuar la misma ejecución aceptada de ending hasta terminar el staff roll. |

Conteo derivado: 0 `AUTOMATED_NATURAL_PASS`, 5 `EXTERNAL_PLAYTEST_REQUIRED` y 1 `EXTERNAL_HARDWARE_OR_SUPPORTED_PEER_REQUIRED`. Los seis casos continúan en `NOT_VALIDATED` y bloquean RC.

## Identidad preservada

- ROM F30: `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`; checksum WonderSwan `9487`.
- BPS acumulativo JP→F30: `61966d6adacf0fe4d9c97938be9809df2a5b3ab3313dad6036a732868e998baf`.
- Árbol `F30_SOURCE`: 133 archivos, hash de árbol `b4c4dd24e3a6f5a16b4ca57de84b86efaed6ee010da45aede3cc59b8d04a331c`.
- El build/BPS/checksum PASS de I14-P1 se reutiliza como evidencia histórica; no se reconstruyó ni repitió.
- No se distribuyen ROM, SRAM, EEPROM, savestates, BIOS ni emuladores.

## Ramas ejecutadas

### Tienda, Magic y Holy Temple

Se usaron dos métodos: una ruta fría F30 por entrada de mando durante 11.700 cuadros, y continuación por mandos Lua desde checkpoints de origen natural documentado. El segundo método se dividió en nueve segmentos de reanudación para preservar trazabilidad; no son nueve métodos. Todas las ejecuciones útiles terminaron con código 0. Los scripts usan entrada, lectura, captura y carga/guardado de checkpoint; no escriben WRAM/SRAM, no fuerzan eventos, no teletransportan y no editan F30.

La ruta fría prueba que el arnés puede reproducir juego natural y recaptura el **primer** First Trial; no lo presenta como el segundo. Las continuaciones no hallaron tienda, Fire/Magic o Holy Temple. Al agotarse las variantes equivalentes, la rama se detuvo y registró la acción externa mínima.

### Link Cable

Se ejecutaron dos instancias simultáneas con perfiles separados y copias de un guardado natural documentado. En ambas, `F44E=07`; el selector quedó en New Game y no apareció sesión Link. No se forzó `F44E`, `F44F`, SRAM ni una respuesta peer.

El segundo método fue una auditoría pasiva de la API y del núcleo exacto de Mesen 2.1.1. Se observaron registros/buffers seriales locales, pero no un transporte entre instancias. Esto solo caracteriza el binario inspeccionado y no todos los emuladores. La rama se reabre únicamente con hardware real o una implementación WonderSwan peer documentada, más un guardado desbloqueado por progresión natural.

### Ending y credits

La ejecución concluyente cargó una sola vez el checkpoint natural F18 más avanzado y aplicó 1.319 entradas a lo largo de 1.320 cuadros continuos. No hubo pokes, redirecciones ni recargas. La captura terminó en el exterior pre-Holy; por ello no existe una secuencia ending→credits válida. El video incluido muestra continuidad de la tentativa, no un PASS terminal.

### Smoke Windows

Se comprobaron dos vías de disponibilidad: resolución por `PATH` y rutas estándar de cmd/Wine/WSL. El host Linux no expuso `cmd`, Wine ni equivalente. `BUILD.bat` no se ejecutó y no se usó Python/Linux como sustituto. Resultado: `NOT_VALIDATED_BLOCKED_PLATFORM`; no bloquea RC por sí solo, pero sí la publicación pública.

## Antibloqueo y alcance

Cada rama quedó limitada a dos métodos distintos. Las secuencias adicionales dentro de un método son segmentos de un mismo replay documentado, no rutas técnicas nuevas. No se repitieron G12, el diferencial F26→F30, el build P1, la venta/reparación controladas ni los pokes de Link históricos. El ahorro exacto de tokens permanece `NOT_MEASURED`.

La tarea de intento está completa; la evidencia de aprobación no. No se abre F31 ni una nueva fase binaria. Cualquier cambio futuro a F30 exige primero un defecto reproducible y evidencia visible/funcional suficiente.

## Decisión

`RC_NOT_AUTHORIZED`. La autorización solo puede cambiar cuando las seis filas del ledger maestro tengan evidencia aceptada y los gates G09, G10, G11, G13 y G14 pasen. La publicación requiere además el smoke nativo Windows.

Los archivos mínimos, sus funciones y hashes están inventariados en `runtime/p2/EVIDENCE_INDEX.md`; los resultados legibles por máquina están en `runtime/p2/I14_P2_BRANCH_RESULTS.json`.
