# Star Hearts F37 — cierre de los cuatro gráficos

Los cuatro recursos quedaron traducidos e integrados:

| Japonés | Inglés | Validación |
| --- | --- | --- |
| 対戦？ | Battle? | PASS sintético en Mesen |
| 値段？ | Price? | PASS sintético en Mesen |
| 伝授？ | Teach? | PASS sintético en Mesen |
| 戻す？ | Return? | PASS sintético en Mesen |

Astra rastreó 77 llamadas al decodificador, 19 modos y 18 puntos de llamada del cargador. No encontró selección de estos cuatro gráficos en las rutas auditadas. Se clasifican como recursos conservados sin selección identificada en esas rutas; no se afirma que sean imposibles de alcanzar por cualquier otra vía.

Para cerrar su traducción y legibilidad, se seleccionó cada recurso mediante inyección del selector en el decodificador real. Mesen cargó los datos de la ROM y los mostró en el cuadro emergente nativo. Las capturas de la tienda son una prueba de renderizado: no se añadieron acciones Battle/Price/Teach/Return al menú de compra ni se ejecutaron esas supuestas operaciones.

Se conservaron los glifos nativos, la sombra, la paleta y el marco. Tres bloques caben en sus posiciones originales; Return? se trasladó a espacio FF verificado del mismo banco y se actualizó sólo su puntero. El manifiesto documenta los 689 bytes modificados.

**Resultados:** cuatro renderizados legibles, cuatro estados recargados con imagen idéntica, 36 capturas de compra/venta sin inyección idénticas a F36, checksum correcto y BPS acumulativo comprobado con aplicador independiente. Los 181 nombres y su operando adicional permanecen byte por byte como en F36; sus pruebas no se repitieron innecesariamente.

El alcance de estos cuatro gráficos queda cerrado en traducción, integración y validación visual sintética. Esto no concede aprobación global a toda la traducción ni demuestra rutas naturales para los cuatro recursos.

El BPS se aplica directamente a la ROM japonesa original, SHA-256 `64179c9924ec1280861ebd83b99aaeb0770701051e590613430ae9a6dbe31255`.

ROM F37: SHA-256 `f0791dcf53045afc126ce11ed5b9eb7091c47c1c8195eaa525737c5fec5ffb57`; checksum `DB46`.

BPS: SHA-256 `dba7b7f5cd2a4980f2ae7af9ed80b5bef6b8042279dda0f46ba00084696eddde`.

Fuentes acumulativas, informe técnico, scripts, capturas, estados y pruebas están incluidos. No se incluye ROM, BIOS ni emulador.
