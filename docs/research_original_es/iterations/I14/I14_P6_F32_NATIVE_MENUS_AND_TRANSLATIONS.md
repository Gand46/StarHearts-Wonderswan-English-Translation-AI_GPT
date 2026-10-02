# I14-P6 — siete menús nativos, e-Pet y descripción Gnome

Paquete 1.37. Fecha técnica UTC 2026-09-28 (2026-09-27 en Bogotá al inicio). F32, checksum `3D99`. **EXPERIMENTAL_INTERNAL_TEST / RC_NOT_AUTHORIZED**.

## Resultado

Se abrieron las siete pantallas que P5 había comprobado únicamente mediante sustitución del encabezado: Animal Powers, Gear Items, Charms, Amulets, Skills, e-Pet y Secret Skills. Esta vez se entró por su menú y dispatcher original, con condiciones de inventario/flags específicas. No se sustituyeron recursos, eventos ni instrucciones de flujo. La procedencia y las condiciones siguen siendo sintéticas; no es progresión natural.

La revisión directa encontró y corrigió:

- **22 rótulos gráficos de e-Pet**, correspondientes a 19 textos únicos.
- **Una descripción de Skills compartida por 20 entradas**: `ノームタイプ　つよさ＋１` → `Gnome: Str+1`.
- Solapamiento de los rótulos elementales ingleses con valores de dos cifras detectado en el primer prototipo: se ajustaron abreviaturas y se desplazaron ambos campos numéricos cuatro píxeles.

Las 11 correcciones F31 permanecen. No se declara traducción global terminada ni cierre del censo completo del juego.

## Condiciones de acceso demostradas

El menú usa `CA86` como selector y la tabla nativa `3A404C`, llamada en `A000:4027`. Los flags se leen mediante `9000:3BD0`, con base física SRAM `10022`, byte `floor(flag/8)` y máscara `80 >> (flag mod 8)`.

| Pantalla | Selector / handler | Condición mínima diagnóstica |
|---|---|---|
| Animal Powers | 1 / A000:4C10 | Flag 0252; Monkey Heart aparece con descripción inglesa |
| Gear Items | 3 / A000:5EF0 | Objeto 0018 en hueco libre C150, cantidad 1; tabla de objetos válidos 364B90 |
| Charms | 6 / A000:7860 | Objeto 00E0, cantidad 1 |
| Amulets | 7 / A000:7E50 | Objeto 0120, cantidad 1 |
| Skills | 10 / A000:8A30 | Flag 0360; nombre Accel y descripción Gnome |
| e-Pet | 11 / A000:8CE0 | Bit 0 en D11B y selector D12F=2..5 |
| Secret Skills | 12 / A000:8F70 | Flag 0310; AxeThr / Throw Axe |

El checkpoint de entrada es el P4 de mapa de reparación, SHA `edde91825ed7c9bf5669ef3317bb1210a6ca331fe432f220a2143914b15b3059`. La ROM F32 no contiene el warp P4. Las escrituras de fixture se ejecutan solo en Lua; después, el mando abre y navega los menús. No se intenta promover estos estados a `AUTOMATED_NATURAL_PASS`.

## e-Pet: texto, fuente y diseño

| Original | Traducción |
|---|---|
| ライフ / マジック | Life / Magic |
| 対戦数 / 勝星数 | Battles / Wins |
| ステータス | Status |
| つよさ / まもり / かしこさ / すばやさ | Str / Def / Int / Agi |
| レベル, cuatro apariciones | Lv |
| 火 / 水 / 風 / 地 / 光 / 闇 / 氷 / 雷 / 神 | Fire / Wtr / Wnd / Erth / Lgt / Dark / Ice / Thun / Holy |

Wtr=Water, Wnd=Wind, Erth=Earth, Lgt=Light y Thun=Thunder. Str/Def/Int/Agi representan Strength/Defense/Intelligence/Agility; los términos compactos responden al espacio real. No se cambian valores, significado de los elementos ni efectos.

