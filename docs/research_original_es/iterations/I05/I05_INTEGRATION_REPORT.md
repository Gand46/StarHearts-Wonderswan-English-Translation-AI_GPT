# I05 — Integración F22 de Bank 0x38

Fecha: 2026-09-26  
Estado: **DONE_WITH_DEFERRED_QA — integración y censo cerrados; runtime/visual diferidos a I11**

## Resultado

Se integraron las ocho traducciones aprobadas de Bank `0x38` mediante ocho punteros uint16 y un pool nuevo de 110 bytes en `0x38FF04–0x38FF71`. La región era relleno `FF`, está inmediatamente después del pool inglés existente y no era destino de ninguna de las cinco tablas auditadas. Las fuentes japonesas originales se conservaron intactas.

| Slot | Fuente JP | Destino F22 | Pantalla |
| --- | --- | --- | --- |
| `0x38024C` | `0x38130F` 弾 | `0x38FF04` | Ammo |
| `0x3804B8` | `0x381E6E` 豆 | `0x38FF0E` | Bean |
| `0x3804C8` | `0x381E72` 鉄 | `0x38FF18` | Iron |
| `0x38664C` | `0x386690` ファイヤー | `0x38FF22` | Fire |
| `0x386806` | `0x38684A` 火の玉を飛ばす | `0x38FF2C` | Shoots fireball. |
| `0x386B60` | `0x386CA2` アクセル | `0x38FF4E` | Accel |
| `0x386BBE` | `0x386E92` メタリコ | `0x38FF5A` | Metalico |
| `0x386C40` | `0x38710E` ト | `0x38FF6C` | To |

## Validación técnica

- F22 SHA-256: `3219fb1a0b49793ee7a9245e5468907c23a28f2b9125743d3cd17837e6485296`.
- Checksum WonderSwan: `2157`.
- Diferencias frente a F21: 128 bytes, exactamente 16 de punteros, 110 del pool y 2 del checksum.
- Offsets inesperados: 0.
- Censo: 1.568 slots de cinco familias; 1.396 destinos japoneses originales revisados.
- Estado F22: 1.395 repuntados, 1 traducido in-place y 0 destinos japoneses activos supervivientes.
- BPS acumulativo JP → F22 e incremental F21 → F22 verificados con herramienta independiente y salida idéntica byte a byte.
- `BUILD.bat` y `build.sh` apuntan al constructor acumulativo F22.

## Runtime y límite de eficiencia

Mesen abortó antes de emular con `std::bad_cast`. El control con F21 certificada y el perfil limpio fallaron de la misma manera, por lo que no es una regresión atribuible a F22. Conforme al presupuesto de I05, no se exploraron rutas equivalentes. Los ocho registros quedan `NOT_VALIDATED_DEFERRED_I11` para runtime/visual/función.

I05 se cierra técnicamente y habilita I06. Esto no concede PASS visual ni habilita RC.
