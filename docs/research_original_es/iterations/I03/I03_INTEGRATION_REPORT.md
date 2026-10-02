# I03 — Integración F20 de Bank 0x21

Fecha: 2026-09-26  
Estado: **DONE**  
Cambio binario: sí, sobre una copia privada de F18  
ROM F18 SHA-256: `fbb161d7b8dd10f279c436519d738c31aa321302019d53ca22d41300bfd55460`  
ROM F20 SHA-256: `3b8eafc74ba8d276d4b639bd806bfaf639786106a15e2ade9471198ad5e44a30`  
Checksum WonderSwan: `60D5`

## Resultado ejecutivo

Las 11 ocurrencias aprobadas de Bank `0x21` quedaron integradas, consumidas por sus rutinas nativas y verificadas. La inspección runtime detectó que `SELL` llenaba los ocho bytes sin NUL y el menú solo mostraba una `L`; se corrigió a `SEL`, se reconstruyó F20 y se repitieron las pruebas.

La ruta disponible desde el checkpoint natural no consume Bank `0x21`; esa evidencia negativa se conserva. Para cerrar el lote se usó una activación controlada no persistente: el opcode real `0x0014`, su handler `9000:338C`, el cargador `9000:BD30` y el stepper `9000:BE6C`. No se modificó la ROM para activar las superficies ni se sustituyó el decodificador del juego.

## Lote final

| Offset | Japonés | Canonical | Forma F20 | Validación runtime |
| --- | --- | --- | --- | --- |
| `0x217C2A` | インディキッド | Indi Kid | `IndiKid` | `9000:BFE6` copió 16 bytes exactos a `DI+0x62` |
| `0x218286`, `0x218338` | リカルド | Ricardo | `Rica` | Dos lecturas y dos copias exactas al búfer de entidad |
| `0x2182C6`, `0x218568` | ズンター | Zunter | `Zunt` | Dos lecturas y dos copias exactas al búfer de entidad |
| `0x218CBE` | ろうじん | Elder | `Eldr` | Lectura y copia exacta al búfer de entidad |
| `0x219610` | 通信エラー… | Link error [code] | `LINK ERROR` + CRLF + código | Visible, sin corte ni basura |
| `0x2192F6` | 武器 | Weapon | `WPN` | Visible y completo |
| `0x2192FE` | 防具 | Armor | `ARM` | Visible y completo |
| `0x219432` | 買う | Buy | `BUY` | Visible y completo |
| `0x21943A` | 売る | Sell | `SEL` | Visible y completo tras corrección de NUL |

Los seis nombres son metadatos de entidad consumidos por `9000:BFE6`; en estas rutas no constituyen una etiqueta independiente en pantalla. La prueba válida para esos campos es la lectura ROM y la copia CP932 exacta al búfer de nombre, acompañada por la ejecución del diálogo adyacente.

## Hallazgo corregido

La forma inicial `SELL` ocupaba cuatro glifos y eliminaba el terminador `0000`. El consumidor de tienda la mostraba como una sola `L`. La forma final `SEL` usa tres glifos más NUL, mantiene el campo de ocho bytes y coincide con el presupuesto demostrado en runtime.

## Validación estática y construcción

- 11/11 registros coinciden con el manifiesto final.
- 107 bytes difieren de F18, incluidos los dos bytes de checksum; 0 offsets inesperados.
- Terminadores, opcodes, parámetros, CRLF y seis bytes `FE` preservados.
- Diccionario MTE intacto y sin repointing.
- `BUILD.bat` y `build.sh` reconstruyen F20 desde la ROM JP limpia.
- BPS acumulativo JP → F20 e incremental F18 → F20 reconstruyen el SHA final byte a byte.

## Runtime y visual

| Superficie | Evidencia | Resultado |
| --- | --- | --- |
| Boot/título | `runtime/boot_f20.png` | PASS_SMOKE |
| Gameplay/overlay | `runtime/menu_start_f20.png` | PASS_SMOKE |
| Seis nombres | `runtime/controlled_bank21/speakers/*_trace.txt` | PASS_RUNTIME_CONSUMER_BUFFER |
| WPN/ARM | `wpn_arm_trace.txt` + `wpn_arm_f20.png` | PASS_RUNTIME_VISUAL |
| BUY/SEL | `buy_sel_trace.txt` + `buy_sel_f20.png` | PASS_RUNTIME_VISUAL_AFTER_CORRECTION |
| Error Link | `link_error_trace.txt` + `link_error_f20.png` | PASS_RUNTIME_VISUAL |

La cobertura natural completa queda reservada para las iteraciones globales de regresión. No se usa OCR como autoridad.

## Compuerta de salida

- [x] 11 candidatos integrados y estáticamente verificados.
- [x] Los 11 campos fueron consumidos por rutinas originales.
- [x] Todas las superficies renderizadas del lote fueron inspeccionadas.
- [x] Defecto `SELL` corregido y revalidado como `SEL`.
- [x] Boot y checkpoint natural sin regresión aparente.
- [x] Checksum y ambos BPS verificados.
- [x] Evidencia positiva y negativa conservada.
- [x] Sin cambios experimentales en la ROM liberable.

Resultado: **PASS / I03 DONE**. I04 queda habilitada.
