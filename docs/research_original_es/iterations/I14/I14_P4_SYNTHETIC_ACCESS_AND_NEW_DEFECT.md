# I14-P4 — acceso sintético reproducible y defecto nuevo

2026-09-28 · Paquete 1.35 · `RC_NOT_AUTHORIZED`

## Resultado

Se desensambló el cargador de mapas y se construyeron tres ROMs experimentales mediante BPS directo JP→F30+hook. El parche carga el mapa completo, sus actores y colisiones; después se interactúa con entradas de mando. No es una decompilación completa ni una ruta natural. F30 y su BPS oficial permanecen intactos.

| Superficie | Evidencia nueva | Límite |
|---|---|---|
| Reparación | Interior estable, mercader y panel nativo; reproducción en F30 original | Entrada sintética; no nueva transacción completa |
| Fire/Magic | Diálogo de Ifrit, `Fire Obtained!`, flags asignados por el juego y Magic con `Fire`/`Shoots fireball.`/`Equip?` | Procedencia sintética del mapa; no aprendizaje por recorrido natural |
| Holy Temple | Mapa 000A/celda 3 cargado y visible | No se activó Tirawaka ni el segundo First Trial; no confundir esta celda con el encuentro tardío |
| Ending/credits | Sin evidencia nueva; se preserva descarte de 01DE | Falta consumidor terminal identificado o checkpoint prefinal válido |
| Link | No se modificó la bandera ni se repitió un intento sin transporte | Continúa exigiendo hardware o peer soportado |

Siguen 0 `AUTOMATED_NATURAL_PASS`, cinco `EXTERNAL_PLAYTEST_REQUIRED` y un `EXTERNAL_HARDWARE_OR_SUPPORTED_PEER_REQUIRED`. El acceso sintético no satisface los seis gates originales.

## Hallazgo que reabre trabajo técnico

`DEFECT-I14P4-01`, severidad HIGH: el encabezado del menú de reparación muestra **武器** (armas). Se reprodujo con F30 SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, desde el checkpoint sintético de entrada y usando solo mando; el hook ya no está en la ROM utilizada para esta comprobación. Captura: `runtime/p4/evidence/repair_f30/final.png`.

La revisión P21 aprobó coste/durabilidad y `Repair?`/`RP`, pero omitió este encabezado. No se modifica retrospectivamente su traza funcional; se revoca cualquier lectura de aquella revisión como aprobación de toda la pantalla. G15 pasa a FAIL y G10 registra el defecto. Hay 0 críticos y 1 alto abierto. La corrección del recurso gráfico y su integración quedan pendientes; no se cambió F30 de forma especulativa. El censo I10 de 237 operandos mantiene su alcance histórico, no cubre este recurso gráfico.

## Ingeniería y procedencia

La ROM F30 se recuperó aplicando el BPS autorizado a la JP del handoff del usuario, no repitiendo el build cerrado. Checkpoint origen: `StarHearts_WORK_HANDOFF_F19_CORE_DEPURADO_2026-09-25/project/evidence/checkpoints/F18_grass_cut_probe_NAV_ONLY.mss`, SHA-256 `6ffd42a48e6111eb31befcb85ee9c7c11b233870e95ae4c901f0abd0f97eb5bc`. Su procedencia natural se reutiliza del expediente; **sus descendientes tras el hook son sintéticos**.

Desensamblado dirigido con wsdisasm 1.1.0 y comprobación de ejecución:

- Hook físico `395CA0`, sustitución del CALL nativo `AF30` por CALL `FF00`; retorno preserva el CALL original.
- Cueva `39FF00–39FF34`, verificada como FF antes de escribir; PUSHF/PUSHA y POPA/POPF.
- Condición de entrada: región `CAD3=0000` y celda `CAD5=000F`. No es un selector de menú; al volver a esa celda se dispara otra vez.
- Parámetros nativos: `CAF5` región, `CAF7` celda, `CAF9/CAFA` posición en tiles. El loader convierte a las coordenadas de jugador.
- Cadena: `A000:B9EE` (reinicio vídeo/cache), `9000:6052` (carga), `9000:66EE` (redibujado). La traza confirma `96052` y `96338`.
- Cada variante cambia exactamente 57 bytes respecto de F30: dos del CALL, 53 de código y dos del checksum. No altera texto, scripts de eventos, tablas de objetos ni el código de adquisición de Fire.
- El hook sí causa cambios de WRAM y de estado de juego. No equivale a «sin pokes» o acceso natural; solo las continuaciones sobre F30 usan mando sin escrituras externas.

Fire se entrega en la continuación F30 por `9000:3330`, frame 1586. Los bytes de flags observados pasan de `00/00` a `80/C0` entre frames 1560 y 1680. No se escriben esos bytes desde Lua. Magic ejecuta `A000:46E0` en frame 1021 y `A000:48C8` en 1026 de su continuación. La repetición dirigida produjo capturas SHA-256 idénticas para adquisición, Magic y reparación.

## Intentos descartados y límite

El método de acceso asistido durante runtime se probó con un cambio de región en el resolvedor y con una llamada PC/pila al cargador: no produjo un acceso estable que se aceptase. El segundo método fue el hook de ROM al cargador completo. Dentro de este método, la primera versión conservaba fondos corruptos y la segunda necesitó el redibujado nativo; ambas se descartan. La versión entregada muestra fondo y actores coherentes. No se repiten como nuevas rutas.

No se realizó una búsqueda exhaustiva de flags del templo ni de las escenas terminales: faltan condiciones narrativas y consumidor concreto. El siguiente intento debe aportar ese dato, no volver a inyectar los mismos diálogos P3. El supuesto ahorro exacto de tokens es `NOT_MEASURED`; se conservaron scripts cortos, trazas dirigidas y capturas seleccionadas. No se ejecutaron G12, el diferencial F26→F30 ni los builds técnicos cerrados. No hay cmd/Wine en este host; BUILD.bat no se ejecutó.

## Próxima acción mínima

1. Corregir `DEFECT-I14P4-01`: rastrear el recurso del encabezado de `A000:9C50/A000:A894`, traducirlo y validar exclusivamente esa superficie y los consumidores compartidos. Existe reproducción estable, por lo que ya no hace falta un playtest externo para investigar este defecto.
2. Reutilizar el hook para exploración de regiones con condiciones conocidas; la rama Holy necesita identificar el encuentro tardío y sus flags. Ending/credits necesitan consumidor terminal o checkpoint prefinal, no la escena máxima 01DE.
3. Para cerrar los gates naturales, repetir los hitos desde saves de ruta documentada sin hook ni estados sintéticos. Link exige además transporte serial real o soportado. Windows smoke exige cmd o Wine funcional.

Ver `runtime/p4/REPRODUCE.md`, `I14_P4_RESULTS.json`, `PROVENANCE.json`, `PATCH_VALIDATION.json` y `P4_EVIDENCE_SHA256SUMS.txt`. El paquete público contiene fuentes, BPS y evidencia; no ROM, SRAM ni savestates. Los checkpoints sintéticos se regeneran desde el checkpoint privado del handoff.
