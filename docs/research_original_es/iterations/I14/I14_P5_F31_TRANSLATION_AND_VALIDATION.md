# I14-P5 — once correcciones integradas en F31

Fecha técnica UTC: 2026-09-28. Paquete 1.36. `RC_NOT_AUTHORIZED`.

## Resultado y alcance

Se corrigió el defecto HIGH `DEFECT-I14P4-01` y se amplió la revisión al mismo grupo gráfico. **Diez encabezados gráficos y una etiqueta dinámica** se traducen en F31. No es un nuevo cierre del universo del juego. Tienda natural, Fire/Magic natural, Holy Temple tardío, ending, credits y Link válido siguen pendientes.

| Japonés | F31 | Evidencia |
|---|---|---|
| 武器 | Arms | Panel nativo de reparación, entrada al mapa sintética |
| 防具・護符 | Armor/Charms | Menú nativo de armadura, inventario diagnóstico |
| 防具 | Armor | Reparación nativa de armadura, inventario diagnóstico |
| 防 | Def | Valor 1 y límite de campo 99 legibles, Dur conservado |
| 動物の能力 | Animal Powers | Encabezado mediante cargador nativo controlado |
| 装備アイテム | Gear Items | Encabezado mediante cargador nativo controlado |
| タリスマン | Charms | Terminología SELL F29; encabezado controlado |
| アミュレット | Amulets | Encabezado controlado |
| 妖精リスト | Skills | Se conserva el rótulo funcional del menú inglés existente; no se valida todo el sistema de habilidades |
| e-ペット | e-Pet | Solo encabezado; función e-Pet no validada |
| 奥義リスト | Secret Skills | Encabezado controlado |

Cuatro cambios se leen en sus paneles nativos, con las modificaciones de estado declaradas. Los otros siete se comprobaron con selección de recurso en el cargador nativo; eso demuestra consumo, glifos y legibilidad del encabezado, **no la disposición completa ni funcionamiento de esas siete funciones**. La matriz de traducciones conserva esta diferencia.

## Causa y corrección

El menú de reparación consume la tabla gráfica `30841C`, índice 4 (`309A56`). La traza registra la lectura del descriptor `308426`; los tiles de vídeo `8020/8040/8060/8080` coinciden con el frame 4 original. Los pares 2/3, 4/5 y 6/7 contienen Armor/Charms, Arms y Armor. Se reconstruyeron estos pares; los frames 0/1/8/9/10 permanecen idénticos tras decodificar.

Los otros siete encabezados son los índices 3, 5, 7, 8, 11, 12 y 13 de la misma tabla. Solo cambian los píxeles de `x=8..87,y=0..15` de su frame gráfico. Las otras regiones y frames se compararon byte a byte al decodificar. Los índices 0/1/2/6/9/10/14/15 permanecen idénticos.

e-Pet no admitía el recurso reconstruido dentro de su espacio. Su primera paleta se reubicó en `30FB8E`, verificado como relleno FF; sus bytes y las otras tres paletas permanecen idénticos. Se actualizó únicamente el offset interno correspondiente. No se sobrescribió el recurso siguiente.

La etiqueta 防 se construía con una instrucción en `3A69FE`. F31 usa un CALL local a `3AFF00`, una zona FF verificada, para escribir `Def` en CP932 y continuar el formateador numérico original. El cambio no modifica inventario, daño, defensa, fondos, eventos o transiciones. La prueba diagnóstica de valor 99 verifica la separación respecto a Dur.

Se conservó la fuente nativa: las máscaras del encabezado Arms/Charms previo y la captura del menú coinciden exactamente, píxel a píxel. Las demás palabras proceden de esa misma captura. Para e-Pet se ensamblaron los glifos nativos e/P/e/t y el guion original. No se usaron fuentes genéricas, OCR como aprobación ni imágenes generadas.

## Validación realizada

- Build nuevo JP→F31 desde fuentes acumulativas; no se repitió la auditoría técnica cerrada de F30.
- BPS directo JP→F31 aplicado por un lector independiente, identidad exacta y checksum `4EA7`.
- 4.350 bytes distintos frente a F30, todos en los rangos previstos; cero cambios inesperados. Los hooks de warp P4 no están integrados.
- Casos negativos: JP incorrecta, BPS truncado y BPS corrupto rechazados.
- Lectura visual de Arms, Armor/Charms, Armor, Def 1 y Def99 en sus paneles nativos. Los controles de armadura siembran WRAM `C63C=00D0` y `C646=0001`; el valor 99 fuerza solo el registro de salida del cálculo para probar anchura.
- Lectura visual de los otros siete encabezados mediante el cargador `A000:2530`, sustituyendo el índice 2 de Magic por el recurso solicitado. No se presenta esa vista como menú auténtico del sistema objetivo.
- La vista diagnóstica e-Pet contiene artefactos fuera del encabezado por incompatibilidad de ese recurso con la pantalla Magic usada como soporte. Un control idéntico sobre F30 reproduce esos artefactos: **cero píxeles distintos fuera del encabezado**. No se afirma PASS visual de la función e-Pet completa.
- Magic/Fire sobre F31 conserva una captura idéntica a la aceptada en P4: cero píxeles distintos. No se repitió su adquisición ni se convirtió el checkpoint sintético en natural.
- No se repitieron G12, el diferencial F26→F30 ni las ramas fallidas ending/Link. No se ejecutó BUILD.bat: el host no dispone de cmd/Wine. La fuente del wrapper apunta a F31.

## Procedencia y reproducción

`runtime/p5/PROVENANCE.json` relaciona cada ejecución, script, hash ROM y checkpoint. El acceso a reparación reutiliza el checkpoint P4 de mapa cargado; Magic reutiliza el checkpoint posterior a la entrega nativa de Fire. Todos esos descendientes conservan clasificación sintética.

En el paquete privado, `PRIVATE_CHECKPOINTS/` se sitúa fuera de la carpeta de fuentes distribuibles. Incluye el origen F18 y dos checkpoints P4 reutilizables, con hashes y límites. No se incluye ROM comercial, BIOS ni SRAM independiente. No redistribuir los checkpoints como evidencia de avance natural.

`runtime/p5/REPRODUCE.md` contiene comandos y matrices. La captura y las trazas son evidencia del alcance declarado; el PASS del validador del paquete significa coherencia de registros, no traducción global terminada.

## Pendientes

Se mantienen los cinco playtests reales y Link con hardware/peer soportado. Las siete funciones cuyos encabezados se revisaron de forma aislada necesitan todavía entrada propia y revisión integral cuando exista un estado apropiado. No se encontraron nuevos defectos confirmados sin corrección dentro de este lote; no se declara cero japonés en toda la ROM ni un porcentaje global.

El siguiente trabajo útil requiere condiciones concretas del encuentro tardío Holy Temple o un consumidor/checkpoint terminal; no repetir 01DE ni los mismos eventos inyectados como sustituto. La lectura completa de funciones avanzadas puede aprovechar los nuevos recursos y scripts, con máximo dos métodos o 40 minutos por rama. Ahorro exacto de tokens: `NOT_MEASURED`.
