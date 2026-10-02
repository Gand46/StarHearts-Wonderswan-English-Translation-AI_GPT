# I11-P8 — rutas nativas de tienda y Magic

**Rectificaciones I11-P9/P10:** `C008=2` proviene de la opción 3 del título (Link Cable), no de tienda. P9 atribuyó erróneamente `C0F2&0040` y `CA80` a tienda: organizan el menú principal. `0230` habilita Magic junto con `0070`; `0252` pertenece a otro grupo del menú. P10 confirmó `A000:48C8` como consumidor Magic. Las lecturas y pantallas registradas abajo permanecen como observaciones controladas, sin aprobar ninguna de las dos superficies. Véanse `I11_P9_ROUTE_CORRECTION.md` e `I11_P10_MAGIC_ROUTE_AND_HEADER.md`.

Fecha: 2026-09-26. ROM F26 SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`; checksum `6ABA`; sin cambio binario. Lote de dos superficies y métodos diferenciados, con guardado natural certificado como origen de las pruebas controladas.

## Tienda

El desensamblado localiza en Bank `0x39`, dirección física `0x395BB0`, el despacho por palabra WRAM `C008`. El valor `0002` llama la rutina `A000:0120` (físico `0x3A0120`), reclasificada en P9 como rama del modo Link Cable. El Continue frío del guardado certificado alcanza ese despacho en el cuadro 190 con `C008=0000`. Escribir `0002` precisamente en ese punto produjo 36 lecturas de `OWNED`, 34 de `BUYPRICE` y 29 de `REPAIR` antes del cuadro 610, pero no atribuye esas lecturas a una compra. La imagen resultante es roja, sin panel válido. Escribir `C008` después de entrar al campo no alteró la escena.

Evidencia histórica reducida: `runtime/shop_dispatch/baseline_dispatch.txt`, `controlled_dispatch.txt` e `invalid_controlled_render.png`. Scripts: `runtime/scripts/i11_p8_shop_dispatch_trace.lua` y `i11_p8_native_shop_mode_probe.lua` (nombres heredados de la hipótesis corregida). Esto demuestra lecturas bajo control en la rama Link, sin aprobar la tienda. La superficie continúa `OPEN`.

## Magic

El comprobador genérico `9000:3BD0` (físico `0x393BD0`) toma un identificador, desplaza tres bits y prueba la máscara rotada en el bitset de SRAM con puntero `1000:0022`. Se ensayaron `0230` en SRAM `0068` y luego `0252` en SRAM `006C`, máscara `20`. El segundo bit fue leído dos veces, pero Magic todavía mostró `None`. P10 determinó que faltaba además `0070` (SRAM `0030`, bit `80`) para que `0230` habilitara Magic en `CA80`. Confirmó después el consumidor de texto `A000:48C8` mediante entrada normal del menú; P8 por sí solo no estableció ese vínculo.

Evidencia histórica: `runtime/magic_gate/initial_wrong_id_trace.txt`, `corrected_gate_trace.txt` y `magic_still_none.png`; script `runtime/scripts/i11_p8_magic_flag_probe.lua` (nombre heredado de la hipótesis corregida). La superficie combinada conserva `PARTIAL_OPEN`: `Save Drum` y su descripción están aprobados; P10 muestra Magic en control, pero quedan un encabezado japonés y el aprendizaje natural.

## Decisión

La matriz sigue en 3 `PASS`, 2 `PARTIAL_OPEN` y 2 `OPEN`. I11 permanece `IN_PROGRESS`; I12, I13 e I14 están bloqueadas como etapas. Quedan cuatro etapas incompletas. La siguiente entrada útil exige una ruta real de tienda distinta de `C008=2` y `C0F2&0040`, la procedencia natural de una magia aprendida y del encabezado japonés, Link natural con interfaz válida, o consumidores reales de ancho máximo. No repetir el despacho sintético, el bit aislado ni los recorridos equivalentes.
