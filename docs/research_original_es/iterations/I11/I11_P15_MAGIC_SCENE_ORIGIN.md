# I11-P15 — índice de escena del evento Fire

Fecha local: 2026-09-26. F27 SHA-256 `641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4`. Sin cambio binario. Una superficie: Magic. Tres métodos acotados: desensamblado de la búsqueda nativa, lectura estructural de la tabla y encuesta de checkpoints. Un intento adicional de observar la búsqueda mientras avanzaba el checkpoint First Trial no alcanzó su precondición en 180 cuadros y se descarta como prueba positiva.

## Procedencia de `0x1BB9B8`

`9000:3A20` toma el índice global de escena en `CAD7` y selecciona Bank `DB` cuando `0060≤CAD7<0094`. Para `CAD7=007E`, el índice local es `001E`. El selector `A000:2530` interpreta la cabecera del banco: 52 entradas (`0034`), tamaño de cabecera `006A`, puntero `169A` para el índice `001E`; `006A + 8×169A = B53A`. El inicio físico de la tabla es `0x1BB53A`.

`9000:3A86` compara dos claves de 16 bits por fila y suma el desplazamiento relativo de la tercera. La tabla `0x1BB53A` contiene 44 filas (`002C`). La fila 13 (base cero) tiene claves `0300/0305` y desplazamiento `0256`, de modo que el script comienza en `0x1BB790`. La siguiente entrada distinta empieza en `0x1BBBEE`. El comando `0012/0160` de P14 está en `0x1BB9B8`, dentro de ese tramo (`+0228` desde el inicio). Por tanto, el destino normal de búsqueda es **escena `007E`, claves `0300/0305` → script `0x1BB790` → adquisición `0x1BB9B8`**. Las claves se conservan como claves internas; no se infiere de sus valores un NPC, coordenada o acción del jugador.

## Alcance de los guardados disponibles

`runtime/magic_scene_index/available_checkpoint_scenes.tsv` resume una lectura de diez cuadros en cada uno de los siete savestates privados disponibles. Los índices `CAD7` observados fueron `0000` en seis y `0005` en First Trial; ninguno era `007E` al medirlo. En una prueba con A sobre First Trial durante 180 cuadros no se alcanzó `9000:3A20`; no hubo resolución dinámica controlada de `007E` y no se reutiliza el ensayo. Esto **no prueba** que la escena sea inaccesible jugando, solo que los checkpoints existentes no la sitúan ya en ejecución.

La entrada estructural concreta reduce la búsqueda natural a la escena `007E` y la interacción que produzca las claves `0300/0305`. Aún falta llegar a ella con una partida válida, aprender Fire y comprobar la pantalla y función sin redirecciones. No se suma PASS: I11 conserva 3 `PASS`, 2 `PARTIAL_OPEN`, 2 `OPEN`; quedan I11–I14, cuatro etapas incompletas. Tienda, Link y denominador visual de ancho siguen abiertos. Ahorro exacto de tokens: `NOT_MEASURED`.
