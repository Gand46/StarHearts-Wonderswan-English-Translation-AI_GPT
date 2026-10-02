# I11-P10 — consumidor de Magic, muestra de ancho y encabezado pendiente

Fecha: 2026-09-26. F26 intacta, SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`, checksum `6ABA`. Un solo checkpoint de origen natural; escrituras SRAM exclusivamente diagnósticas, no persistidas.

## Corrección de la clasificación P9

La captura antes de la escritura muestra el campo. `C0F2&0040` abre el **menú principal** por `A000:3A90`; el ensayo P9 terminó en ese menú con `Magic` seleccionado, no en una tienda. `A000:404C` despacha sus categorías. `A000:3CAE` construye la máscara `CA80` de disponibilidad del menú. P8/P9 atribuyeron erróneamente los IDs `0230`/`0252` a tienda; `0230` pertenece al grupo que habilita Magic. Las lecturas Bank 37 observadas en la rama Link de P8 no prueban un panel de tienda. La ruta natural de tienda sigue sin identificar. Los informes históricos llevan nota de rectificación.

## Prueba de la condición Magic

`A000:3CAE` prueba primero el ID `0070` por el comprobador genérico `9000:3BD0`; si falta, salta el grupo `0230–0251`. Si existe un hechizo de ese grupo, activa el bit `8000` en `CA80`. El checkpoint tenía `0070=00`, `0230=00` y, tras abrir el menú sin alteraciones, `CA80=24C4`. Con solo los bits correspondientes en SRAM `0030` y `0068` activados temporalmente, la misma entrada normal abrió el menú con `CA80=A4C4`.

Al confirmar Magic mediante entrada normal, la ejecución alcanzó `A000:46E0` y `A000:48C8`; se leyó una vez cada puntero Bank `0x38` para el nombre `Fire` (`0x38664C`) y la descripción `Shoots fireball.` (`0x386806`). La pantalla muestra ambos textos completos y legibles, con la tipografía del juego. `Shoots fireball.` es la muestra I02 de 16/16 glifos; esta lectura aprueba **solo la legibilidad controlada de esa muestra**, no el denominador de ancho máximo ni el aprendizaje natural del hechizo.

La misma pantalla conserva dos glifos japoneses en el encabezado superior. Una búsqueda de lecturas de las 16 cadenas `魔法` preservadas en Bank `0x38` no obtuvo hits durante la apertura; el origen del encabezado no quedó identificado. No se edita a ciegas ni se declara PASS visual de la superficie.

Evidencia reducida: `runtime/magic_unlock/initial.txt`, `menu.txt`, `magic.txt`, `description.txt`, `baseline_magic_route.txt`, `header_reads.txt`, `magic_selected_controlled.png` y `magic_confirmation_controlled.png`. Scripts `runtime/scripts/i11_p10_magic_route_trace.lua` e `i11_p10_magic_unlock_probe.lua`. Las capturas vacías y equivalentes quedan fuera.

## Compuertas

I11 conserva 3 superficies `PASS`, 2 `PARTIAL_OPEN`, 2 `OPEN`. Magic necesita una fuente natural del ID `0070` y del hechizo, además de corregir y revisar el encabezado. `G06_WIDTH` sigue parcial pese a una muestra controlada legible. Tienda y Link continúan abiertas; G12 persistencia permanece PASS. Quedan I11–I14 (cuatro etapas incompletas). La próxima tanda debe rastrear el recurso gráfico o de texto del encabezado con evidencia de origen, o elegir otra ruta natural verificable; no repetir la activación equivalente de ambos bits.
