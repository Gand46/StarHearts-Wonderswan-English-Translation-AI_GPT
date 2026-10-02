# I14-P7 — aceptación sintética / F32 sin cambios

La instrucción vigente del usuario permite cerrar evidencia sintética con la etiqueta **PASS_SYNTHETIC**. Se aplica a ejecución de consumidores nativos, capturas legibles y trazas con modificaciones declaradas. La procedencia natural y el enlace físico dejan de ser requisitos de aceptación de la traducción. No se atribuye ejecución a lo que nunca se observó.

| Caso | Resultado actual | Alcance aceptado o pendiente |
|---|---|---|
| Tienda | PASS_SYNTHETIC | Paneles compra/venta/reparación; venta y reparación completas controladas; encabezado Arms corregido en F31 y conservado en F32. No acredita compra completa ni todo el stock. |
| Fire/Magic | PASS_SYNTHETIC | Premio Fire nativo tras entrada sintética y menú poblado con descripción legible. |
| Holy Temple/Tirawaka/segundo First Trial | PASS_SYNTHETIC | Mapa, nombre/diálogo Tirawaka y banner del segundo First Trial por consumidores nativos controlados. No acredita recorrido tardío conectado. |
| Link wait/error | PENDING_SYNTHETIC_EVIDENCE | LINK ERROR legible; falta WAITING P2 legible. El handshake/transfer serial queda fuera del alcance solicitado. |
| Ending | PENDING_SYNTHETIC_EVIDENCE | No se identificó/ejecutó todavía el consumidor terminal. |
| Credits | PENDING_SYNTHETIC_EVIDENCE | No hay secuencia válida ni capturas primera/última del staff roll. |

**Tres casos aceptados; tres pendientes sintéticos; cero dependencias obligatorias de juego real. RC_NOT_AUTHORIZED** hasta demostrar los tres pendientes con este mismo criterio. Los identificadores históricos que incluyen NATURAL/REAL se conservan para trazabilidad, pero ya no fijan el criterio vigente.

## Corrección de evidencia Link

La revisión directa del PNG I04 `link_wait_f21_d30.png` contradice su aprobación visual antigua: el texto se mezcla con campo/diálogo y no acredita WAITING P2 legible. Se preserva el histórico y se revoca esa aprobación para el estado actual. Dos pruebas puntuales en F32: método 1 lee 0x370000 dos veces pero deja el título, método 2 no entra al consumidor. Ninguna pasa. La rama se detiene al llegar a dos métodos; no se diagnostica un defecto de ROM por un fixture fallido.

Falta inicializar el contexto visual de Link antes de A000:0778 y capturar el texto nativo con traza. No hace falta esperar un peer físico para este objetivo. Ending y credits requieren identificar consumidores distintos de las dos hipótesis 01DE ya descartadas; no repetirlas.

## Traducción y reutilización

Las 11 correcciones F31 y los 23 registros F32 pasan al ledger vigente CURRENT_TRANSLATION_ACCEPTANCE.csv como PASS_SYNTHETIC dentro de su alcance ya observado. Los siete paneles siguen siendo muestras representativas; no se amplía la aprobación a cada objeto/página/función. En esta etapa se modifica la aceptación, no el texto ni la ROM: cero traducciones nuevas y F32/BPS/fuentes idénticos.

CASE_EVIDENCE.json enlaza capturas y trazas con SHA-256. EVIDENCE_INHERITANCE.json documenta nueve rangos pertinentes idénticos F30/F31→F32, junto con las verificaciones previas P5/P6. Las capturas antiguas conservan su versión de origen; no se presentan como ejecuciones nuevas en F32. P4 Fire/Temple procede de acceso sintético; P3 Holy usa redirección de eventos; I11 tienda usa condiciones/búferes controlados. Estas modificaciones quedan aceptadas para el alcance sintético.

El estado previo completo se conserva en HISTORY_I14P6.json. Las afirmaciones naturales de informes anteriores quedan históricas. Las exclusiones funcionales constan en ACCEPTANCE_POLICY.json; no son nuevos bloqueos de la traducción.

## Eficiencia y plataforma

No se ejecutó BAT, ni cmd/Wine, ni se repitieron build/BPS/checksum, G12 o diferencial F26→F30. Se hicieron dos sondeos Link de 260 frames y comprobaciones documentales/bytes acotadas. El ahorro de tokens y duración total no se midieron. El validador del paquete verifica coherencia y hashes, no reemplaza una captura. Se reutiliza el PASS Linux Python de P6.
