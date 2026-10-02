# I11-P12 — traducción gráfica del encabezado Magic (F27)

Fecha: 2026-09-26. Se corrigen los dos glifos japoneses dorados del encabezado Magic por **Magic** en inglés. F27 SHA-256 `641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4`, checksum `99B2`. ROM japonesa original SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`.

## Origen y diseño

La traza de escritura registró `A000:259A/25CF` cargando el bloque de tiles que incluye el encabezado desde Bank `0x30`, recurso físico `0x3096FE` con fuente comprimida a partir de `0x309707`. `A000:254C` decodifica 119 operaciones en 14.336 bytes; el bloque reconstruido coincide con los 18 tiles de vídeo del encabezado. El descriptor del recurso índice 2 está en `0x308422` (valor `0258`).

Se extrajeron los píxeles de `Magic` ya dibujado por la fuente nativa en la barra inferior de la captura F26: cinco celdas de 12 píxeles, `x=8–67`, `y=129–138`. Se trasladaron a la cabecera `y=2–11` con el índice dorado `0xB` y se limpió la celda final `x=68–79`. El mapa de tiles y el patrón de fondo permanecen originales. La inspección directa de F27 muestra **Magic** completo y legible, alineado en el espacio nativo, con `Fire` y `Shoots fireball.` intactos. La prueba RAM y el resultado ROM F27 producen imágenes idénticas para esa pantalla.

El recurso recomprimido ocupa 589 bytes en relleno `FF` `0x30F13E–0x30F38A`; solo su descriptor cambia a `0DA0`. El recurso japonés original, los demás descriptores, código y banco de fuente quedan intactos. La comparación F26→F27 en el checkpoint controlado encuentra 203 píxeles cambiados dentro de `x=8–79,y=2–12`; el menú previo es idéntico. Arranque frío F27 muestra el título válido. La condición Magic sigue siendo controlada (`0070` y `0230` temporales), por lo que no se convierte la superficie en PASS natural.

## Reproducción y compuertas

`F27_SOURCE/` contiene la fuente acumulativa F26, activo nativo, códec, constructor F27 y `BUILD.bat`. Con la ROM japonesa identificada, `BUILD.bat ROM_ORIGINAL.wsc -o F27.wsc` produce el hash anterior. El BPS acumulativo `patches/StarHearts_EN_phase13BG_F27_CUMULATIVE_2026-09-26.bps` aplica directamente sobre la japonesa y produce bytes idénticos al constructor; SHA-256 del BPS `944e86f468d0e0648a5131bb89d49a4aa27f3803fb374326ef7a3a0f05e94417`. No se distribuye ROM comercial.

I11 conserva 3 superficies `PASS`, 2 `PARTIAL_OPEN`, 2 `OPEN`. El encabezado inglés y la muestra de descripción están validados en ruta controlada; falta aprendizaje natural de hechizo, tienda real, Link natural y el denominador visual de ancho. G12 se apoya en las dos partidas F26 y en el aislamiento del cambio gráfico; la regresión global I13 sobre F27 sigue pendiente. Quedan I11–I14, cuatro etapas incompletas. Ahorro exacto de tokens: `NOT_MEASURED`.

El encabezado era un recurso gráfico fuera de las 237 ocurrencias textuales del censo I10. Su corrección no cambia ese denominador ni convierte la auditoría de japonés gráfico restante en una aprobación global.

Evidencia acotada: `runtime/magic_header_f27/` (título, Magic, confirmación, parámetros y primeros accesos por tile), dos scripts de traza/diseño y manifiesto F27. Las capturas redundantes y ROM privada se excluyen.
