# Fuente acumulativa Star Hearts 13BG-F30

Este directorio conserva la fuente acumulativa completa de F29 y añade la corrección F30 de dos etiquetas monetarias de tienda. No incluye ROM comercial.

En Windows:

```bat
BUILD.bat "Star_Hearts_JP_ORIGINAL_REFERENCE.wsc" -o "StarHearts_EN_phase13BG_F30.wsc"
```

En Linux/macOS puede ejecutarse `python scripts/build_phase13BG_F30.py ROM_ORIGINAL.wsc -o F30.wsc`. Se exige la ROM japonesa SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`. El resultado esperado es SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, checksum WonderSwan `9487`.

La prueba runtime del consumidor real demostró que los campos de ocho celdas `BUYPRICE` y `REPAIR` se leen completos, pero el panel sólo muestra los dos primeros glifos (`BU` y `RE`). F30 conserva los campos de 18 bytes y usa `BP` (buy price) y `RP` (repair price), seguidos por espacios nativos. Ambos rótulos quedan completos y distinguibles en su viewport original.

La validación usa los eventos nativos `0014/0031` para venta y `0014/0030` para reparación. La entrada natural a un mercader todavía no está demostrada y no se declara cerrada.
