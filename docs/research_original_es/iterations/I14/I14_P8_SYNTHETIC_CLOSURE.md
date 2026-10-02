# I14-P8 — cierre sintético / F33

**Seis de seis casos PASS_SYNTHETIC; cero pendientes del alcance sintético solicitado. RC_SYNTHETIC_FOR_TESTING.** La aceptación vigente procede de la instrucción «no vamos a esperar evidencias reales ahora bastara con las sinteticas pero quedaran pass sintetic». No se declara progresión natural ni enlace físico probado. La publicación general no está autorizada.

| Caso | Estado | Evidencia y alcance |
|---|---|---|
| Tienda | PASS_SYNTHETIC | Paneles y venta/reparación controladas, heredadas P7; no todo stock/compra completa. |
| Fire/Magic | PASS_SYNTHETIC | Premio Fire nativo y Magic poblada; herencia P7. |
| Link | PASS_SYNTHETIC | WAITING P2 legible tras inicialización nativa; LINK ERROR histórico. Sin peer/transferencia. |
| Holy/Tirawaka/segundo First Trial | PASS_SYNTHETIC | Mapa, diálogo y banner controlados; herencia P7. |
| Ending | PASS_SYNTHETIC | Epílogo29 páginas; tres líneas corregidas F33. Ceremonia anterior y jefe excluidos. |
| Credits | PASS_SYNTHETIC |45 tarjetas/66 cadenas, desde Planning hasta Presented by/BANDAI; consumidor y terminador nativos. |

Se encontró el evento correcto en escena006E. El epílogo comienza1B7FC2; el comando de1B84F0 solicita los créditos por módulo 0025. A partir del estado de mapa sintético y la entrada a coroutine del epílogo, el juego ejecuta ending→credits continuamente. No hay salto posterior para fingir créditos. Capturas cada 30 frames, índices de cada página, trazas y hashes incluidos.

Tres segundas líneas excedían la ventana; F33 las abrevia a «was a messenger of stars.», «in the Inde homeland,» y «ruled by Oser, world savior,». Mismo significado, slots, controles, fuente y diccionario;39 bytes distintos de F32 incluyendo checksum. La ejecución final muestra las tres completas. Créditos ya eran ingleses: cero cambios a esas66 cadenas.

Build Python Linux desde JP, BPS directo aplicado con implementación independiente y checksum 3CF1: PASS. No se ejecutó BAT ni se repitieron G12/F26→F30. El BPS de traducción no contiene el hook de diagnóstico. Hay160 archivos de fuentes acumulativas y37 registros vigentes F31–F33 aceptados sintéticamente; no equivalen al total de textos del juego.

El ledger maestro, matriz de gates, I14_VALIDATION.json y PROJECT_STATE.json coinciden con este cierre. Los informes y validaciones previos quedan como historia; HISTORY_I14P7.json conserva el estado 3/6 anterior. El validador mantiene sus comprobaciones históricas y añade las de F33, cobertura y aceptación sintética actual.

Reproducción y modificaciones: runtime/p8/REPLAY.md, SYNTHETIC_PROVENANCE.json, METHODS_AND_LIMITS.md. Casos/hashes: CASE_EVIDENCE.json y review/*_pages.json. Los límites documentados no son deuda obligatoria de juego real bajo la política actual.
