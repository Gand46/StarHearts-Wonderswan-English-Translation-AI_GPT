# I11-P17 — tienda nativa, corrección visual F28 y vecindad de Fire

Fecha local: 2026-09-26. Dos superficies: tienda y Magic. Cuatro métodos distintos y acotados: mapeo estructural de comandos de comercio, ejecución controlada del evento nativo, comparación visual F27/F28 y reconstrucción/BPS acumulativo. No se repitieron recorridos Wampa ni intentos equivalentes. Ahorro de tokens: `NOT_MEASURED`.

## Ruta estructural de tienda

El opcode de evento `0014` despacha a `9000:338C`, que entrega su operando a `9000:BD30`. Los IDs `0031–004E` seleccionan los índices de inventario `0–29`: sus punteros Bank 21 conducen a callbacks `9000:CEB0–CFD2`, cada callback escribe el índice en `EBC8` y salta al diálogo común `Bank21:93FE` con opciones **BUY/SEL**.

La sonda `runtime/scripts/i11_p17_scene_shop_map.py` recorrió las tablas de escenas y encontró **35 comandos de tienda en 29 escenas**. `runtime/p17_shop_magic/shop_scene_events.csv` registra para cada uno offset, escena, claves, script, ID e inventario. Esto sustituye la búsqueda abierta de “qué evento llama a la tienda” por un conjunto finito de disparadores. La navegación natural hasta uno de ellos sigue pendiente.

## Ejecución controlada y defecto observado

`runtime/scripts/i11_p17_controlled_shop_event.lua` partió del guardado válido First Trial y redirigió un único paso activo del intérprete al comando existente `0014/0031` de `0x1A6CA4` (escena `004D`, claves `0200/050C`). La cadena registrada fue `9000:338C → BD30 → CEB0 → Bank21:93FE`. La interfaz conservó el campo y paleta válidos, mostró el saludo del mercader y **BUY/SEL** completos, y abrió el panel de compra con nombres y precios legibles.

En F27, el rótulo `OWNED` de `0x3769D0` se almacenaba en ocho celdas, pero este consumidor solo dibuja las dos primeras: la pantalla mostraba **OW**. No se aprueba por contexto ni por los bytes fuente; la captura directa demuestra el truncamiento.

## Corrección F28

F28 cambia ese campo a **NO** seguido por seis espacios nativos. `NO` identifica el número poseído junto al contador y cabe en las dos celdas reales. Usa los glifos nativos, conserva posición, paleta, baseline y disposición. La pantalla F28 muestra ambos caracteres completos. Frente a F27 cambian 74 píxeles, todos dentro de `x=121–142, y=129–137`; la captura BUY/SEL es idéntica. Evidencia distribuible:

- `runtime/shop_f28/owned_f27_truncated.png`;
- `runtime/shop_f28/merchant_buy_sell_f28.png`;
- `runtime/shop_f28/buy_panel_f28.png`;
- `runtime/shop_f28/controlled_shop_trace.txt`.

El constructor acumulativo `F28_SOURCE/scripts/build_phase13BG_F28.py` reproduce SHA-256 `1936a7ea0e1a254f07ee4a2aeb3c293c95c6b4b63acb215fad18c740662fc3b4`, checksum WonderSwan `9932`. Solo difieren de F27 ocho bytes del campo y un byte de checksum. El BPS JP→F28 es directo, SHA-256 `9b010c1c892b83b0a37064b931fe37c939ed6412444f8b06556abdff763effac`, y su aplicación produce una ROM byte idéntica al build.

La prueba fría adicional no llegó al cuadro objetivo dentro del límite operativo y no se repitió; no aporta evidencia positiva. La ejecución F28 desde el guardado válido, la reconstrucción exacta, el rango binario cerrado y el BPS round-trip sí pasan.

## Magic: objetivo de acceso reducido

La escena comercial `0074` contiene el comando `0014/0032` en `0x1B8FA0`, claves `0200/0304`. Su región `CAD3=0074` y la región Fire `CAD3=007E` son ambas 4×4 y no tienen sustituciones condicionales. El movimiento vertical estándar del mapa suma `000A`; por ello `0074 + 000A = 007E`. Esta vecindad reduce la búsqueda: un comercio está en la región inmediatamente anterior de la cuadrícula. No demuestra que el borde sea transitable ni que el checkpoint actual pueda llegar allí; la adquisición natural de Fire permanece abierta.

## Estado

La tienda pasa de `OPEN` a `PARTIAL_OPEN`: ya tiene diálogo, selector y panel de compra válidos en ejecución controlada, además de la corrección visual F28; faltan navegación natural, venta, reparación y una transacción funcional completa. Magic continúa `PARTIAL_OPEN`. La matriz queda en **3 PASS, 3 PARTIAL_OPEN y 1 OPEN**. I11 continúa y quedan **cuatro etapas incompletas: I11–I14**.
