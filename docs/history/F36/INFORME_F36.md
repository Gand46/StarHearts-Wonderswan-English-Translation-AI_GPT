# Star Hearts F36 — cierre de tienda y 181 nombres

Se corrigieron **Bazaar** y **Buy?** en los gráficos de compra. La revisión con Astra resolvió los **181 campos japoneses**: son nombres iniciales que el juego copia al búfer del actor. No eran simples datos sin uso. Se observó el nombre japonés de Tirawaka bajo diálogo inglés antes de su sustitución posterior.

F36 incorpora las 181 traducciones con nombres ingleses ya documentados, salvo las decisiones editoriales explícitas Jimusu, Guard y Poco. La identificación se apoyó en 164 enlaces de ID a la tabla de entidades y 17 casos revisados individualmente. No se tomó automáticamente el nombre del siguiente hablante.

También se corrigió **un operando adicional de Tirawaka**, fuera de los 181, que terminaba con otro código de control y había quedado fuera del censo anterior.

| Validación | Resultado |
| --- | --- |
| Consumidores de los 181 campos | 181 resueltos |
| Traducción e integración | 181/181 |
| Ejecución del cargador nativo: ocho palabras y 16 bytes exactos | 181/181 PASS; cero fallos |
| Metadatos vecinos | 181/181 conservados |
| Tienda | Bazaar y Buy? legibles en Mesen; venta sin cambios visuales |
| Nombre inicial de ocho caracteres | Tirawaka completo y legible |
| Operando adicional | Tiraw integrado y confirmado en pantalla |
| Fuentes → ROM y BPS original → ROM | Idénticos byte por byte |
| Checksum WonderSwan | 775C, correcto |
| Estados de tienda incluidos | Cuatro guardados sintéticos recargados correctamente |

La validación visual de nombres fue **representativa**: no se afirma que se hayan visitado ni revisado visualmente las 181 escenas. El lote sí está cerrado en identificación del consumidor, traducción, integración y carga nativa de cada campo. Los estados son de diagnóstico; no acreditan persistencia del guardado interno ni recorrido natural.

Quedan fuera del cierre global los cuatro gráficos **対戦？**, **値段？**, **伝授？** y **戻す？**, cuyo uso todavía debe rastrearse, además del resto del universo no demostrado por esta revisión. F36 se entrega como versión de pruebas; no se declara traducción completa del juego.

El paquete contiene las fuentes acumulativas, BPS directo desde la ROM japonesa, mapeo de cada campo, informe independiente de Astra, scripts, trazas, capturas y estados. No contiene ROM, BIOS ni emulador. `README_F36.md` explica la compilación y las direcciones técnicas; `qa/F36/companions/INFORME_181_F36.md` contiene el análisis del consumidor.

ROM F36 SHA-256: `da2966870ef022e68f84e07ead6d017a686c47f55a6036f57974c57c6d4578d2`.

BPS acumulativo SHA-256: `038daaa050834cf5532beaf74f4431f2cfbe60b9d79c481ef8845c6860b0653d`.
