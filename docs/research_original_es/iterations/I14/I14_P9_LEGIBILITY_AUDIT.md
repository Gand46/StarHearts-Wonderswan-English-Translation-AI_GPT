# I14-P9 — revisión de legibilidad y corrección de falsas aprobaciones

La objeción del usuario es correcta: la captura WAITING P2 entregada en P8 **no cumple QG-35**. Su PASS se revoca. La aceptación de acceso sintético nunca dispensó fuente, integridad de glifos, legibilidad ni lectura de píxeles reales.

| Hallazgo | Causa demostrada | Resultado actual |
|---|---|---|
| WAITING P2, frame 600 | Fotograma de desplazamiento: los 3.584 píxeles de la franja son exactamente el promedio de los frames 599 y 601. Los trazos duplicados no son la forma del glifo. Algunas capturas anteriores también dejan P2 fuera de pantalla. | Captura rechazada y reemplazada por frame 720 completo y estable. Fuente y ROM del rótulo sin cambios. |
| Segundo banner de First Trial | El token F04C contiene «en» minúscula; F11 lo documentaba erróneamente como «EN». La salida era EVenT. Reintroducir F079 para ahorrar bytes volvió a omitir «ir» en este consumidor especial. | F34 usa EVENT:First Trial, con EVENT e i/r explícitos y el mismo slot de 28 bytes. Se elimina solo el espacio posterior a los dos puntos; su margen nativo separa visualmente las palabras. |
| LINK ERROR | El texto traducido movió el campo numérico de +12 a +24 bytes. El formateador seguía escribiendo en +12: LINK E123R y placeholders FE visibles como basura. | F34 ajusta el destino F3B2→F3BE. Lectura real: LINK ERROR y códigos 123/999 en la segunda línea. |

Los dos últimos eran errores reales de integración/representación, no una fuente nueva. Se corrigen en la misma iteración. Se conservaron las capturas anteriores como evidencia de fallo y se sustituyeron sus referencias en el ledger activo. `SUPERSEDED_APPROVALS.json` identifica explícitamente las aprobaciones revocadas; los históricos no vuelven a aprobarlas.

## Fuente y reconocimiento

WAITING se revisó a escala nativa y mediante celdas aisladas aleatorizadas, etiquetadas solo con números. Se transcribieron los nueve glifos antes de leer la clave: todos se reconocieron y sus máscaras blancas coinciden exactamente con la referencia nativa del juego. Las dos I son iguales. No se usó OCR. Este control oculta orden y palabra; no se presenta como un estudio con un revisor independiente que desconociera el mensaje.

Se compararon 94 glifos latinos/símbolos imprimibles CP932 contra JP: 93 son idénticos. El guion bajo «_» tiene dos bytes modificados desde una revisión histórica; no se observó en las capturas revisadas y no aparece como 8151 literal en bancos de guion 19–21. Esto **no demuestra que nunca se utilice**: su procedencia/uso visible queda NOT_VALIDATED, no PASS ni defecto runtime probado. F34 no modifica ningún glifo, diccionario, paleta ni renderizador compartido.

El prototipo de cambiar colores de la franja Link fue descartado al comprobar que no resolvía la causa de la evidencia. No forma parte del BPS final.

## Alcance de la revisión

Se revisaron 28 capturas de referencia de interfaz: encabezados, reparación/estadísticas, los siete paneles nativos de P6, e-Pet con datos y vacío, tienda, Fire/Magic, Link, Holy/Tirawaka y el segundo banner. Las capturas antiguas de encabezado solo validan su encabezado; sus datos de prueba no se aprueban como funcionamiento de todo el panel.

En Tirawaka, f0600 solo respalda el nombre completo: el resto de ese primer mensaje aún se estaba escribiendo. Se añade f0720 como fragmento del mensaje de prueba posterior; no se aprueba todo el diálogo por inferencia.

Se retienen las 29 páginas de epílogo y 45 tarjetas de créditos P8, inspeccionadas directamente y conservadas por igualdad de guion, recursos y consumidores pertinentes. La modificación del número Link es local a su manejador y la del banner local a su string. No se encontró otro glifo malformado confirmado en el alcance revisado. Esta conclusión no certifica todas las traducciones, nombres, estados ni escenas del juego.

`VISUAL_SAMPLE_AUDIT.csv`, `LATIN_FONT_CENSUS.json`, `WAITING_GLYPH_AUDIT.json`, `MOTION_CAPTURE_ANALYSIS.json` y `COVERAGE.json` detallan denominadores y límites. Las máscaras e imágenes proceden de capturas reales; los recortes/ampliaciones diagnósticos no sustituyen la vista nativa.

## Entrega y criterio vigente

F34: solo 8 bytes diferentes de F33; checksum 3CD5. Build completo Python/Linux desde JP y aplicación independiente del BPS directo: PASS. Se incluyen fuentes acumulativas, hashes, trazas y las evidencias antes/después. No se repitieron G12 ni F26→F30; no se ejecutó BAT/cmd/Wine. Ahorro de tokens: no medido.

Los seis casos continúan **PASS_SYNTHETIC únicamente con las evidencias corregidas**. Estado **RC_SYNTHETIC_FOR_TESTING**; no se autoriza publicación general ni se certifica legibilidad global. No se inventa una prueba natural ni comunicación Link real. La procedencia del guion bajo histórico sigue clasificada explícitamente como no validada.
