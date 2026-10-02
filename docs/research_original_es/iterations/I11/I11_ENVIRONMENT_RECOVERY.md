# I11 — recuperación del entorno Mesen

Resultado: `PASS` para ejecución headless.

- Emulador: Mesen 2.1.1 Linux x64.
- SHA-256 del ejecutable privado usado: `ae43f1438282aaaff90a009aa8ada648bc5d631b070656285d7de9cbff513b41`.
- Perfil mínimo: `settings.json` con `{}` junto al ejecutable.
- Runtime: `LD_PRELOAD=$(g++ -print-file-name=libstdc++.so.6)`.
- Modo: `--testRunner --doNotSaveSettings --debug.scriptWindow.allowIoOsAccess=true`.
- Sin `LD_PRELOAD`, el proceso aborta con `std::bad_cast`.
- No se requiere X11 para esta ruta.

Regla de reproducibilidad: cada ruta debe arrancar desde ROM limpia o desde un savestate explícito. Un perfil que contenga autoestados no puede reutilizarse como evidencia de inicio limpio.
