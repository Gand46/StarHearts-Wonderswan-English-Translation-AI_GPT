# Fuente acumulativa Star Hearts 13BG-F29

Este directorio conserva la fuente acumulativa completa de F28 y añade la corrección F29 del selector de categorías de venta. No incluye ROM comercial.

En Windows:

```bat
BUILD.bat "Star_Hearts_JP_ORIGINAL_REFERENCE.wsc" -o "StarHearts_EN_phase13BG_F29.wsc"
```

En Linux/macOS puede ejecutarse `python scripts/build_phase13BG_F29.py ROM_ORIGINAL.wsc -o F29.wsc`. Se exige la ROM japonesa SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`. El resultado esperado es SHA-256 `4704a7d4e06696455ac6017632135c03259e42783f7af095b0231246e754eadb`, checksum WonderSwan `9639`.

F28 todavía mostraba `装備アイテム`, `武器`, `防具`, `タリスマン` y `アミュレット` al elegir `SEL`. F29 repunta únicamente ese recurso comprimido y muestra `Gear Items`, `Arms`, `Armor`, `Charms` y `Amulets`. Los píxeles provienen de una captura inglesa del propio juego incluida en `assets/native_shop_labels_reference.png`; no se usa una fuente externa. `scripts/build_sell_category_resource.py` reproduce el recurso `assets/sell_category_resource.bin` desde F28 y esa referencia.

El BPS acumulativo distribuido aplica directamente desde la ROM japonesa. La entrada natural a un mercader, una venta completa y las superficies `BUYPRICE`/`REPAIR` siguen pendientes de validación.
