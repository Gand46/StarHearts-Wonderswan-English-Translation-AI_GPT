# I02 — Contexto, glosario y adjudicación

Fecha: 2026-09-26  
Estado: **DONE**  
Cambio binario liberable: **no**

## Resultado ejecutivo

La totalidad del lote de I02 queda adjudicada antes de tocar la ROM:

- 237 ocurrencias pendientes agrupadas en 206 textos únicos;
- 206 traducciones aprobadas y cero `NEEDS_CONTEXT`;
- 214 ocurrencias del opcode `0x0022`, equivalentes a 188 nombres únicos, vinculadas al consumidor demostrado en I01;
- 23 ocurrencias adicionales, equivalentes a 18 términos, resueltas por su tabla o superficie estructural;
- 206 formas de pantalla pasan el prechequeo estático de glifos/bytes;
- cero colisiones entre formas de pantalla de términos japoneses distintos;
- F18 conserva el SHA-256 `fbb161d7b8dd10f279c436519d738c31aa321302019d53ca22d41300bfd55460`.

Se cierra `G03_CONTEXT`. `G04_ENCODING` y `G06_WIDTH` siguen abiertos: la codificación final, los punteros, el render y el ancho visual deben validarse después de cada integración binaria.

## Entradas y método

- Línea base: `baseline/JP_PENDING_STRUCTURAL.csv` (238 filas: 237 pendientes y la exclusión documentada `Ａ型`).
- Consumidor de nombres: `iterations/I01/I01_CONSUMER_TRACE_REPORT.md`.
- Fuentes terminológicas: manifiestos F1/F2/F3/F5, formas ya fijadas en F18, el pool activo de Bank 0x38 y decisiones editoriales registradas por término.
- Generador reproducible: `build_i02_glossary.py`.

El generador vuelve a leer la línea base, comprueba el hash de F18, exige cobertura exacta de los 206 textos, codifica las formas aprobadas en CP932/fullwidth y falla ante exceso de límite o colisión de nombres.

## Decisiones obligatorias

| Japonés | Traducción aprobada | Contexto/límite |
| --- | --- | --- |
| インディキッド | Indi Kid / `IndiKid` | Etiqueta inline, 7 glifos + NUL |
| リカルド | Ricardo / `Rica` | Etiqueta inline, 4 glifos + NUL |
| ズンター | Zunter / `Zunt` | Etiqueta inline, 4 glifos + NUL |
| ろうじん | Elder / `Eldr` | Etiqueta inline, 4 glifos + NUL |
| アクセル | Accel | Nombre de entidad, 8 glifos |
| メタリコ | Metalico | Nombre de entidad, 8 glifos exactos |
| ト | To | Alias visible de un kana, 8 glifos disponibles |

`ト` queda deliberadamente como `To`: I01 demostró que el handler visible consume únicamente ese operando. La relación con el campo interno `トペークン` y con el índice 112 de la tabla de entidades aporta contexto, pero no autoriza expandir el texto visible a una forma que el registro no contiene.

En la delimitación binaria previa a I03 se comprobó que las etiquetas de Bank `0x21` no son campos genéricos de ocho glifos: son cadenas inline terminadas en `0000`, seguidas inmediatamente por el siguiente opcode. Para preservar los controles sin repointing ni cambio de diccionario MTE, las cuatro formas de pantalla anteriores se documentan como abreviaturas técnicas; sus nombres canónicos no cambian.

## Superficies de ancho fijo

| Superficie | Forma aprobada | Uso/límite |
| --- | --- | --- |
| 武器 | WPN | Campo de equipo, 4 glifos |
| 防具 | ARM | Campo de equipo, 4 glifos |
| 買う | BUY | Comando de tienda, 4 glifos |
| 売る | SEL | Comando de tienda, 3 glifos; en I03 el consumidor real demostró que la forma de 4 glifos perdía el terminador y se renderizaba incompleta |
| 現在対戦者を待っています | WAITING P2 | Mensaje Link, 10 de 12 glifos |
| 所持… | OWNED | Campo de tienda, relleno hasta 16 bytes al integrar |
| 買値… | BUYPRICE | Campo de tienda, 8 glifos |
| 修理… | REPAIR | Campo de tienda, relleno hasta 16 bytes al integrar |
| 火の玉を飛ばす | Shoots fireball. | Descripción de magia, 16 glifos exactos |

El mensaje de error de enlace se codificará como `LINK ERROR\r\n「<FE×6>」`: ocupa 32 de 36 bytes y conserva tanto CRLF como los seis bytes de parámetro `FE`.

## Artefactos de decisión

- `I02_GLOSSARY.csv`: una fila por texto único, con traducción canónica, forma codificada, bytes CP932, familias, bancos, contexto, límites, fuente y aprobación.
- `I02_ADJUDICATION.csv`: una fila por cada una de las 237 ocurrencias, con estados de consumidor, contexto, traducción, ancho, integración y runtime.
- `I02_WIDTH_PRECHECK.csv`: presupuesto estático por término y obligación de revisión visual posterior.
- `I02_VALIDATION.json`: conteos, pruebas de round-trip, colisiones, fuentes y límites de la compuerta.
- `I02_SUMMARY.json`: resumen legible por máquina y decisiones terminológicas obligatorias.

## Validación y límites

- 205 cadenas ordinarias reproducen exactamente sus bytes tras `CP932 decode → encode`.
- El mensaje con parámetros se valida aparte: 32/36 bytes, seis `FE` y CRLF preservados.
- Las 206 formas caben en su presupuesto estático.
- No se modificaron punteros, checksum ni ROM; por ello esas pruebas no aplican todavía.
- No se ejecutó QA visual/runtime en I02; un prechequeo de ancho no demuestra ausencia de clipping en pantalla.
- Los 181 campos compañeros de I01 permanecen sin cambios y fuera de esta integración.

## Compuerta de salida

- [x] 237 ocurrencias con contexto y traducción adjudicados.
- [x] 206 términos únicos con traducción aprobada.
- [x] Cero `NEEDS_CONTEXT`.
- [x] Fuente terminológica, consumidor, CP932 y presupuesto registrados.
- [x] Evidencia negativa y la exclusión `Ａ型` conservadas.
- [x] Ningún cambio experimental ni binario retenido.
- [x] `G03_CONTEXT` cerrado.
- [ ] `G04_ENCODING`, `G05_POINTERS`, `G06_WIDTH`, runtime, visual y función: pendientes de las iteraciones binarias.

Resultado: **PASS** para I02.

## Estado siguiente

I03 queda habilitada para integrar únicamente las 11 ocurrencias de Bank `0x21` sobre una copia de F18. La integración deberá preservar controles, validar bytes y punteros, comprobar checksum, alcanzar las superficies afectadas y producir un BPS acumulativo JP → F20. No se autoriza todavía integrar en bloque los 214 nombres `0x0022`.
