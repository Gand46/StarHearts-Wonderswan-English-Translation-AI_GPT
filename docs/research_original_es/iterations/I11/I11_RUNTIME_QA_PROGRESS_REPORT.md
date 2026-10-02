# I11 — avance de QA runtime por superficies

Fecha: 2026-09-27  
Estado: `DONE_WITH_DEFERRED_QA`  
Tanda: `I11-P22`  
ROM validada: F30, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, checksum `9487`  
Cambio binario acumulado: sí, F27 Magic, F28 `OWNED→NO`, F29 selector de venta y F30 `BUYPRICE→BP`/`REPAIR→RP`; P20–P22 no cambian F30

## Resultado acumulado

Mesen 2.1.1 funciona en modo headless con `settings.json` junto al ejecutable y `LD_PRELOAD` con la `libstdc++.so.6` del sistema. Esta tanda reutilizó un guardado natural certificado de F15 para comprobar compatibilidad de Continue en F26 y derivó de él un checkpoint de navegación. El guardado, la ROM y los savestates permanecen fuera del paquete.

Pasan con evidencia reproducible, natural o de origen natural documentado:

- boot, título, creación del héroe y confirmación `Blood type A`;
- cuadros de nombre, diálogo de Manny y mensaje breve `Event: First Trial`;
- menú principal, Status y Options;
- Continue frío de compatibilidad F26 desde el guardado certificado;
- equipo/inventario: ficha `Tomahawk`, `Atk 8 Dur 4`, descripción `Inde Village Axe`, confirmación `Equip?` y arma equipada;
- objetos/descripciones: `Save Drum` y `Save Anywhere` en Key Items;
- combate de campo: enemigo presente, movimiento y dos animaciones de ataque visibles.

No se observan cortes, solapamientos, basura ni pérdida de legibilidad en las capturas aceptadas. Cuatro de las siete superficies obligatorias quedan en `PASS`, dos en `PARTIAL_OPEN` y una en `OPEN`.

## Límites y evidencia negativa

- `Magic` permanece deshabilitado en el checkpoint sin cambios. P10 activó temporalmente IDs `0070` y `0230`: `Fire` y `Shoots fireball.` se leen completos, y F27 reemplaza los dos glifos japoneses del encabezado con `Magic` en fuente nativa. La superficie combinada permanece parcial por faltar aprendizaje natural.
- La continuación natural desde First Trial alcanzó Wampa por dos rutas, pero no activó una tienda. Una ruta de tienda desde el checkpoint con inventario obtuvo cero lecturas `OWNED`, `BUYPRICE` y `REPAIR`; se detuvo sin repetir métodos equivalentes.
- Tres variantes de entrada desde el título seleccionaron WonderGate y no Link Cable. La espera/error de Link Cable sigue abierta.
- Las lecturas controladas de `WAITING P2`, `OWNED`, `BUYPRICE` y `REPAIR` demuestran dataflow, pero sus imágenes inyectadas carecen de contexto UI válido y no cuentan como PASS visual.
- P20 cierra el denominador visual de ancho máximo bajo control: el análisis reproducible reduce los 209 operandos en capacidad física a 182 formas únicas y demuestra que el máximo integrado real de ocho glifos solo corresponde a `Kitchiki` y `TradrKid`. Ambos, más `IndiKid`, `Rica`, `Zunt` y `Eldr`, se dibujan mediante la cadena nativa compartida desde un checkpoint de diálogo de origen natural. Las transcripciones directas coinciden; margen mínimo 7 px y cero corte/solapamiento/basura. No se afirma alcance natural de las entidades candidatas.
- P3 separó 31 términos I02 al límite lógico de 209/214 operandos integrados al límite físico, sin convertir el censo estático en PASS visual. Tres nuevas secuencias de título siguieron seleccionando WonderGate; véase `I11_P3_WIDTH_AND_LINK_REPORT.md`.
- P4 identifica `F44F` como selector del título (0 Continue, 1 WonderGate, 2 New Game). El índice sintético 3 dibuja Link Cable, pero la confirmación queda sin interfaz válida. Link continúa OPEN; véase `I11_P4_LINK_SELECTOR_REPORT.md`.
- P5 identifica la máscara `F44E`: `07` en el guardado disponible excluye Link Cable; el código añade `08` cuando una bandera de la estructura apuntada está activa. Activar solo ese bit en WRAM permite Down→Right seleccionar Link Cable con entradas normales, pero A acaba en una pantalla uniforme sin espera/error. Es evidencia controlada del selector, no PASS de Link; véase `I11_P5_LINK_GATE_REPORT.md`.
- P6 ubica la bandera fuente en SRAM `0x133C` bit `04`, dentro de un bloque protegido por suma. Cambiarla sin corregir la suma deshabilita Continue; recalcularla preserva Continue y permite seleccionar Link con Down→Right, pero la confirmación repite exactamente la pantalla inválida P5. La activación natural y la espera/error siguen abiertas; véase `I11_P6_LINK_SAVE_FLAG_REPORT.md`.
- P7 adelantó la compuerta independiente G12: dos guardados naturales con Save Drum en F26 mostraron `SAVED!`, cambiaron el hash de SRAM y cargaron mediante dos Cold Continue en procesos/perfiles distintos. G12 pasa; I13 conserva su regresión global y sigue bloqueada por dependencias. Véase `I11_P7_F26_PERSISTENCE_PREVALIDATION.md`.

