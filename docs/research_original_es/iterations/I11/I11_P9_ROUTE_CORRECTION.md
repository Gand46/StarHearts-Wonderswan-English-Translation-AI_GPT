# I11-P9 — ruta Link y diagnóstico de menú principal

**Rectificación I11-P10:** P9 clasificó erróneamente `A000:3A90`, `A000:404C`, `A000:4FA0` y `A000:5144` como ruta de tienda. Son flujo del menú principal y sus categorías. `C0F2&0040` abrió el menú ordinario. `0230` forma parte del grupo de Magic cuando también está presente `0070`; `0252` pertenece a otro grupo del menú. No se identificó entrada natural de tienda. Las trazas brutas P9 se conservan con esta clasificación corregida.

Fecha: 2026-09-26. F26 intacta, SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`, checksum `6ABA`.

## Despacho Link

La opción 3 del título es Link Cable. Su confirmación asigna `C008=0002` y el despachador `9000:5BB0` salta a `A000:0120`. Por tanto, las 36/34/29 lecturas controladas P8 de `OWNED`/`BUYPRICE`/`REPAIR` ocurrieron en una escena Link inválida, sin demostrar una venta ni un panel de tienda. `runtime/route_correction/controlled_label_callers.txt` registra 99 lecturas tempranas de esas etiquetas sin probar cuál se dibujó.

## Menú principal

La máscara `C0F2&0040` se comprueba en `9000:5D4C` y alcanza `A000:3A90` mediante `9000:5D5D` fuera de las áreas excluidas `CAD3=0025/006E`. La captura P9 muestra el menú ordinario. El checkpoint consultó esa puerta 120 veces con `C0F2=0000`; una escritura temporal `0040` alcanzó una vez `A000:3A90`, sin hits en `A000:4FA0`, `A000:5144` ni lecturas Bank 37. Las etiquetas originales `shop_entry/menu/screen` del archivo `controlled_field_gate.txt` son nombres instrumentales heredados; no designan tienda.

`A000:3CAE` construye `CA80` para disponibilidad de categorías del menú. Busca IDs `0230–0251` para el bit `8000` y `0252–025F` para el bit `4000`. P10 confirmó que el primer grupo necesita además `0070` y habilita Magic. `A000:404C` despacha categorías del menú; `A000:4FA0` y `A000:5144` no constituyen una cadena de tienda probada. Las referencias Bank 37 en `A000:A974`, `A000:A9CE` y `A000:AA2C` siguen siendo punteros verificados estáticamente, sin ruta natural de tienda.

Evidencia histórica: `runtime/route_correction/natural_checkpoint_gate.txt`, `controlled_field_gate.txt` y `controlled_label_callers.txt`; scripts `runtime/scripts/i11_p9_shop_gate_snapshot.lua` e `i11_p9_field_shop_gate_probe.lua` (nombres anteriores a la rectificación).

## Ancho y estado

I02 clasifica `BUYPRICE` como etiqueta de 8/8 glifos. Su consumidor natural y sus píxeles no se han identificado ni aprobado. La contabilidad de 209/214 operandos al límite físico sigue separada de la cobertura visual. I11 conserva 3 superficies `PASS`, 2 `PARTIAL_OPEN` y 2 `OPEN`; quedan cuatro etapas incompletas. Véase `I11_P10_MAGIC_ROUTE_AND_HEADER.md` para el consumidor Magic y la muestra controlada legible.
