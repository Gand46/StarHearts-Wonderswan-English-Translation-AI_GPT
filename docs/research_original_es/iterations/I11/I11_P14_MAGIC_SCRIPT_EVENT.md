# I11-P14 — comando de evento que concede Fire

Fecha local: 2026-09-26. ROM F27 SHA-256 `641acc39309f64cc16bfeee0f450461c99dd20d4ee4a28e7d0481a54471625d4`. **Sin cambio binario ni aprobación de adquisición natural.** Tanda limitada a una superficie, dos métodos distintos (referencia/despacho estático y ejecución controlada del intérprete); no se repitió la captura de Magic ni una navegación equivalente.

## Referencia de evento

En el script físico `0x1BB9B8` aparece una única secuencia `12 00 60 01 00 00`; `02 00` es el comando siguiente. El despachador `9000:311C` lee el opcode `0012`, y la entrada de su tabla en ROM `0x39319E` vale `3330`. El handler `9000:3330` lee `ES:[SI]` como `AX=0160`, comprueba que el segundo word es cero y llama a `9000:5028`. La adquisición pasa por `9000:50F4/5124` y el escritor `9000:3B70`, identificados en P13. Este vínculo concreta **un script que entrega el objeto del primer hechizo**; no revela por sí solo el mapa, NPC ni condiciones que ejecutan el script.

## Comprobación acotada en F27

La sonda `runtime/scripts/i11_p14_script_acquisition_probe.lua` partió de un checkpoint natural First Trial. En un paso de script activo (`9000:3151`, cuadro 27) redirigió temporalmente el puntero `ES:SI` a `2000:B9B8` y el banco mapeado a `DB` (Bank físico `1B`). No escribió los bits de Magic. La ejecución registró **una entrada** en `9000:3330`, **una** en `9000:5028` con `AX=0160` y escrituras nativas para `0070`, `0230` y `0231`. Al cuadro 29, SRAM pasó de `0030=00, 0068=00` a `0030=80, 0068=C0`; la sonda se detuvo ahí. Hubo otra llamada intercalada al escritor para `0009` que no cambia la conclusión sobre esos tres bits. Se conserva solo `runtime/magic_script_event/native_award_trace.txt`; las trazas largas descartadas no forman parte de la evidencia.

La redirección del puntero es **controlada**: confirma que los bytes del script F27 producen los bits previstos mediante las funciones del juego, pero no que el evento sea alcanzable en el checkpoint ni que se haya aprendido Fire naturalmente. P12 ya validó la pantalla inglesa controlada; no se suma un PASS visual. I11 sigue con 3 `PASS`, 2 `PARTIAL_OPEN`, 2 `OPEN`; quedan I11–I14 (cuatro etapas incompletas). La ruta natural de este evento, tienda, Link y el denominador visual de ancho permanecen pendientes. Ahorro exacto de tokens: `NOT_MEASURED`.
