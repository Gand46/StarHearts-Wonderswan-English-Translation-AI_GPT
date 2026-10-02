# I11-P3 — denominadores de ancho y acceso Link Cable

Fecha: 2026-09-26. ROM F26 SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`. Sin cambio binario.

## Hallazgo verificable de ancho

`I02_WIDTH_PRECHECK.csv` contiene 206 términos: 31 igualan su límite lógico de glifos. Se reparten en 24 términos de nombres de script (uno compartido con entidad), cuatro etiquetas de hablante, dos de tienda y una descripción de magia.

Los cuatro CSV de decisiones I06–I09 contienen 214 operandos `0x0022` integrados. En 209, la longitud del `integrated_display` iguala la capacidad física `capacity_glyphs`; I06 45/45, I07 60/63, I08 53/54, I09 51/52. Muchos nombres I02 de ocho glifos fueron compactados a campos físicos de 2–7 glifos; por tanto, los 31 términos lógicos **no** son el denominador visual de los 214 operandos finales. Estas son comprobaciones estructurales, no lecturas del texto renderizado.

La compuerta `G06_WIDTH` y la superficie aislados/ancho máximo permanecen `PARTIAL_OPEN`. El siguiente método útil es seleccionar consumidores reales a partir de los CSV de decisiones, capturar las formas *integradas* al límite y transcribir los píxeles antes de consultar el texto esperado. No extrapolar desde el prechequeo I02 ni desde OCR contextual.

## Link Cable: resultado negativo acotado

Desde título F26 con guardado certificado, tres secuencias nuevas probaron: `down2` antes de derecha, derecha seguida de `down` sostenido tras una espera, y varias pulsaciones derechas espaciadas. En las tres la selección visible se quedó en WonderGate (captura frame 440 SHA-256 `19749cf319531fc8706ce86b96124f1cfbe68c9cd6c12ed16575c99fd125c4d4`); al confirmar se entró a WonderGate/Bazar, no a Link Cable. La secuencia está parametrizada en `runtime/scripts/i11_p3_link_title_route.lua`. Los ensayos completos permanecen privados; no se duplicaron imágenes ya contenidas en `runtime/link_negative/`.

Esto no prueba que Link Cable sea inalcanzable: solo descarta esas entradas en el estado probado. Se detiene la navegación equivalente. Un reintento requiere hipótesis nueva —por ejemplo, evidencia de condición de habilitación o breakpoint del selector—. `WAITING P2` y `LINK ERROR` en F26 siguen sin PASS visual natural.

## Estado

La matriz I11 no cambia: 3 PASS, 2 parciales y 2 abiertas. I11 sigue `IN_PROGRESS`, I12 bloqueada. Restan I11–I14 (cuatro etapas). El ahorro de tokens no está medido.
