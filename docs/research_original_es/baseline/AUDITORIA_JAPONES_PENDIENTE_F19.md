# Auditoría de japonés pendiente — Star Hearts F19 CORE DEPURADO

Fecha: 2026-09-26  
Alcance: ROM jugable incluida en el handoff F19 (`F18_CHECKPOINT`), análisis estructural completo dirigido y una ruta acotada en Mesen.  
Resultado: **NO APTO para afirmar traducción completa**.

## Dictamen

La auditoría encontró **237 ocurrencias estructurales pendientes**, correspondientes a **206 textos japoneses distintos**:

| Evidencia | Ocurrencias | Textos distintos | Interpretación |
|---|---:|---:|---|
| `STATIC_HIGH` | 23 | 21 | Campo/tabla/mensaje estructurado o destino de puntero todavía japonés. |
| `STATIC_MEDIUM` | 214 | 188 | Operando japonés bajo una gramática de script repetida; falta confirmar semántica del consumidor `0x0022`. |
| `RUNTIME_CONFIRMED_VISIBLE` | 0 | 0 | Ningún pendiente fue alcanzado visualmente en esta iteración. |
| Retenido y comprobado no visible | 1 | 1 | `Ａ型` conserva `型`, pero la ruta validada solo muestra `A`. |

`RUNTIME_CONFIRMED_VISIBLE = 0` **no significa que los 237 no se muestren**; significa que su renderizado aún no fue capturado. Conforme a las reglas universales v1.5, no se concede `PASS` visual con evidencia estática y no se informa un porcentaje global sin denominador exhaustivo.

## Distribución de pendientes

| Banco | Ocurrencias | Familia principal |
|---:|---:|---|
| `0x19` | 24 | operandos de nombre de script `0x0022` |
| `0x1A` | 21 | operandos de nombre de script `0x0022` |
| `0x1B` | 31 | operandos de nombre de script `0x0022` |
| `0x1C` | 32 | operandos de nombre de script `0x0022` |
| `0x1D` | 32 | operandos de nombre de script `0x0022` |
| `0x1E` | 22 | operandos de nombre de script `0x0022` |
| `0x1F` | 37 | operandos de nombre de script `0x0022` |
| `0x20` | 15 | operandos de nombre de script `0x0022` |
| `0x21` | 11 | nombres, mensaje de enlace y rótulos de menú |
| `0x37` | 4 | espera de enlace y rótulos de tienda |
| `0x38` | 8 | destinos japoneses aún seleccionados por tablas conocidas |
| **Total** | **237** | **206 textos distintos** |

## Hallazgo nuevo principal: BANK19–20

Se identificaron **214 operandos japoneses, 188 distintos**, con la gramática estricta:

```text
22 00 <texto CP932> 21 00 00 00
```

Aparecen dentro de bancos de script cuyo diálogo circundante ya fue traducido/reempaquetado. Ejemplos: `ティラワカ`, `ザイオン`, `アクセル`, `ベルフェゴー`, `リヴァイアサン`, `かなみ` y `みづき`.

La estructura es demasiado regular para tratarla como falso positivo, pero todavía falta demostrar mediante traza, disección del intérprete o captura de pantalla que `0x0022` alimenta un nombre visible. Por eso se clasifican como `STATIC_MEDIUM`, no como `RUNTIME_CONFIRMED`.

Además hay **181 campos japoneses internos/de nombre con relleno cero** en esos bancos. Muchos añaden sufijos para mantener identificadores únicos (`クン`, `ン`, `ター`, etc.). No se cuentan como unidades visibles independientes y no deben editarse a ciegas; primero hay que determinar si son identificadores, nombres de objeto o texto de presentación.

El CSV adjunto contiene las 214 ocurrencias, sus offsets y las grafías inglesas ya establecidas cuando existe evidencia en los manifiestos F anteriores. El resto queda como `NEEDS_TERMINOLOGY`.

## Hallazgos `STATIC_HIGH`

| Offset(s) | Japonés | Propuesta inicial | Evidencia/nota |
|---|---|---|---|
| `0x217C2A` | インディキッド | Indi Kid | Campo de nombre delimitado dentro de registro de script traducido; revisar grafía. |
| `0x218286`, `0x218338` | リカルド | Ricardo | Dos ocurrencias; grafía canónica documentada en F5. |
| `0x2182C6`, `0x218568` | ズンター | Zunta | Dos ocurrencias; el diálogo adyacente contiene `Ｚｕｎｔａ！`. |
| `0x218CBE` | ろうじん | Old man | Rótulo de rol/nombre. |
| `0x219610` | 通信エラー「`FE×6`」… | Communication error… | Mensaje estructurado con seis parámetros `0xFE` y CRLF; conservar controles. |
| `0x2192F6` | 武器 | Weapon | Rótulo fijo de menú. |
| `0x2192FE` | 防具 | Armor | Rótulo fijo de menú. |
| `0x219432` | 買う | Buy | Rótulo fijo de tienda. |
| `0x21943A` | 売る | Sell | Rótulo fijo de tienda. |
| `0x370000` | 現在対戦者を待っています | Waiting for opponent. | Mensaje CP932 al inicio del banco; probable modo Link Cable. |
| `0x3769D0` | 所持 | Owned | Campo fijo de 16 bytes; referencia exacta en código `0x3AAA2C`. |
| `0x3769E2` | 買値 | Buy price | Campo fijo de 16 bytes; referencia exacta en código `0x3AA9CE`. |
| `0x3769F4` | 修理 | Repair | Campo fijo de 16 bytes; referencia exacta en código `0x3AA974`. |
| `0x38130F` | 弾 | Bullet / Ammo | El slot `0x38024C` aún selecciona este destino; confirmar semántica. |
| `0x381E6E` | 豆 | Bean | El slot `0x3804B8` aún selecciona este destino. |
| `0x381E72` | 鉄 | Iron | El slot `0x3804C8` aún selecciona este destino. |
| `0x386690` | ファイヤー | Fire | Primer slot de la tabla de 33 nombres mágicos (`0x38664C`). |
| `0x38684A` | 火の玉を飛ばす | Shoots a fireball. | Primer slot de 33 descripciones mágicas (`0x386806`). |
| `0x386CA2` | アクセル | Axel | Slot `0x386B60`; grafía canónica documentada en F2. |
| `0x386E92` | メタリコ | Metalico | Slot `0x386BBE`; requiere revisión terminológica. |
| `0x38710E` | ト | `NEEDS_CONTEXT` | Slot `0x386C40`; no traducir por conjetura. |

