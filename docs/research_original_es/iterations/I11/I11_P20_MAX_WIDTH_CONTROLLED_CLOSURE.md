# I11-P20 — cierre controlado del denominador visual de ancho

Fecha: 2026-09-27  
Resultado: `PASS_CONTROLLED_SHARED_NATIVE_RENDERER`  
ROM: F30 sin cambios, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`

## Denominadores reconciliados

P3 conservaba dos cifras que no podían intercambiarse: 31/206 términos I02 en su límite lógico y 209/214 operandos integrados en la capacidad física disponible dentro de cada script. P20 vuelve a calcular ambas cifras desde los CSV vigentes y añade el denominador visual real del consumidor común.

Los 214 operandos `0x0022` recorren la cadena ya demostrada `9000:3564 → DI+0062 → 9000:E929 → A000:B7DE`, que copia y dibuja como máximo ocho glifos. En la ROM F30 sólo dos formas integradas únicas ocupan ese máximo visual: `Kitchiki` y `TradrKid` (esta última aparece en dos registros). Los demás campos físicamente llenos contienen de uno a siete glifos; estar al límite de su espacio inline no los convierte en cadenas de ocho glifos en pantalla.

## Renderizado controlado

La ruta natural F12 alcanzó el diálogo nombrado de `Manny`; la traza observó su búfer `D2AD` y el puente `9000:E929→A000:B7DE`. Se creó privadamente un checkpoint en el cuadro 1828, antes del render. Cada muestra sustituye sólo el búfer vivo inmediatamente antes de `E929`; la ROM, el evento, la caja, la fuente y el renderizador permanecen nativos.

Se conservaron seis capturas con nombres neutrales para separar la primera lectura visible del texto esperado. La transcripción directa, sin OCR, fue:

| Muestra | Transcripción visible | Glifos | Margen derecho |
|---|---:|---:|---:|
| `sample_01.png` | Kitchiki | 8 | 9 px |
| `sample_02.png` | TradrKid | 8 | 7 px |
| `sample_03.png` | IndiKid | 7 | 15 px |
| `sample_04.png` | Rica | 4 | 39 px |
| `sample_05.png` | Zunt | 4 | 40 px |
| `sample_06.png` | Eldr | 4 | 39 px |

Todos los glifos son completos, coherentes con la fuente nativa, distinguibles y legibles a escala nativa; no hay corte, solapamiento ni contacto con el borde. `Kitchiki` y `TradrKid` cubren el máximo integrado real. `IndiKid`, `Rica`, `Zunt` y `Eldr` cubren las cuatro etiquetas de hablante que P3 mantenía en el límite lógico. Las otras dos familias límite ya cuentan con evidencia previa: F30 muestra `BP/RP` dentro de sus viewports reales y F27 muestra `Shoots fireball.` completo en 16/16 glifos.

## Alcance honesto

Conforme a UR-31.1, esta prueba aprueba el renderizado, tipografía, glifos, diseño, ancho y legibilidad del consumidor compartido. No prueba que cada entidad haya sido encontrada durante juego normal y no se presenta como playthrough natural. Ese límite no bloquea la superficie específica de ancho, pero sigue aplicando a la cobertura natural general.

La superficie `Isolated/max-width strings` pasa de `PARTIAL_OPEN` a `PASS_CONTROLLED`. La matriz I11 queda en 4 `PASS`, 2 `PARTIAL_OPEN` y 1 `OPEN`. I11 sigue abierta por tienda/repair natural, Magic natural y Link Cable. No hubo cambio binario; F30 y su BPS permanecen vigentes. Ahorro exacto de tokens: `NOT_MEASURED`.
