#include "ScriptMgr.h"

// Clase base vacía para registrar el módulo en el emulador
class mod_nightelf_warlock : public PlayerScript {
public:
    mod_nightelf_warlock() : PlayerScript("mod_nightelf_warlock") {}
};

// Función de carga requerida por AzerothCore
void Addmod_nightelf_warlockScripts() {
    new mod_nightelf_warlock();
}