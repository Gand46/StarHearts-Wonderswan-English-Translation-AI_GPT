# Fuente acumulativa Star Hearts 13BG-F28

Este directorio conserva la fuente acumulativa completa de F27 y añade la corrección F28 de la etiqueta de cantidad poseída de la tienda. No incluye ROM comercial.

En Windows:

```bat
BUILD.bat "Star_Hearts_JP_ORIGINAL_REFERENCE.wsc" -o "StarHearts_EN_phase13BG_F28.wsc"
```

En Linux/macOS puede ejecutarse `python scripts/build_phase13BG_F28.py ROM_ORIGINAL.wsc -o F28.wsc`. Se exige la ROM japonesa SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`. El resultado esperado es SHA-256 `1936a7ea0e1a254f07ee4a2aeb3c293c95c6b4b63acb215fad18c740662fc3b4`, checksum WonderSwan `9932`.

F27 almacenaba `OWNED` en un campo de ocho celdas, pero el consumidor real de la tienda dibuja solo las dos primeras. F28 usa `NO` más seis espacios nativos; la captura runtime muestra ambos glifos completos junto al contador. El BPS acumulativo distribuido aplica directamente desde la ROM japonesa.
