# I11-P16 — región de Fire y entrada nativa del comercio

Fecha: 2026-09-27. F27 SHA-256 `641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4`. Sin cambio binario. Dos superficies (Magic y tienda), dos métodos estructurales distintos; no se repitieron recorridos de Wampa, Link ni capturas controladas de Magic. La sonda reproducible `runtime/scripts/i11_p16_map_shop_sources.py` y su salida `runtime/p16_map_shop/structural_trace.json` comprueban los bytes y las relaciones indicadas.

## Magic: región física del evento

`9000:63F6` indexa la tabla de regiones del banco `D8` (Bank físico `18`) con `CAD3`; `9000:640B` inicializa `CAD7=CAD3` y solo sustituye ese índice cuando una condición por celda lo requiere. La entrada `CAD3=007E` está en `0x181668`, representa una región de **4×4 celdas** y sus 16 registros tienen cero condiciones. Por tanto, al encontrarse en cualquiera de esas celdas, la selección ordinaria conserva `CAD7=007E`. P15 vinculó ese índice con la entrada `0300/0305` y la adquisición `0160` del script `0x1BB9B8`. La lectura del diálogo anterior al premio apunta narrativamente al espíritu de Fire; no se usa el diálogo para afirmar coordenadas o modo de acceso.

Esta relación concreta el objetivo de navegación: **región `CAD3=007E`**, cualquiera de sus 16 celdas, y luego interacción que genere las claves `0300/0305`. No se conoce desde qué salida o progreso se entra a la región; los guardados disponibles siguen fuera de ella. No se atribuye aprendizaje natural.

## Tienda: diálogo y función de panel

En Bank físico `21`, la secuencia de comercio que comienza en `0x2193FE` presenta el saludo del mercader y las opciones de tres celdas **BUY/SEL** en `0x21942A–0x21943F`. La rama en `0x21944A` referencia `9000:D026`, cuyo primer paso es la llamada lejana a `A000:A4E0` (físico `0x3AA4E0`); esta función llama a `A000:A7C8`. Otra rama de la misma colección, `0x219280`→`9000:CE10`, llama también a `A000:A4E0`. El contexto explícito de compra/venta permite identificar `A4E0` como rutina del panel comercial; rectifica la clasificación **indeterminada** usada durante esta búsqueda, sin revivir las atribuciones erróneas de P8/P9 a Link o al menú principal.

La etiqueta **SEL** ocupa tres glifos en la tabla; no se amplía a `SELL` sin probar la anchura y el recurso correspondiente. Las referencias Bank 37 a `OWNED`, `BUYPRICE` y `REPAIR` conservan su estado anterior: todavía no hay imagen de tienda válida ni transacción natural que demuestre su dibujo. Tampoco se ha hallado qué NPC o evento del mapa llama a este diálogo. La identificación estructural no equivale a un PASS visual ni funcional.

## Compuerta

I11 conserva 3 `PASS`, 2 `PARTIAL_OPEN`, 2 `OPEN`; quedan **cuatro etapas incompletas, I11–I14**. Próximo paso distinto: enlazar el diálogo Bank 21 con el disparador de un mercader accesible en una partida válida y recorrer su compra/venta, o localizar una entrada natural a `CAD3=007E` para comprobar la adquisición y la pantalla Magic F27. Link natural, regresión global F27 y denominador visual máximo siguen pendientes. Ahorro exacto de tokens: `NOT_MEASURED`.
