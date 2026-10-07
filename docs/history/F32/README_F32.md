# F32 — e-Pet y descripción compartida

Estado: EXPERIMENTAL_INTERNAL_TEST / RC_NOT_AUTHORIZED. Idioma: inglés.

Entrada JP: 4.194.304 bytes, SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`.
Salida F32: SHA-256 `8b7afc0975bdaa91c25aad5b9b5aa722af310421db472bbc917752432ebdbc7a`, checksum `3D99`.

Procedimiento probado en Linux con Python 3, sin BAT:

```bash
python3 scripts/build_phase13BG_F32.py /ruta/JP.wsc -o /ruta/F32.wsc --bps /ruta/F32.bps
```

Incluye toda la cadena de fuentes JP→F32 y los assets necesarios. El usuario solo aporta JP; no necesita ROMs ni parches intermedios. No incluye hooks de avance sintético. Los replays diagnósticos están separados del build.

Para regenerar únicamente los gráficos con Pillow:

```bash
python3 scripts/build_epet_labels.py /ruta/F31.wsc assets/F32/native_latin_atlas.png /ruta/assets_regenerados
```

El atlas procede del renderer CP932 nativo. Se mantienen sus píxeles y posiciones verticales; solo se elimina margen horizontal vacío para componer los rótulos. No se altera la fuente ni el renderer compartido. El formato numérico original se conserva; los valores elementales se desplazan cuatro píxeles a la derecha en la ficha e-Pet.

Se traducen 22 rótulos gráficos (19 textos únicos), más una descripción compartida por 20 entradas de la tabla de 161 slots. Ver el informe I14-P6 para capturas, abreviaturas y límites. Los wrappers históricos son auxiliares; no se ejecutó ni se exige BAT en esta etapa por instrucción del usuario.
