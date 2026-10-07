# Fuente acumulativa Star Hearts 13BG-F27

Este directorio contiene las fuentes heredadas completas F26 y la corrección gráfica F27. No incluye ROM comercial.

En Windows:

```bat
BUILD.bat "Star_Hearts_JP_ORIGINAL_REFERENCE.wsc" -o "StarHearts_EN_phase13BG_F27.wsc"
```

También puede ejecutarse `python scripts/build_phase13BG_F27.py ROM_ORIGINAL.wsc -o F27.wsc` en Linux/macOS. Se exige SHA-256 de la ROM japonesa `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`. El constructor reproduce F26 con su fuente acumulativa, valida su hash, reemplaza el recurso comprimido de Magic y verifica F27 SHA-256 `641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4` y checksum `99B2`.

`assets/magic_header_tiles.bin` contiene solo los 18 tiles modificados. `assets/native_magic_reference.png` y `scripts/build_magic_header_tiles.py` documentan su procedencia en la fuente nativa de F26; Pillow se necesita únicamente si se desea regenerar ese activo. El build ordinario usa el binario verificado y no requiere Pillow.

El BPS distribuido en `../patches/` aplica **directamente** desde la ROM japonesa. La prueba de aplicación byte a byte se documenta en `../I11_P12_MAGIC_HEADER_F27.md`.
