# Star Hearts — 1.40 / I14-P9 / F34

**Revisión correctiva de legibilidad: tres aprobaciones antiguas revocadas; dos defectos ROM corregidos y una captura reemplazada.**

- WAITING P2: la imagen P8 de frame 600 mezcla dos posiciones durante el desplazamiento. Usar la captura estable 720; nueve glifos reconocidos y comparados con la fuente nativa. El rótulo no cambia en ROM.
- Segundo banner: EVenT se corrige a EVENT:First Trial dentro del mismo espacio.
- LINK ERROR: código numérico corregido a su campo real; ya no pisa ERROR ni deja basura.

Informe: iterations/I14/I14_P9_LEGIBILITY_AUDIT.md. Reproducción y evidencias: iterations/I14/runtime/p9. Históricos se conservan con sus errores identificados; leer SUPERSEDED_APPROVALS.json antes de reutilizarlos.

Fuentes completas: iterations/I14/F34_SOURCE/README_F34.md.
BPS directo JP→F34: iterations/I14/patches/StarHearts_EN_phase13BG_F34_CUMULATIVE_2026-09-28.bps.
F34 SHA-256: d22bb029570e1b053e7cc11bd0cd1632ff310343d3c44ffaa072f771ae820ca0. Checksum 3CD5.

Seis casos PASS_SYNTHETIC en alcance documentado, RC_SYNTHETIC_FOR_TESTING. Sin aprobación global del juego ni publicación general. El guion bajo histórico tiene procedencia/uso visible no validados; no se observó en la muestra. No se exige prueba natural/peer ni BAT ya excluidos por el usuario.
