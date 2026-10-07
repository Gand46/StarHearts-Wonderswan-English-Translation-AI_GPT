# F33 — epílogo legible / aceptación sintética

Requiere Python 3 y ROM JP SHA 64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_phase13BG_F33.py /ruta/JP.wsc -o /ruta/F33.wsc --bps /ruta/JP_to_F33.bps
```

Reconstruye F32 y abrevia tres líneas del epílogo demostradas demasiado anchas en el consumidor nativo. Nuevas líneas: «was a messenger of stars.», «in the Inde homeland,» y «ruled by Oser, world savior,». Se conserva el significado, slots, primeras líneas, CR/LF y terminadores. No cambia fuente, diccionario, punteros ni integra acceso sintético; este solo vive en un fixture de diagnóstico separado. Manifest: phase13BG_F33_changes.json.

Los BAT y scripts anteriores son históricos. Para F33 usar el comando Python anterior; sin BAT/cmd/Wine.