- P8 observó lecturas Bank 37 en `C008=2`; P9 demostró que era la rama Link Cable del título. P10 rectificó otra inferencia P9: `C0F2&0040` lleva al menú principal `A000:3A90`, no a tienda. La ruta natural de tienda sigue sin identificar. Los nombres instrumentales P9 de las trazas se conservan como datos históricos; véanse `I11_P9_ROUTE_CORRECTION.md` e `I11_P10_MAGIC_ROUTE_AND_HEADER.md`.
- P10 confirmó el desbloqueo controlado de Magic mediante `0070` y `0230`, `CA80=24C4→A4C4`, ejecución en `A000:46E0/48C8` y una lectura de cada puntero Bank 38 para `Fire` y `Shoots fireball.`. La descripción de 16/16 glifos es legible; el encabezado mantiene dos glifos japoneses y su fuente no está identificada. No se suma un PASS visual ni se aprueba el denominador de ancho.

- P11 localizó el primer glifo japonés del encabezado Magic en el mapa de tiles `0x3800` y los tiles de vídeo `0x8020/0x8040`. La traza Bank 30 acota recursos candidatos, pero no establece el offset ROM de los píxeles; cambiar `0x3645B8` modificó `None`, no el encabezado. Sin origen binario demostrado, F26 permanece intacta y Magic parcial. Véase `I11_P11_MAGIC_HEADER_PROVENANCE.md`.

