# I01 — Tracing del consumidor `0x0022`

Fecha: 2026-09-26  
Estado: **DONE**  
Cambio binario liberable: **no**

## Resultado ejecutivo

La familia `22 00 <CP932> 21 00 00 00` queda clasificada como fuente de nombres visibles de entidades.

- 214 ocurrencias y 188 textos distintos pasan a `CONSUMER_PROVEN`.
- El operando de `0x0022` se copia a un búfer de nombre de entidad y ese búfer llega a una rutina que resuelve glifos y configura DMA hacia memoria de vídeo.
- Los 181 campos japoneses con relleno cero observados antes de estos registros no son leídos por el handler `0x0022`.
- Regla de sincronización: traducir el operando `0x0022`; conservar cada campo compañero sin cambios hasta demostrar un consumidor separado.
- La ROM inglesa F18 conserva su SHA-256 original. Ninguna ablación temporal fue retenida.

I02 queda desbloqueada para resolver contexto, terminología y ancho antes de integrar traducciones.

## Cadena consumidora demostrada

| Etapa | CPU | Offset físico | Evidencia |
| --- | --- | --- | --- |
| Despacho | `9000:311C` | `0x39311C` | Lee opcode de `ES:SI`, incrementa `SI` y llama la tabla `9000:317A`. |
| Entrada `0x0022` | `9000:31BE` | `0x3931BE` | La entrada contiene `0x3564`. |
| Selección de entidad | `9000:0BB0` | `0x390BB0` | Busca una entidad activa por dos claves y devuelve su registro en `DI`. |
| Copia de nombre | `9000:3564` | `0x393564` | Copia hasta ocho glifos CP932 desde el operando a `DI+0x62` y termina con `0x0000`. |
| Puente de render | `9000:E929` | `0x39E929` | Entrega el búfer `DI+0x62` a `A000:B7DE`. |
| Carga de glifos | `A000:B7DE` | `0x3AB7DE` | Resuelve hasta ocho glifos y configura DMA por puertos `0x40–0x48` hacia memoria de vídeo. |

Los seis tramos de código son idénticos entre la ROM japonesa y F18. Sus límites y hashes están en `I01_CONSUMER_TRACE.json`.

## Relación con campos compañeros

El censo reproducible encontró:

- 181 campos japoneses de ancho fijo y relleno cero;
- 178 de 214 operandos con un campo previo a no más de 128 bytes;
- 36 sin compañero en esa ventana;
- 165 pares a distancia exacta de 34 bytes;
- dentro de esos 165: 48 textos idénticos, 114 compañeros que añaden sufijo y 3 relaciones distintas.

El sufijo aparece en el campo compañero, pero el handler `0x0022` empieza en el operando posterior al opcode y avanza únicamente hacia delante. Por ello el compañero no alimenta el nombre visible mediante esta ruta. No se declara que los 181 campos carezcan de consumidor: se clasifican como identificadores internos probables con consumidor independiente aún no demostrado y se retienen.

## Ablaciones controladas

Se ensayaron cinco muestras representativas —BANK `0x19`, `0x1A`, `0x1C`, `0x1F` y `0x20`— con tres variantes temporales por muestra:

1. solo operando;
2. solo compañero;
3. operando y compañero.

Resultado de las 15 variantes:

- modificar solo el operando cambia la salida del bucle de copia `0x0022`;
- modificar solo el compañero no cambia esa salida;
- modificar ambos produce la misma salida de nombre que modificar solo el operando;
- la gramática `21 00 00 00` y el checksum WonderSwan quedaron válidos en todas las copias temporales;
- ninguna copia temporal se conservó ni ingresó en la ROM de trabajo.

La simulación es fiel a las instrucciones del handler, pero no sustituye una captura de cada entidad en su ruta natural. Los detalles están en `I01_ABLATION_RESULTS.json`.

## Tracing runtime acotado

La sonda física de Mesen se validó con un control positivo: el diálogo visible de F12 en `0x193740–0x193760` produjo 63 lecturas durante 3000 cuadros y expuso las rutinas lectoras esperadas.

Los 214 registros `0x0022` produjeron cero lecturas durante 28 720 cuadros acumulados de cobertura acotada: boot, First Trial, navegación hacia Wampa y cinco checkpoints naturales. Este resultado solo delimita la cobertura temprana; no se usa para declarar invisibilidad.

## Disposición de I01

| Universo | Cantidad | Estado | Acción |
| --- | ---: | --- | --- |
| Operandos `0x0022` | 214 | `CONSUMER_PROVEN` | Traducir tras aprobación de contexto y ancho. |
| Textos distintos | 188 | Pendientes de I02 | Resolver glosario y forma CP932 de hasta 8 glifos. |
| Campos compañeros | 181 | Consumidor independiente no probado | Retener; no sincronizar automáticamente. |
| ROM F18 | 1 | Sin cambios | Sigue siendo la base binaria. |

## Compuerta

`G02_CONSUMER`: **PASS para la familia `0x0022`**.

Permanecen abiertas las compuertas de contexto, anchura, integración, runtime individual, visual y función. No se autoriza todavía modificar los 214 registros en una ROM liberable.
