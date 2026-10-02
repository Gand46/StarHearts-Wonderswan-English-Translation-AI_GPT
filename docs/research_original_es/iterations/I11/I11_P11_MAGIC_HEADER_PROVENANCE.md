# I11-P11 — procedencia gráfica del encabezado Magic

Fecha: 2026-09-26. F26 intacta, SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`; checksum `6ABA`. Mismo checkpoint de origen natural P10 y dos bits SRAM temporales (`0070`, `0230`); sin guardar modificaciones. Cuatro métodos diagnósticos acotados, una superficie (Magic), sin repetir la evaluación visual de Fire.

## Hallazgo de diseño

La captura P10 mostraba dos glifos japoneses dorados en la parte superior. Se localizaron en las cajas de píxeles `x=8–19,y=2–12` y `x=68–79,y=2–12`. Un volcado de la memoria de vídeo antes/después de abrir Magic encontró cambios en el mapa de tiles `0x3800` y en el área gráfica `0x8000`. Anular temporalmente la fila superior del mapa `0x3800–0x383F` modificó únicamente la mitad superior de esa franja; el resto del encabezado siguió visible en la siguiente fila. Anular por separado 32 bytes en `0x8020` alteró `x=9–15,y=2–7`, y en `0x8040` alteró `x=16–19,y=3–7`. Se prueba así el consumo de esos tiles por el **primer glifo visible**, no su origen físico en ROM ni el segundo glifo completo.

Una traza de lecturas físicas durante la entrada Magic registró bloques Bank `0x30` en `0x308400–0x308B80` y `0x3096E0–0x309840`, además de la tabla Bank `0x36` `0x364480–0x3645A0`; esas direcciones son candidatos de recursos y del flujo de pantalla, pero aún no se ha vinculado un byte ROM específico a cada tile dorado. La ausencia de lecturas de cadenas `魔法` contiguas en P10 no prueba que el gráfico no tenga texto japonés. Una variante privada cambió `0x3645B8` de `82 6D` (`N`) a `82 60` (`A`) con checksum recalculado: cambió el rótulo inferior `None`, mientras el encabezado quedó igual. Esa dirección se descarta como origen del encabezado; la variante ROM privada no se distribuye.

## Decisión

No se sustituyen tiles ni tipografía sin localizar el recurso y demostrar el alcance de su reutilización. El encabezado sigue en japonés y Magic conserva `PARTIAL_OPEN`; la muestra `Fire`/`Shoots fireball.` de P10 sigue legible solo bajo control. No hay nuevo PASS, F26/BPS permanecen intactos. La próxima prueba distinta debe enlazar las escrituras de tiles de `0x8020/0x8040` con su flujo de descompresión y el recurso ROM, después proponer un rótulo inglés compatible con la disposición nativa y validar cada glifo visualmente. Tienda, Link y denominador visual de ancho siguen pendientes. Quedan I11–I14: cuatro etapas incompletas.

Evidencia reducida: `runtime/magic_header_provenance/rom_reads.tsv` (367 bloques de 32 bytes leídos), `top_row_zero_controlled.png` y `provenance_summary.json`; capturas íntegras P10 en `runtime/magic_unlock/`. Scripts `runtime/scripts/i11_p11_magic_video_snapshot.lua`, `i11_p11_magic_rom_provenance.lua` e `i11_p11_tilemap_causality.lua`. Los volcados binarios, la ROM de prueba y las capturas equivalentes permanecen privados. Ahorro de tokens: `NOT_MEASURED`.
