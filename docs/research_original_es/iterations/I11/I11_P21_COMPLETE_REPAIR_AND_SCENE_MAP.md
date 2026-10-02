# I11-P21 — reparación completa controlada y mapa de escena

Fecha: 2026-09-27  
ROM: F30, SHA-256 `17e4fb5eed9f8df7f1e500e9f50aecd1febf0e147545afd6a0c07ce844461eaa`, checksum `9487`  
Resultado: `PASS_CONTROLLED_COMPLETE_REPAIR`; entrada natural al mercader todavía abierta  
Cambio binario: ninguno

## Objetivo y límite de la afirmación

P19 había alcanzado la rama nativa `0014/0030`, mostrado `RP` y `Repair?`, pero no había elegido cantidad de reparación. P21 corrige exclusivamente esa deuda funcional. Parte del Save #2 certificado, usa el mismo redireccionamiento controlado al evento nativo y modifica de forma efímera solo la durabilidad inicial del `Tomahawk` y el saldo para que la operación sea observable. No se afirma haber llegado al mercader mediante navegación natural.

## Causa y ejecución

El menú de reparación no usa el primer pad para la cantidad. La rutina `A000:57EE` consulta `C05A & 0010`, correspondiente a `Up2`, e incrementa `F443`; `Down2` usa `0040`. Con una unidad seleccionada, la cadena nativa fue:

- `9000:CE44`: rama de arma;
- `A000:9C50`: menú de reparación;
- `A000:A894`: panel y vista previa;
- `A000:5A4A`: cálculo de coste;
- `A000:5A59`: comprobación de fondos;
- `A000:5A60`: débito;
- `A000:5A80`: aplicación de la reparación;
- `A000:5A89`: suma de `F443` a la durabilidad y limpieza de la cantidad.

El resultado medido fue:

| Campo | Inicial | Final |
| --- | ---: | ---: |
| Cantidad seleccionada | 0 | 1 antes de confirmar; 0 tras consumirla |
| Durabilidad real | 3 | 4 |
| Dinero hexadecimal | `1000` | `0F70` |
| Dinero decimal | 4096 | 3952 |
| Coste | — | `0090` = 144 |

La vista previa ya muestra `Dur 4` antes del commit, pero la traza de memoria conserva `3` hasta el cuadro 437. En ese cuadro se ejecutan cálculo, fondos, débito y aplicación; después la comprobación final registra durabilidad `4`, saldo `0F70` y cantidad `0`.

## Revisión visual

Las tres capturas aceptadas muestran `Tomahawk`, `Atk 8 Dur 4`, el rótulo F30 `RP`, el saldo y el diálogo de confirmación sin corte, solapamiento ni basura:

- selección: `RP 144`, `NO 4096`;
- confirmación: `Repair?` con los mismos valores;
- final: `RP 0`, `NO 3952`.

La evidencia está en `runtime/repair_f30_p21/`; `visual_review.csv` conserva la lectura directa de cada captura y `controlled_complete_repair_trace.txt` la transición funcional.

## Mapeo estático de la escena

`i11_p21_repair_scene_map.py` escanea todas las entradas de script conocidas en Banks 19–20 y encuentra una sola secuencia exacta `0014/0030`:

- script físico `0x1D1BA2`;
- escena `0x00DC`;
- claves `0300/0001`, fila 0;
- registro de región físico `0x182580`;
- región 1×1, sin condiciones de celda.

Esto reduce la búsqueda natural a una escena, pero no demuestra cómo se entra en ella. `repair_scene_map.json` conserva `natural_scene_entry_observed=false`.

## Decisión

La reparación completa pasa como `PASS_CONTROLLED`: se consumó por rutinas nativas, con coste, débito y aumento de durabilidad demostrados. La fila de tienda permanece `PARTIAL_OPEN` únicamente por faltar la entrada natural a un mercader. La matriz I11 sigue 4 `PASS`, 2 `PARTIAL_OPEN` y 1 `OPEN`; I12 continúa bloqueada.

No se repitieron las rutas Wampa/WonderGate ni la venta P19. El ahorro exacto de tokens no se inventa: `NOT_MEASURED`.