- P12 reconstruyó el recurso comprimido Bank 30 del encabezado con píxeles de la fuente nativa, repuntó solo su descriptor y produjo F27 y BPS acumulativo JP→F27 reproducibles. La pantalla Magic controlada lee `Magic`, `Fire` y `Shoots fireball.`; 203 píxeles difieren solo en `x=8–79,y=2–12` y el menú previo es idéntico. Boot frío F27 válido. Véase `I11_P12_MAGIC_HEADER_F27.md`.
- P13 identificó la función de adquisición `9000:5028` y el escritor de bits `9000:3B70`: el objeto `0160` activa `0070`, `0230` y `0231`. Se desconoce el evento natural que concede `0160`; no hubo nueva prueba visual ni cambio binario. Magic conserva `PARTIAL_OPEN`; véase `I11_P13_MAGIC_ACQUISITION_SOURCE.md`.
- P14 localizó en Bank `1B`, `0x1BB9B8`, un comando de script `0012` que concede `0160`. Una redirección controlada del intérprete F27 confirmó `9000:3330→5028` y SRAM `0030:00→80`, `0068:00→C0`, deteniendo el ensayo en el cuadro 29. Falta el disparador natural del evento; sin PASS visual ni cambio binario. Véase `I11_P14_MAGIC_SCRIPT_EVENT.md`.
- P15 reconstruyó la tabla de escenas y ubicó ese comando dentro de la escena global `007E`, entrada `0300/0305`, script `0x1BB790`. Los siete checkpoints disponibles mostraron `CAD7=0000/0005`, ninguno `007E`; no se aprueba acceso natural ni hay cambio binario. Véase `I11_P15_MAGIC_SCENE_ORIGIN.md`.
- P16 enlazó la escena Fire `007E` con la región `CAD3=007E` de 4×4 celdas sin condiciones. En Bank 21 localizó el diálogo de mercader BUY/SEL y su callback `9000:D026→A000:A4E0`; falta disparador natural y pantalla válida. Sin cambio binario ni nuevo PASS. Véase `I11_P16_MAP_AND_SHOP_SOURCE.md`.
- P17 mapeó 35 comandos nativos de tienda en 29 escenas, ejecutó de forma controlada `0014/0031` desde First Trial y obtuvo una interfaz válida. Detectó `OWNED→OW`, lo corrigió a `NO` en F28 y validó el resultado visual, build y BPS acumulativo. La tienda pasa a `PARTIAL_OPEN`; escena `0074` queda como vecino estructural de Fire `007E`. Véase `I11_P17_SHOP_RUNTIME_AND_F28.md`.
- P18 seleccionó `SEL` con entrada normal dentro del evento controlado y alcanzó `9000:D026→A000:A4E0`. El panel real expuso cinco rótulos japoneses gráficos; F29 repunta su recurso Bank `0x30` y los reemplaza por `Gear Items`, `Arms`, `Armor`, `Charms` y `Amulets` usando píxeles ingleses nativos del propio juego. Boot, BUY/SEL y panel de compra permanecen idénticos. El checkpoint no leyó `BUYPRICE`/`REPAIR` ni completó una venta; véase `I11_P18_SHOP_SELL_AND_F29.md`.
- P19 reutilizó el Save #2 certificado con `Tomahawk`, adquirió `Earth Axe` mediante `9000:5028` y completó la venta nativa: inventario `0065/0066→0066`, saldo `0000→01E0`, 24 lecturas `BUYPRICE`. El evento separado `0014/0030` alcanzó la rama de reparación de armas, leyó `REPAIR` 32 veces y mostró `Repair?`; la durabilidad final no cambió y no se declara reparación consumada. F30 adapta los viewports de dos glifos con `BP` y `RP`. Véase `I11_P19_SHOP_TRANSACTION_AND_F30.md`.
- P20 confirma en una ruta natural de Manny la cadena de nombres `9000:3564→DI+0062→9000:E929→A000:B7DE`, guarda un checkpoint previo y sustituye solo el búfer D2AD para revisar el denominador máximo sin crear rutas ficticias. Véase `I11_P20_MAX_WIDTH_CONTROLLED_CLOSURE.md`.
- P21 identifica `Up2` como control de cantidad `F443`, selecciona una unidad y completa la reparación nativa: coste `0090`/144, dinero `1000→0F70` y durabilidad `3→4`. Las capturas de selección, `Repair?` y resultado final pasan. El único comando `0014/0030` queda mapeado a escena `00DC`, región 1×1 sin condiciones; la entrada natural sigue sin observarse. Véase `I11_P21_COMPLETE_REPAIR_AND_SCENE_MAP.md`.
- P22 transfiere las tres rutas exclusivamente naturales a `MANUAL_REQUIRED_BEFORE_RC`, con requisito y evidencia mínima. Se detienen repeticiones equivalentes y se habilita I12 sin modificar la matriz ni atribuir PASS. Véase `I11_P22_MANUAL_QA_HANDOFF.md`.

## Compuerta I11

I11 queda `DONE_WITH_DEFERRED_QA` e I12 queda habilitada. Matriz conservada: 4 `PASS`, 2 `PARTIAL_OPEN`, 1 `OPEN`. QA manual obligatoria antes de RC:

1. entrada natural a un mercader; venta y reparación ya pasan bajo control;
2. magia poblada y su descripción;
3. Link Cable natural con espera/error.

Quedan tres etapas activas de la auditoría: I12, I13 e I14.