## Revisión específica de BANK38 y del número anterior “623”

El valor anterior de **623** provenía de dividir dos rangos por dobles NUL y decodificarlos como CP932. Era un inventario de fragmentos almacenados, no 623 textos activos.

El censo nuevo sigue las tablas conocidas:

| Familia | Slots con destino japonés en JP | Reapuntados/re-codificados en EN | Destino aún japonés | Traducido in situ |
|---|---:|---:|---:|---:|
| Ítems/nombres/descripciones | 1,158 | 1,155 | 3 | 0 |
| Nombres mágicos | 33 | 32 | 1 | 0 |
| Descripciones mágicas | 33 | 32 | 1 | 0 |
| Nombres de entidades | 160 | 157 | 3 | 0 |
| Nombres de mapa | 12 | 11 | 0 | 1 |
| **Total** | **1,396** | **1,387** | **8** | **1** |

La tabla primaria de localizaciones de 257 entradas no conserva candidatos japoneses activos. Los **268 sufijos japoneses** de los registros del mapa mundial se mantienen clasificados como no renderizados por la evidencia previa del consumidor, que usa únicamente `x/y/type`.

## Japonés almacenado que no se cuenta como pendiente visible

- Los pools CP932 originales de BANK38 permanecen en la ROM después del reapuntamiento a inglés/MTE. Su mera presencia no demuestra consumo.
- Los 268 sufijos del mapa mundial ya cuentan con evidencia previa de no renderizado.
- Las tablas kana, análisis de nombre, palabras reservadas/prohibidas de BANK36 son datos funcionales, no objetivos de reemplazo global.
- El bloque de misión que comienza en `0x365216` no es seleccionado por la tabla de 49 entradas auditada.
- `Ａ型` en `0x362EB8` es destino de una tabla real, pero las capturas `f0380` y `f0420` muestran únicamente `A`; `型` queda recortado/no renderizado.
- Los 181 campos internos/de nombre de BANK19–20 quedan `NEEDS_TRACE`; no se editan ni se suman como unidades visibles.

## Verificación dinámica acotada

La ruta `route_hero_short_F8.lua` terminó con `PASS hero_short` en Mesen 2.1.1. Cubrió arranque, New Game, género, nombre, fecha de nacimiento, grupo sanguíneo, confirmación y juego inicial.

Resultado visual específico: el grupo sanguíneo muestra solamente `A`; no aparece el carácter `型`. Ninguno de los 237 pendientes fue alcanzado en esa ruta.

No se validaron Link Cable, las pantallas de tienda relevantes, juego tardío, final ni créditos. Las coincidencias exactas `スタッフ`, `エンディング`, `プログラム` y `開発` caen en el pool fuente retenido de BANK38 y **no prueban** por sí mismas un corpus activo de créditos. Créditos/final permanecen `NOT_VALIDATED`.

## Escaneo crudo y falsos positivos

WS Text Auditor v0.1.1 devolvió 7,892 candidatos “strong” en la ROM inglesa con el límite/configuración usados; la ROM original alcanzó el tope de 10,000. Esos valores mezclan binario que parece Shift-JIS, fuentes retenidas, tablas funcionales y texto potencial. No son un denominador de traducción ni justifican reemplazos globales.

## Próximo cierre recomendado

1. Trazar o hacer una ablación controlada de un operando `0x0022` alcanzable para clasificar la familia de 214.
2. Si es visible, construir el glosario canónico desde las tablas/manifiestos existentes y actualizar todos los duplicados físicos requeridos sin tocar identificadores a ciegas.
3. Corregir los 23 `STATIC_HIGH` en un nuevo build, conservando controles, anchos fijos, punteros y checksum.
4. Capturar QA real de nombres, equipo/tienda, magia, entidades y Link Cable.
5. Recorrer final y créditos antes de cualquier afirmación RC/final.

## Integridad y reproducibilidad

- ROM JP: `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`
- ROM EN auditada: `fbb161d7b8dd10f279c436519d738c31aa321302019d53ca22d41300bfd55460`
- La auditoría es de solo lectura; **no se modificó la ROM**.
- `audit_japanese_pending.py` regenera y valida el CSV/JSON contra offsets, hashes, tablas y conteos esperados.

