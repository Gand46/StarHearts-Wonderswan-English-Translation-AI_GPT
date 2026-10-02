# I11-P7 — persistencia F26 adelantada para I13

Fecha: 2026-09-26. ROM F26 SHA-256 `0394c490bf239198fd86dced631448695069f517c21089f4a0c634914216d1a1`; ROM intacta. Entrada: guardado natural certificado de F15, SHA-256 `b067d46e48dca3ffabb6de93f6ab1475297137c346880b233518e9c3d298e1af`. No se cargó savestate ni se alteró SRAM/WRAM.

## Método y resultado

Tres perfiles Mesen 2.1.1 separados, cada uno en un proceso nuevo, recibieron únicamente el `.sav` y `.ieeprom` producidos por el paso anterior. El script `runtime/scripts/i11_p7_f26_save_cycle.lua` usa entradas normales: título, Continue, Y1/Save Drum, Yes. Las capturas se inspeccionaron directamente.

| Paso | Evidencia en pantalla | SRAM 32 KiB SHA-256 | Validación |
| --- | --- | --- | --- |
| Entrada F15 certificada | Continue compatible con F26 | `b067d46e48dca3ffabb6de93f6ab1475297137c346880b233518e9c3d298e1af` | Punto de partida, no guardado F26 |
| Save #1 en F26 | `Save progress now?` y `SAVED!` | `30c17cac18a0f78e7ab37864d81d083dafc0b6358285b0e2b9c195bb2d67aa55` | Cambiaron 228 bytes; suma interna correcta `9BA6` |
| Cold Continue #1 | Título Continue y retorno al campo | Copia de Save #1 | PASS en otro proceso/perfil |
| Save #2 en F26 | Segundo `SAVED!` tras Continue | `bdf516a28f149238992942f657e45b1f8f7fb377e66762a56243f399ec8fb2c6` | Cambiaron 6 bytes; suma interna correcta `9BA9` |
| Cold Continue #2 | Título Continue y retorno al campo | Copia de Save #2, hash estable | PASS en tercer proceso/perfil |

La suma interna se calculó con la rutina ya trazada en P6 sobre `0x128E–0x282C` y coincide con la palabra en `0x282D`. Las capturas representativas están en `runtime/f26_persistence/`; el título de ambos procesos fríos es byte a byte idéntico y se conserva una sola imagen. ROM, guardados, EEPROM, perfiles y logs completos quedan fuera del paquete. No se infiere persistencia a partir de la mera existencia de `.sav`.

## Clasificación

El requisito específico de **Save Drum → dos guardados naturales F26 → dos Cold Continue** pasa y cierra `G12_PERSISTENCE` según su denominador. I13 sigue bloqueada como etapa por su dependencia y la regresión global pendiente (incluidas rutas posteriores y final). I11 mantiene 3 PASS, 2 PARTIAL_OPEN y 2 OPEN: esta prueba independiente no cierra tienda, Magic, Link ni ancho máximo. Quedan I11–I14, cuatro etapas incompletas. Lote ampliado v1.2: un método dirigido, tres procesos, seis capturas conservadas; ahorro exacto de tokens no medido.
