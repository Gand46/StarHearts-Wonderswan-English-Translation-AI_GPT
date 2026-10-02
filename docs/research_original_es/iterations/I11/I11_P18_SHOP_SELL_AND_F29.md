# I11-P18 — selector de venta, japonés residual y corrección F29

Fecha local: 2026-09-27. Dos superficies acotadas: tienda y muestra máxima `BUYPRICE`. Cuatro métodos: ejecución controlada de `SEL`, procedencia del recurso comprimido, reconstrucción con glifos nativos y regresión/build/BPS. No se repitieron recorridos Wampa, Magic ni Link. Ahorro exacto de tokens: `NOT_MEASURED`.

## Ruta `SEL` y hallazgo

`runtime/scripts/i11_p18_controlled_shop_sell.lua` reutiliza el evento nativo `0014/0031` ya probado en P17 y cambia solo la entrada del selector: Down y A. La traza registra `9000:D026` y `A000:A4E0`, por lo que la captura pertenece al panel real de venta. F28 mostró directamente cinco rótulos japoneses visibles: `装備アイテム`, `武器`, `防具`, `タリスマン` y `アミュレット`. Ese panel no puede aprobarse por contexto ni por inferencia.

La misma ejecución leyó el rótulo de cantidad en Bank `0x37`, pero no leyó `BUYPRICE` ni `REPAIR`: el checkpoint probado no contenía un artículo vendible en esa ruta. Un segundo guardado con equipo no alcanzó el paso activo del intérprete durante el límite de 500 cuadros; se conserva solo como resultado negativo privado y no se repite. Por tanto, una venta completa, el precio y reparación siguen abiertos.

## Procedencia y corrección F29

La traza de ROM enlaza el panel con el descriptor de Bank `0x30` en `0x30843C`, recurso original `0x30B7AE`. Sus cuatro cuadros internos se descomprimen a 2144, 1024, 14336 y 64 bytes; el cuadro 0 carga gráficos en `0x8000` y el cuadro 1 el mapa en `0x3800`. Esto demuestra el consumidor y permite corregir el recurso sin tocar cadenas o gráficos no relacionados.

F29 repunta ese único descriptor a `0x30F38E` e instala un recurso de 2048 bytes. Muestra `Gear Items`, `Arms`, `Armor`, `Charms` y `Amulets`. Todos los píxeles proceden de rótulos ingleses ya renderizados por la fuente nativa del juego en la captura aprobada `runtime/menu/arms_after.png`; se conservan paleta, borde, fondo, mapa base y regla inferior. La revisión directa de `runtime/shop_f29/sell_panel_f29_english.png` confirma los cinco rótulos completos, alineados y legibles.

Frente a F28 cambian 869 píxeles, limitados a `x=24–94, y=8–83`. `BUY/SEL`, el panel de compra F28 y el arranque frío son byte idénticos a sus capturas aceptadas. No se detectó regresión fuera del panel corregido.

## Reproducibilidad

F29 tiene SHA-256 `4704a7d4e06696455ac6017632135c03259e42783f7af095b0231246e754eadb` y checksum WonderSwan `9639`. `F29_SOURCE/scripts/build_sell_category_resource.py` reproduce byte a byte el recurso SHA-256 `afb35868f0bf83fa9f9f438e89f0594ea186b7670d9e55d78f4182cacd521819`; `build_phase13BG_F29.py` reconstruye F29 desde la ROM japonesa original. El BPS acumulativo JP→F29 tiene SHA-256 `d2011c478085c32ef0c95517b92ee6d7e732d161d22e51a1517da1563d78990a` y su aplicación reproduce la ROM byte a byte.

Evidencia distribuible: `runtime/shop_f29/`, `runtime/scripts/i11_p18_controlled_shop_sell.lua`, `runtime/scripts/i11_p18_build_sell_resource.py`, `runtime/scripts/i11_p18_render_sell_resource.py`, `F29_SOURCE/` y `patches/StarHearts_EN_phase13BG_F29_CUMULATIVE_2026-09-27.bps`.

## Estado

La tienda permanece `PARTIAL_OPEN`: ya están aprobados en ejecución controlada el diálogo, `BUY/SEL`, compra, entrada a `SEL`, selector de categorías y la corrección F29; faltan entrada natural, artículo vendible, venta funcional, precio y reparación. `BUYPRICE` no se aprueba como muestra 8/8 porque no fue leído ni dibujado. La matriz conserva **3 PASS, 3 PARTIAL_OPEN y 1 OPEN**. I11 continúa y quedan **cuatro etapas incompletas: I11–I14**.
