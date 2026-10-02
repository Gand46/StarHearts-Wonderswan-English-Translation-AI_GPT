# I13-P1 — regresión F30 y traspaso a cierre

Fecha: 2026-09-27  
Resultado: `DONE_WITH_DEFERRED_QA`  
ROM activa: F30, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, checksum `9487`.

## Resultado demostrable

La matriz I13 contiene 20 casos: 14 pasan técnicamente y 6 requieren juego real antes del RC. La ejecución nueva de bajo costo arrancó F30 con un perfil Mesen limpio, mostró el título, seleccionó `New Game` mediante entrada natural y llegó a una escena jugable. No se usaron savestates ni escrituras RAM.

La comparación completa F26→F30 clasifica los 2.488 bytes distintos: todos caen en los descriptores/recursos de Magic y tienda autorizados, las tres etiquetas fijas de tienda o el checksum. Hay 0 cambios inesperados y los bancos físicos 0x19–0x21 son idénticos. Por ello la evidencia ya certificada de menús, combate, First Trial, Wampa, Village Rule y G12 se reutiliza sin repetir rutas equivalentes.

G12 conserva dos guardados naturales con hashes distintos y dos Cold Continue en procesos independientes. I13 no vuelve a ejecutarlos: el diferencial binario demuestra que F27–F30 no modificaron el ámbito de persistencia; repetirlos aumentaría el costo sin aportar una condición nueva.

## Deuda manual explícita

Se conserva la deuda I11 de tienda natural, Magic natural y Link Cable válido; la deuda I12 de ending y credits; y se agrega un único caso I13 para Holy Temple/Tirawaka/segundo First Trial. Son 6 casos manuales obligatorios. Ninguno impide el cierre técnico de I13, pero todos bloquean la autorización RC.

I13 queda cerrada técnicamente con QA diferida. I14 queda habilitada para preparar el cierre, reconstrucción y expediente pre-RC; no puede declararse RC hasta adjuntar y aprobar las seis evidencias reales.

## Eficiencia

- Métodos nuevos: comparación binaria exhaustiva y una ejecución limpia F30.
- Rutas largas repetidas: 0.
- Cold Continue repetidos: 0; se reutilizan los dos ya certificados.
- Cambio binario: no.
- Traducción o diseño pendiente detectado por esta regresión: ninguno nuevo.
- Ahorro exacto de tokens: `NOT_MEASURED`; no se inventa una cifra.
