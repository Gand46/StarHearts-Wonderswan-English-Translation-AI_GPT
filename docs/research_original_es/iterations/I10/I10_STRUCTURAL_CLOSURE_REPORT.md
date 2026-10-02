# I10 — Cierre estructural y denominador F26-QA1

Fecha: 2026-09-26  
Estado: **DONE — censo estructural cerrado; I11 habilitada**

## Resultado

El segundo censo reconcilia las 237 candidatas activas con una integración verificable: 11 en I03/F20, 4 en I04/F21, 8 en I05/F22, 45 en I06/F23, 63 en I07/F24, 54 en I08/F25 y 52 en I09/F26. No hay hallazgos activos sin `record_id`, exclusiones nuevas ni japonés superviviente en los recursos activos revisados.

El denominador final documentado contiene 238 disposiciones: 237 registros integrados con PASS estático y `Ａ型` como único registro retenido no visible con evidencia previa.

## Comprobaciones reproducibles

- F26 permanece sin cambios: SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`, checksum `6ABA`.
- 214 operandos `0x0022`, opcodes y delimitadores `21 00 00 00`: PASS.
- Cambios inesperados fuera de los operandos inline en Banks `0x19–0x20`: 0.
- 181 campos japoneses internos/compañeros conservados para su consumidor separado: recuento estable F18 → F26.
- Cinco familias Bank `0x38`: 1.568 slots; 1.396 destinos japoneses originales; 1.395 repuntados; 1 traducido in-place; 0 supervivientes activos.
- 15 payloads fijos de Bank `0x21/0x37` y 8 destinos Bank `0x38`: PASS.
- Mensaje Link: CRLF y seis bytes `FE` preservados.
- Caracteres japoneses aislados en los 237 recursos activos: 0.

## `Ａ型` y consumidor alternativo

Existe una sola cadena exacta `Ａ型`, en `0x362EB8`. La única referencia lejana directa a su tabla es `6000:2EB0` en `0x394530`. El código en `0x3944FA` carga esa tabla con `LES`, la indexa por la selección de tipo sanguíneo y copia la cadena terminada en NUL. No apareció otro consumidor directo estructuralmente respaldado.

Se conserva la disposición `RETAINED_NONVISIBLE_WITH_EVIDENCE`: la ruta validada muestra solo `A`; la revisión visual se mantiene en I11 para evitar convertir evidencia estática en un PASS visual.

## Escaneo bruto

WS Text Auditor v0.1.1 produjo 7.861 candidatos fuertes con los parámetros compatibles con la línea base y 43.949 candidatos al habilitar caracteres aislados. Estos conteos incluyen pools fuente retenidos, tablas funcionales y coincidencias en datos/código; no son el denominador de traducción. La reconciliación estructural no produjo candidatos activos nuevos.

## Gate

I10 cumple su compuerta: cero hallazgos activos sin `record_id`, todas las disposiciones documentadas y denominador final cerrado. No se modifica la ROM ni se genera un BPS nuevo; el acumulativo JP → F26 continúa siendo el parche vigente.

Quedan cuatro etapas de la auditoría: I11 (QA runtime/visual), I12 (late game, ending y créditos), I13 (regresión y persistencia) e I14 (cierre RC).
