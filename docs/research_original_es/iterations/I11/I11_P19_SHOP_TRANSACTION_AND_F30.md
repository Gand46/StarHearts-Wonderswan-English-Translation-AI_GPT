# I11-P19 — transacción de venta, reparación y F30

Fecha: 2026-09-27  
Resultado: `PASS_CONTROLLED`, con entrada natural al mercader todavía abierta  
ROM activa: F30, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, checksum WonderSwan `9487`

## Alcance verificable

P19 reutiliza el Save #2 certificado que contiene un `Tomahawk` real (`0065`). La ruta cercana a Wampa activa un evento válido, pero ese NPC no es mercader: su diálogo señala la tienda de Wampa. Para no atribuirle una entrada natural inexistente, la prueba redirige ese evento activo a comandos de tienda ya presentes en la ROM y declara el método como controlado.

Antes de la tienda, el mismo evento llama la función nativa de adquisición `9000:5028` con el arma `0066` (`Earth Axe`). Esto deja dos armas válidas, condición que exige el selector `Arms`, sin fabricar una estructura de inventario manual.

## Venta completa

El evento nativo `0014/0031` alcanza `9000:BD30`, la rama `SEL` `9000:D026` y el panel `A000:A4E0`. La secuencia selecciona `Arms`, abre la lista `Tomahawk/Earth Axe`, muestra `Sell?` y confirma la venta del `Tomahawk`.

El estado final es demostrable:

- inventario previo: `0065,0066,0000`;
- lectura de `BUYPRICE`: 24 accesos;
- valor mostrado: `480` (`0x01E0`);
- inventario final: `0066,0000,0000`;
- dinero final: `0x01E0`.

Por ello la venta completa pasa bajo control. No se declara entrada natural al mercader.

## Consumidor de reparación

La reparación no pertenece a la rama `SEL`. P19 localizó y ejecutó el evento nativo separado `0014/0030`, en físico `0x1D1BA2`. Con una reducción efímera de durabilidad `4→3`, la ruta alcanza `9000:CE44` (armas), `A000:9C50` (menú), `A000:A894` (panel), lee `REPAIR` 32 veces y muestra `Repair?`.

Esto valida el consumidor y el rótulo de reparación. La durabilidad final permanece en 3, por lo que P19 no afirma una reparación consumada.

## Hallazgo visual y corrección F30

Los campos `BUYPRICE` y `REPAIR` ocupan ocho celdas en Bank `0x37`, pero ambos paneles muestran sólo dos glifos. F29 producía `BU` y `RE`: legibles como prefijos, pero incompletos. F30 conserva cada campo de 18 bytes y usa:

| Offset | F29 | F30 | Resultado |
|---|---|---|---|
| `0x3769E2` | `BUYPRICE` | `BP` + 6 espacios | `BP 480` completo |
| `0x3769F4` | `REPAIR` + 2 espacios | `RP` + 6 espacios | `RP 0` completo |

La diferencia visual queda confinada a los rótulos: 36 píxeles para venta, caja exclusiva `(14,129)-(22,138)`, y 21 píxeles para reparación, caja `(16,129)-(22,138)`.

## Reproducción y límites

- Fuente acumulativa: `F30_SOURCE/`.
- BPS JP→F30: `patches/StarHearts_EN_phase13BG_F30_CUMULATIVE_2026-09-27.bps`.
- Scripts controlados: `runtime/scripts/i11_p19_controlled_sale.lua` y `runtime/scripts/i11_p19_controlled_repair.lua`.
- Capturas y resumen: `runtime/shop_f30/`.

El rebuild desde la ROM japonesa y el roundtrip BPS producen byte a byte F30. La superficie tienda sigue `PARTIAL_OPEN` únicamente por la entrada natural al mercader y por no declarar una reparación consumada. Magic natural, Link y el denominador visual de ancho máximo continúan abiertos; I12 permanece bloqueada.
