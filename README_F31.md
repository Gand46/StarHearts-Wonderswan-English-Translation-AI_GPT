# F31 — diez encabezados y etiqueta Def

Entrada: JP original SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`.
Salida F31: `fbf949271412eb023cb94765782126a689eead61e8c6a56b2a12b85ed23acd52`, checksum `4EA7`.

El constructor conserva la cadena completa de fuentes JP→F30 y aplica las once correcciones F31. Emite ROM local y BPS directo JP→F31. No integra el hook de acceso sintético P4.

Windows: `BUILD.bat "ruta\original.wsc" -o F31.wsc`

Linux: `./build.sh /ruta/original.wsc -o F31.wsc`

macOS: `sh build.command /ruta/original.wsc -o F31.wsc`

Requiere Python 3. El constructor y su BPS se ejecutaron en Linux; los wrappers Windows y macOS no se ejecutaron en sus sistemas nativos. `--bps ruta.bps` permite elegir la salida del parche. Los archivos originales se verifican por hash; no se sobrescriben deliberadamente.

Los recursos binarios necesarios están incluidos. Para regenerar sus píxeles desde F30 y la captura nativa, con Pillow instalado:

```text
python scripts/build_menu_header_assets.py F30.wsc carpeta_de_salida assets/native_shop_labels_reference.png
```

La reproducción de assets no usa tipografías externas. Las máscaras del encabezado inglés previo Arms/Charms coinciden exactamente con la captura de referencia. El generador reutiliza esos píxeles y sus métricas; e-Pet reutiliza además el guion del recurso original.

`phase13BG_F31_changes.json` define preimágenes, rangos y hashes. El detalle de pruebas y límites está en `../I14_P5_F31_TRANSLATION_AND_VALIDATION.md`. Estado: **EXPERIMENTAL_INTERNAL_TEST / RC_NOT_AUTHORIZED**. Las seis evidencias reales pendientes no se sustituyen por estos accesos de diagnóstico.
