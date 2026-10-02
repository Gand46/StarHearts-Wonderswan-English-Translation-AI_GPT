# I11-P6 — origen inmediato de la bandera Link

Fecha: 2026-09-26. F26 SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`; ROM intacta. Lote acotado: desensamblado dirigido y dos variantes de una intervención sobre el mismo byte; ninguna ruta de juego repetida.

## Estructura y suma

El puntero lejano `1000:128E` de `CS:B3B2` apunta al bloque de SRAM del menú. La instrucción en `A000:B3A1` prueba el bit `04` de `es:[si+00AE]`, dirección lineal `0x1133C` y desplazamiento `0x133C` en el guardado de 32 KiB. En el guardado certificado ese byte vale `00`.

El desensamblado de `A000:ADA2` suma los bytes desde `0x128E` hasta `0x282C` inclusive (`0x159F` bytes), niega la suma a 16 bits y la compara en `A000:ADE2` con la palabra little endian de `0x282D–0x282E`. El archivo certificado confirma suma calculada y almacenada `9BA3`.

## Ensayo controlado

Tras restaurar una copia del guardado certificado, el script `runtime/scripts/i11_p6_link_source_probe.lua` puso `04` **solo en el byte mapeado de SRAM** antes de abrir el título. Sin corregir la suma, el menú dio `F44E=0C`: Link habilitado, Continue/WonderGate deshabilitados. La suma calculada dejó de coincidir con `9BA3`; esa variante no demuestra un guardado válido.

Se restauró de nuevo la copia certificada. La misma intervención con `MESEN_REPAIR_CHECKSUM=1` actualizó la palabra de suma en RAM antes del título:

| Frame | SRAM `0x133C` | Suma calculada/almacenada | Máscara `F44E` | Selector `F44F` |
| ---: | ---: | --- | ---: | ---: |
| 60, antes | `00` | `9BA3` / `9BA3` | `00` | `00` |
| 60, después | `04` | `9B9F` / `9B9F` | `00` | `00` |
| 140, título | `04` | `9B9F` / `9B9F` | `0F` | `00` |
| 490, Down→Right | `04` | `9B9F` / `9B9F` | `0F` | `03` |

El título mantuvo Continue y seleccionó Link Cable mediante entradas normales bajo **guardado sintéticamente alterado y suma corregida**. Al confirmar, volvió a aparecer una pantalla uniforme sin `WAITING P2` ni `LINK ERROR`. Los PNG de selección y confirmación son byte a byte idénticos a los ya incluidos en `runtime/link_gate/` de P5; no se duplican. La suma calculada cambió posteriormente durante la transición, por lo que esta prueba solo afirma su validez hasta la selección.

## Decisión

La compuerta Link lee el bit `04` de un campo protegido por suma en SRAM. No se ha demostrado qué evento de juego escribe naturalmente ese bit, ni una espera/error Link válida en F26. Link Cable sigue `OPEN`; I11 permanece 3 PASS, 2 PARTIAL_OPEN y 2 OPEN, con I12 bloqueada. Quedan cuatro etapas I11–I14. Ahorro de tokens: no medido; se evitó duplicar imágenes y reintentos equivalentes.
