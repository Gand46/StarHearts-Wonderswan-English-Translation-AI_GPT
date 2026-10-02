# I04 — Integración F21 de Bank 0x37

Fecha: 2026-09-26  
Estado: **DONE_WITH_DEFERRED_QA — integración cerrada; visual natural de tienda diferida a I11**

## Resultado de esta etapa

Las cuatro ocurrencias aprobadas de Bank `0x37` están integradas en F21, reconstruyen de forma determinista, conservan límites, NUL y punteros lejanos, y son consumidas por sus rutinas nativas. El checksum WonderSwan y ambos BPS pasan verificación independiente.

I04 se cierra técnicamente sin conceder un PASS visual indebido. El mensaje `WAITING P2` pasa inspección en activación nativa controlada, pero `OWNED`, `BUYPRICE` y `REPAIR` no cuentan con una captura legible dentro de la escena natural completa de tienda. Las capturas con inicialización parcial siguen siendo evidencia diagnóstica, no PASS visual; las tres deudas quedan `NOT_VALIDATED_DEFERRED_I11`.

## Cambios F21

| Offset | Japonés | Pantalla F21 | Resultado estático |
| --- | --- | --- | --- |
| `0x370000` | 現在対戦者を待っています | `WAITING P2` | PASS |
| `0x3769D0` | 所持 | `OWNED` | PASS |
| `0x3769E2` | 買値 | `BUYPRICE` | PASS |
| `0x3769F4` | 修理 | `REPAIR` | PASS |

- F21 SHA-256 privado: `00f46965177716ec459ac2a0f6e89a4e50548af205582e6d0ba176c015fc36ec`.
- Checksum WonderSwan: `5B38`.
- Cambios reales respecto de F20, checksum incluido: 61 bytes.
- Offsets inesperados: 0.
- Punteros `7000:69D0`, `7000:69E2` y `7000:69F4`: intactos y dentro de rango.
- Fuente/fonte nativa: sin cambios; no hubo repointing.

## Evidencia runtime

- Link: la función real `A000:0778` leyó `0x370000`, llamó al motor original `9000:3C00`, retornó y dejó `WAITING P2` legible en la captura controlada.
- Tienda: `A000:A9D6`, `A000:A97C` y `A000:A922` leyeron respectivamente `OWNED`, `BUYPRICE` y `REPAIR`; las tres pasaron por `9000:5778` y `9000:3C00`.
- Los wrappers reales `A000:A858` y `A000:A894` confirmaron la secuencia de campos de compra/reparación más `OWNED`.
- Boot y menú START desde el checkpoint natural pasan sin regresión.
- La navegación natural alcanzó un interior y diálogo reales, pero no el panel de tienda que consume estas tres etiquetas.

## BPS

- JP original → F21 acumulativo: PASS, SHA-256 del parche `a02e739e0aa836f66f3709f76f9f276e085eaddae9837e2e398737f898958c20`.
- F20 → F21 incremental: PASS, SHA-256 del parche `8954e3c59bb66c6dee2557e38e5ff5c420f440a43eec07ad072f2523c090a575`.
- Ambos reconstruyen byte a byte el SHA-256 F21 esperado mediante `17_WS_Patch_Tools_v0.1.1`.

## Compuerta y siguiente acción

Pasan integración, encoding, límites, punteros, checksum, reconstrucción, BPS, boot y consumo runtime. La revisión visual/funcional natural del panel de tienda se transfiere a I11. I05 queda habilitada; I14/RC permanece bloqueada hasta cerrar esa deuda.

No se distribuye ninguna ROM.