Se reutilizaron los glifos latinos CP932 dibujados por el renderer nativo, capturados en un atlas diagnóstico. El atlas usa sustitución temporal del búfer de nombres de Skills, declarada exclusivamente como extracción tipográfica. No concede PASS de progresión. Los glifos conservan todos sus píxeles, altura y coordenadas verticales; solo se elimina margen horizontal vacío al componer la imagen. No hay tipografía externa, escalado ni modificación de la fuente/renderer compartido.

El recurso gráfico índice 12, situado en `30AA96`, conserva sus cuatro paletas y su encabezado F31. El prefijo reconstruido ocupa 1.402 bytes dentro de los 1.597 disponibles antes de la siguiente paleta conservada. Tras decodificar, cada píxel fuera de los rectángulos de etiquetas es idéntico. Las referencias internas permanecen intactas.

Los operandos de posición en `3A8EED` y `3A8EF6` cambian X=140/188 a X=144/192. El formateador numérico, ancho de dos dígitos, valores y gameplay no cambian. La prueba con 99 reveló y luego descartó por corrección el primer prototipo con solapamiento; se conserva como evidencia negativa, nunca como aprobado.

## Descripción compartida

La tabla `3872F4` contiene 161 slots: 160 entradas más el marcador desconocido. En F31 había 20 referencias directas a `387436`, 140 referencias a 23 IDs del motor traducido y un marcador `????`. La descripción literal japonesa seguía activa y el consumidor `A000:8B14..8B26` la dibujaba. Se corrigió in-place en 26 bytes, con terminador y relleno preservados. La tabla de 161 slots no cambia.

El registro de lectura de `87436..8744F` demuestra consumo nativo del texto corregido. La revisión directa lee `Gnome: Str+1`. La denominación Skills del menú inglés previo se conserva; esta corrección cubre la descripción, no una revisión lingüística exhaustiva de los 160 nombres.

## Validación y límites

- Revisión de capturas nativas, incluyendo estados seleccionados y mensajes Remove?/Discard? observados en la navegación.
- e-Pet con valores 0 y 99/999, nombre de ocho letras y las cuatro paletas. Las cifras altas y el nombre ABCDEFGH son fixtures de anchura; no acreditan un e-Pet adquirido, entrenado o enlazado.
- Cinco menús no afectados conservan identidad de píxeles frente a F31 en cuatro capturas cada uno: 20 comparaciones sin diferencias.
- Build Linux desde JP, BPS directo aplicado independientemente y checksum 3D99. 1.226 bytes cambiados, todos previstos; cero offsets inesperados.
- Quince recursos de menú decodificados permanecen idénticos; también las cuatro paletas e-Pet y la tabla de descripciones. No se repitieron G12 ni el diferencial F26→F30.
- **BAT no se intentó ni se buscó cmd/Wine**, conforme a la instrucción actual del usuario. La validación de build se limita al núcleo Python Linux. El wrapper se mantiene apuntando a F32 como fuente auxiliar sin certificar su host.

El alcance visual de las siete pantallas pasa de encabezado aislado a **panel nativo representativo controlado**. No se certifican todos sus objetos, todas las páginas, evolución de e-Pet, Link ni funcionalidad integral de cada sistema.

Los seis casos reales conservan exactamente sus clasificaciones: cinco `EXTERNAL_PLAYTEST_REQUIRED` y uno `EXTERNAL_HARDWARE_OR_SUPPORTED_PEER_REQUIRED`. Holy Temple tardío, ending y credits no se reintentaron sin condición nueva. Ningún resultado de esta etapa autoriza RC.

Siguiente avance útil: obtener condiciones concretas o checkpoint tardío de Holy Temple y el consumidor/checkpoint terminal para ending→credits. Reutilizar los nuevos accesos para defectos visuales reproducibles; no repetir los métodos ya descartados. Ahorro de tokens: no medido. Cada replay nuevo se limita a 1.120 frames y 35 segundos internos, con watchdog de 45 segundos.
