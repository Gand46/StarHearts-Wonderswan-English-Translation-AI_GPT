# F34 — corrección de calidad visual

```bash
PYTHONDONTWRITEBYTECODE=1 python3 scripts/build_phase13BG_F34.py /ruta/JP.wsc -o /ruta/F34.wsc --bps /ruta/JP_to_F34.bps
```

Requiere la ROM JP SHA-256 64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255 y Python 3. Reconstruye todas las revisiones acumulativas hasta F34.

Corrige dos defectos demostrados: mayúsculas mezcladas del segundo banner y posición del código numérico de LINK ERROR. El banner queda EVENT:First Trial, con el espaciado visual del glifo de dos puntos y sin omitir palabras; conserva el slot de 28 bytes, terminador y motor. El destino del número se ajusta al placeholder ya traducido. No cambia la fuente, el diccionario ni el renderizador compartido.

WAITING P2 conserva ROM y fuente: el defecto de evidencia era una captura durante el desplazamiento. Se documentan una captura estable y reconocimiento aislado de sus nueve glifos, idénticos a la referencia nativa. No se incorpora el prototipo de cambio de colores.

BUILD.bat es histórico; usar el comando Python anterior. Sin BAT/cmd/Wine.
