# I11-P22 — cierre técnico con QA manual obligatoria transferida

Fecha: 2026-09-27  
ROM: F30, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, checksum `9487`  
Estado I11: `DONE_WITH_DEFERRED_QA`  
Cambio binario: ninguno

## Decisión de avance

I11 no se mantiene indefinidamente en navegación sin evidencia nueva. El proyecto ya agotó métodos distintos para las tres rutas naturales restantes y conserva pruebas controladas suficientes para separar traducción/integración de recorrido:

- tienda: consumidores, categorías, `BP/RP`, venta y reparación completa pasan; solo falta llegar naturalmente a un mercader;
- Magic: encabezado F27, `Fire`, descripción y adquisición nativa controlada pasan; solo falta la progresión natural a `007E`;
- Link Cable: selector, bandera fuente y textos se mapearon, pero falta un estado válido y un segundo participante o enlace compatible.

La regla de eficiencia del plan permite cerrar un lote como `DONE_WITH_DEFERRED_QA` cuando estructura, consumidor, build y parche pasan y solo queda acceso natural/visual completo. La deuda no se convierte en PASS: G09, G10 y G11 permanecen parciales, y los tres casos bloquean I14/RC hasta completarse.

## Por qué son pruebas especiales

Los savestates disponibles están en escenas `0000/0005`, no en `00DC/007E`. `00DC` es una región interior 1×1 sin condiciones y `007E` una región 4×4; sus productores naturales dependen de recorrido/progreso que no está contenido en los checkpoints certificados. Link añade una dependencia externa: estado natural de desbloqueo y un peer compatible. Más redirecciones o pokes repetirían evidencia controlada ya obtenida y no demostrarían acceso real.

`manual_playtest/MANUAL_PLAYTEST_REQUIRED.csv` fija para cada caso el objetivo, requisito y evidencia mínima. Una prueba manual futura puede cerrar las filas sin rehacer P17–P21.

## Efecto sobre el programa

- I11 queda técnicamente cerrada como `DONE_WITH_DEFERRED_QA`, no como PASS total.
- I12 queda habilitada para auditar late game, ending y credits.
- La matriz de superficies conserva 4 `PASS`, 2 `PARTIAL_OPEN` y 1 `OPEN` hasta recibir evidencia manual.
- No se permite RC ni afirmación de 100 % mientras alguno de los tres casos siga abierto.
- Quedan tres etapas activas del programa: I12, I13 e I14.

El ahorro exacto de tokens se conserva como `NOT_MEASURED`; la ganancia verificable es evitar nuevos ensayos equivalentes sin hipótesis distinta.
