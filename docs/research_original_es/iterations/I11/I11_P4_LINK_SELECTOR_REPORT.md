# I11-P4 — selector del título y Link Cable

Fecha: 2026-09-26. ROM F26 SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`. Sin cambio binario.

## Prueba diferencial nativa

Se arrancó F26 desde el mismo guardado certificado y se capturó la WRAM del título antes y después de una única dirección por ejecución. El byte `0xF44F` tuvo estos valores estables al frame 300:

| Entrada | Selección visible | `0xF44F` |
| --- | --- | ---: |
| Ninguna | Continue | 0 |
| Right | WonderGate | 1 |
| Down | New Game | 2 |
| Down2 | Continue | 0 |

Una secuencia natural Down → Right dejó New Game seleccionado; confirmó New Game al pulsar A. Las capturas `runtime/link_diagnostic/new_game_selected_natural.png` y `wondergate_selected_natural.png` documentan las dos direcciones funcionales. Las WRAM completas quedan fuera del paquete.

## Prueba sintética limitada

Una sola escritura reversible de `3` a `0xF44F` en RAM (ROM intacta) hizo que el menú dibujara el marco sobre Link Cable. El rótulo Continue permaneció resaltado y, al confirmar, apareció una transición oscura sin mensaje legible; después quedó una pantalla blanca. Las tres capturas `runtime/link_diagnostic/link_*` son **diagnósticas**, no PASS visual. No se observó `WAITING P2` ni `LINK ERROR` en un contexto válido.

El índice 3 pertenece al selector visual, pero esta manipulación no demuestra que Link Cable sea alcanzable naturalmente ni que funcione con el hardware de enlace. Se intentó trazar escrituras del selector en dos dominios de memoria; ambos callbacks dieron cero eventos. La causa del bloqueo natural sigue `NOT_VALIDATED`. El script `runtime/scripts/i11_p4_title_state_probe.lua` reproduce las entradas y la intervención sintética con límite de 1.110 frames.

## Decisión

Link Cable permanece `OPEN`. La matriz I11 conserva 3 PASS, 2 parciales y 2 abiertas; I12 continúa bloqueada. Un siguiente ensayo requiere una condición nueva demostrada del menú o un consumidor nativo de enlace con contexto gráfico válido. No repetir movimientos de título equivalentes. Quedan cuatro etapas I11–I14. Ahorro de tokens: no medido.
