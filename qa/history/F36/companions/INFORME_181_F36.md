# Cierre de consumidor e integración de los181 campos — F36

Se resolvieron los181 consumidores antes desconocidos: son nombres iniciales de actor, no identificadores inertes. Se integraron181 traducciones y las181 pasaron lectura y copia en el handler nativo de Mesen sobre F36. No quedan consumidores UNKNOWN en este universo. Además se descubrió y corrigió un operando0022 japonés fuera del censo181.

F35: `6198444ae2e18467c7fd2c44eb8d32888b662ba06a35625cdf3282ecd7e16084`.
F36: `da2966870ef022e68f84e07ead6d017a686c47f55a6036f57974c57c6d4578d2`.

## Cadena probada

Cada campo empieza ocho bytes después de opcode0004. Sus seis bytes previos son dos claves de actor y un ID. Handler3931F8 llama390EDA y avanza26bytes de operandos. El nombre ocupa16bytes; los cuatro siguientes son metadatos y no se modifican.

-180casos: rama397348, copia de8words en3973C8 desdeES:SI+6 aactor+62.
-1caso, Belphego ID00AF: rama391F30, misma copia en391FA6.
-El puente39E929 toma actor+62 y lo pasa a3AB7DE, renderer nativo limitado a8glifos.
-Las16posiciones de bytes permiten8CP932 fullwidth; si el nombre es menor, se rellena con cero. No se escribeASCII ni MTE en este búfer. Un nombre de8glifos exactos no necesita terminador adicional: el renderer tiene límite8 y la estructura no dispone de un17.ºbyte para texto.

**Identidad independiente de proximidad:**164registros tienen ID01E0..027F y apuntan a los160nombres canónicos Bank38 mediante `slot=386B60+2*(ID−01E0)`. La resta y tabla están demostradas en394228 y39424A. En todos164, el japonés canónico es prefijo exacto del campo inicial. Se tomó el inglés ya resuelto de esa tabla; cinco nombres largos usan la forma de ocho glifos aprobada enI02. No se eligió automáticamente el siguiente hablante0022.

Los17restantes están enumerados en`exceptions_17.csv`. Se usaron coincidenciasJP exactas del glosario, la identidad deTirawaka ID0014 y revisión editorial explícita:ジムス→Jimusu (noJim/ジムハ niPergypt Soldier),えいへい→Guard (no????),ポコ→Poco (grafía existente en diálogo/misión). Root aprobó el mapeo completo antes de insertar.

## Prueba que refuta la invisibilidad

El evento iniciado en19580E, con claves de su actor seleccionadas, muestra enF35 el nombre japonésティラワカ junto al diálogo inglés antes de llegar al0022. La traza registra el renderer con ese búfer a cuadro649;0022 no lo reemplaza hasta842. La captura `runtime/screen.png` conserva el japonés. EnF36, la misma ruta y cuadro800 muestra **Tirawaka**, ocho glifos nativos completos y legibles dentro de su marco.

La selección de evento, claves y estado es **SYNTHETIC_NATIVE_EVENT_COROUTINE / WRAM_POKE**, desde`P4_repair_synthetic_entry.mss`; no prueba acceso natural. No se alteró ROM durante estas pruebas. La existencia de sobrescrituras0022 en otras rutas no convierte el campo inicial en inerte.

## Resultado medido sobre F36

| Control | Resultado |
|---|---|
|Precondición F35 y16bytesEN F36|181/181PASS|
|Opcode, claves, ID y cuatro metadatos vecinos preservados|181/181PASS|
|Copia nativa real:8lecturasword y16bytes finales exactos|181/181PASS|
|Ramas ejecutadas|180por973C8;1por91FA6|
|Nombre inicial renderizado y revisado individualmente|Tirawaka,1/181|
|Familia visual compartida|RepresentativaPASS; Tirawaka8, Belphe yTiraw|
|Recorrido natural de181eventos|NOT_VALIDATED|
|Captura individual de181nombres iniciales|NOT_VALIDATED; no se declara181/181visual|

En la capturaBelphego, el handler alternativo copia **Belphego** íntegro; el script luego ejecuta su0022 ya traducido y el renderer muestra **Belphe**, la abreviatura previa. Esa captura no se presenta como una imagen del valor inicialBelphego.

## Hallazgo extra fuera181

En1B7D30 existe un0022 real cuyo operando1B7D32 eraティラワカ, seguido directamente por001C003C; no coincide con la gramática estrecha `0022 … 0021 0000` del censo previo. Se integró **Tiraw** en los mismos10bytes, conservando001C003C. La trazaF36 ejecuta3564 conSI7D32 a cuadro511 y3AB7DE conTiraw a587; la captura confirmaTiraw. No sumar este operando al denominador181.

## Reproducción y límites

`python validate_f36.py F35.wsc F36.wsc --evidence CARPETA` verifica manifiesto, metadatos yCSVde lectura nativa.

Para repetir las181copias, crearOUT y ejecutar con rutas absolutas:

```bash
OUT=/salida BASESTATE=/privado/P4_repair_synthetic_entry.mss \
TARGETS=/evidencia/targets.lua EXPECT=after \
LD_PRELOAD=/usr/lib/x86_64-linux-gnu/libstdc++.so.6 \
timeout 45 /Mesen --testRunner --doNotSaveSettings \
--debug.scriptWindow.allowIoOsAccess=true --timeout=35 \
/evidencia/trace_all_copies.lua /F36.wsc
```

`probe.lua` repite las capturas conOFFSET195816,1D93C8 o1B7D0A ylas mismas variablesOUT/BASESTATE; la ROM especificada determinaF35/F36. Usa una copia aislada deMesen2.1.1, settings.jsonvacío, límite850frames. Las advertencias de memoria no inicializada del emulador no se toman como aprobación; se exigió ejecución del handler, lecturas, igualdad exacta y revisión de las capturas.

El primer intento de lote restauraba savestate desdeendFrame y terminó tras un registro; se descartó. El lote definitivo reinicializa el fixtureWRAM y utiliza la coroutine nativa para cada caso; contiene181filasPASS. Los intentos fallidos no forman evidencia positiva.

Este cierre resuelve el universo181 y el extra explícito. No declara fin global de traducción, cobertura total delCFG ni aprobación visual individual de181eventos. No reabre los demás censos. Ahorro de tokens:no medido.
