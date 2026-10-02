# I11-P13 — origen de los bits de adquisición de Magic

Fecha: 2026-09-26. Análisis estático acotado sobre F27 SHA-256 `641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4`; **sin cambio binario ni nueva aprobación visual**. Esta tanda no repite los dos bits inyectados ni la captura Magic de P12.

## Cadena de producción encontrada

| Lugar ROM / CPU | Instrucción decisiva | Resultado |
| --- | --- | --- |
| `0x393B70` / `9000:3B70` | `lds bp,[cs:3BF0]`, `sar ax,3`, `ror al,cl`, `or [bp],al` | Activa el bit de `AX` en el bitset con base `1000:0022`. Es la contraparte escritora del comprobador `9000:3BD0`. |
| `0x395028` / `9000:5028` | Clasifica el identificador de objeto recibido en `AX`; para `AX<0060` o `AX>00DF` invoca `9000:50F4` | Punto de entrada general de obtención. `0160` sigue esta rama. |
| `0x3950F4` / `9000:50F4` | Normaliza el identificador y pasa por `9000:A4A2` antes de marcarlo | Ruta de adquisición para objetos que no son equipo. No basta con escribir SRAM: la función aplica sus propias condiciones. |
| `0x395124–0x39514D` / `9000:5124–514D` | Para `0160≤BP<018D`, activa `0070` y `BP+00D0` | El primer identificador de ese intervalo, `0160`, produce exactamente `0070` y `0230`. |
| `0x39514E–0x395163` / `9000:514E–5163` | Para `0230`, `0234` y `0239`, activa también el bit sucesor | Adquirir `0160` produce asimismo `0231`; la prueba anterior de dos bits era un mínimo para abrir el menú, no una reproducción completa de la adquisición. |

Hay cinco sitios de llamada directa a `9000:5028` en Bank 39 (`0x393346`, `0x39AE92`, `0x39C7B0`, `0x3A3BEE`, `0x3AA407`); varios toman el identificador de estructuras de estado, sin una constante `0160` junto a la llamada. Por tanto, esta cadena identifica el **productor nativo y el identificador de entrada**, pero todavía no vincula un evento de mapa o un encuentro específico con `0160`. No se infiere que el checkpoint guardado ya haya aprendido Fire. La secuencia aislada `68 60 01` en `0xE79A4` no muestra contexto de código y no se toma como referencia de evento.

## Implicación para la auditoría

La siguiente prueba con valor demostrable debe localizar el origen de un objeto `0160` en un evento del juego y recorrerlo con entradas normales sobre F27. P10/P12 ya demuestran el consumidor y el diseño inglés bajo control; no se vuelven a ejecutar como sustituto del evento natural. Magic sigue `PARTIAL_OPEN`; la matriz conserva 3 `PASS`, 2 `PARTIAL_OPEN`, 2 `OPEN`. Tienda, Link y el denominador visual de ancho siguen abiertos. I11–I14 siguen siendo cuatro etapas incompletas; ahorro exacto de tokens `NOT_MEASURED`.

Evidencia reproducible: desensamblado localizado de los intervalos ROM `0x393B70–0x393BD0` y `0x395028–0x3951CF`, búsqueda de referencias directas a `9000:5028` y comparación algebraica `0160+00D0=0230`. No se distribuye la ROM ni se ensayó una ruta de juego equivalente adicional.
