# I11-P5 — compuerta nativa de Link Cable

Fecha: 2026-09-26. F26 SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`; ROM intacta.

## Hipótesis y prueba acotada

El desensamblado del banco físico `0x3A`, offsets `0x3AB37B–0x3AB49D`, muestra que la rutina inicializa la máscara de opciones `F44E=04`; la llamada a `A000:ADE2` puede añadir `03` para Continue/WonderGate. Un `test es:[si+00AE],04`, usando el puntero lejano situado en `CS:B3B2`, añade `08` para Link Cable. El cambio de selección pasa por `B3B6`: comprueba `F44E & (1 << candidato)` antes de escribir `F44F`. Por tanto, el valor 3 del selector solo es alcanzable con entradas normales cuando el bit 3 de `F44E` está habilitado.

Desde la copia restaurada del guardado certificado, la captura inicial registró `F44E=07`, `F44F=00`. Una escritura **sintética y reversible solo en WRAM** añadió `08` a `F44E` en el frame 150. Después se usaron entradas normales Down y Right, seguidas de A:

| Frame | Máscara `F44E` | Selector `F44F` | Observación |
| ---: | ---: | ---: | --- |
| 140 | `07` | `00` | Título antes de la intervención |
| 300 | `0F` | `02` | New Game seleccionado con Down |
| 490 | `0F` | `03` | Link Cable seleccionado con Right; marco y rótulo visibles |
| 700 | `0F` | `03` | Tras A, pantalla uniforme sin texto de espera/error |
| 1100 | `0F` | `03` | Pantalla uniforme persistente |

Las capturas `runtime/link_gate/link_selected_controlled.png` y `link_confirmed_invalid.png` documentan el resultado. La primera aprueba únicamente el dibujo de la opción en el título **bajo habilitación sintética**; la segunda no aprueba el consumidor de enlace. El script `runtime/scripts/i11_p5_link_gate_probe.lua` reproduce la secuencia en 1.110 frames y exige la máscara inicial `07`. La prueba se detuvo ahí. Los intentos con un guardado de emulador alterado se descartaron y no forman parte de la evidencia.

## Decisión

Se ha explicado la condición inmediata que bloquea la navegación hacia Link Cable en el guardado disponible. La procedencia natural del bit `04` en la estructura apuntada y una pantalla `WAITING P2`/`LINK ERROR` válida siguen `NOT_VALIDATED`. Link Cable permanece `OPEN`; la matriz I11 continúa 3 PASS, 2 PARTIAL_OPEN, 2 OPEN. I12 sigue bloqueada. Quedan cuatro etapas I11–I14. Tokens ahorrados: no medidos.
