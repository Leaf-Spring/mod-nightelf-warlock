import struct
import os

WARLOCK_CLASS_BIT = 256   # Bit correspondiente a la clase Brujo (2^8)
NIGHTELF_RACE_BIT = 8     # Bit correspondiente a la raza Elfo de la Noche (2^3)

# Spell IDs representativos de la racial de Elfo de la Noche (Fusión de sombras):
TARGET_RACIAL_SPELLS = {20580, 58984}

def patch_char_base_info(filename="CharBaseInfo.dbc", race=4, class_id=9):
    print("=== 1/3: Procesando CharBaseInfo.dbc ===")
    if not os.path.exists(filename):
        print(f"[!] Archivo no encontrado: {filename}\n")
        return

    with open(filename, "rb") as f:
        data = bytearray(f.read())

    magic, record_count, field_count, record_size, string_block_size = struct.unpack("<4sIIII", data[:20])
    records_start = 20
    string_block_start = records_start + (record_count * record_size)

    # Verificar si (4, 9) ya existe
    for i in range(record_count):
        off = records_start + (i * record_size)
        r, c = data[off], data[off + 1]
        if r == race and c == class_id:
            print(f"[-] OMITIDO: La combinación Elfo de la Noche ({race}) - Brujo ({class_id}) ya existe en el archivo.\n")
            return

    # Inserción del registro de 2 bytes
    new_record = bytes([race, class_id])
    data[string_block_start:string_block_start] = new_record
    struct.pack_into("<I", data, 4, record_count + 1)

    with open(filename, "wb") as f:
        f.write(data)
    print(f"[+] ÉXITO: Se registró la combinación Elfo de la Noche ({race}) + Brujo ({class_id}).\n")


def patch_char_start_outfit(filename="CharStartOutfit.dbc", target_race=4, target_class=9, source_race=7):
    print("=== 2/3: Procesando CharStartOutfit.dbc ===")
    if not os.path.exists(filename):
        print(f"[!] Archivo no encontrado: {filename}\n")
        return

    with open(filename, "rb") as f:
        data = bytearray(f.read())

    magic, record_count, field_count, record_size, string_block_size = struct.unpack("<4sIIII", data[:20])
    records_start = 20
    string_block_start = records_start + (record_count * record_size)

    max_id = 0
    already_exists = False
    templates = []

    for i in range(record_count):
        off = records_start + (i * record_size)
        outfit_id = struct.unpack_from("<I", data, off)[0]
        race = data[off + 4]
        cls = data[off + 5]

        if outfit_id > max_id:
            max_id = outfit_id

        if race == target_race and cls == target_class:
            already_exists = True

        if race == source_race and cls == target_class:
            templates.append(bytearray(data[off : off + record_size]))

    if already_exists:
        print(f"[-] OMITIDO: Los outfits para Elfo de la Noche ({target_race}) - Brujo ({target_class}) ya existen.\n")
        return

    if not templates:
        print(f"[!] ERROR: No se encontraron las plantillas de Brujo Gnomo (Raza {source_race}).\n")
        return

    added_bytes = bytearray()
    added_count = 0

    for template in templates:
        max_id += 1
        cloned = bytearray(template)
        struct.pack_into("<I", cloned, 0, max_id)  # Nuevo Outfit ID
        cloned[4] = target_race                    # Raza Elfo de la Noche (4)
        
        added_bytes.extend(cloned)
        added_count += 1

    data[string_block_start:string_block_start] = added_bytes
    struct.pack_into("<I", data, 4, record_count + added_count)

    with open(filename, "wb") as f:
        f.write(data)
    print(f"[+] ÉXITO: Se clonaron {added_count} outfits (Nuevos IDs: {max_id - added_count + 1} y {max_id}).\n")


def patch_skill_line_ability(filename="SkillLineAbility.dbc"):
    print("=== 3/3: Procesando SkillLineAbility.dbc ===")
    if not os.path.exists(filename):
        print(f"[!] Archivo no encontrado: {filename}\n")
        return

    with open(filename, "rb") as f:
        data = bytearray(f.read())

    magic, record_count, field_count, record_size, string_block_size = struct.unpack("<4sIIII", data[:20])
    records_start = 20

    patched_spells = 0

    for i in range(record_count):
        off = records_start + (i * record_size)
        
        spell_id = struct.unpack_from("<I", data, off + 8)[0]
        race_mask = struct.unpack_from("<I", data, off + 12)[0]
        class_mask = struct.unpack_from("<I", data, off + 16)[0]

        if (race_mask & NIGHTELF_RACE_BIT) and (spell_id in TARGET_RACIAL_SPELLS):
            if not (class_mask & WARLOCK_CLASS_BIT):
                new_class_mask = class_mask | WARLOCK_CLASS_BIT
                struct.pack_into("<I", data, off + 16, new_class_mask)
                patched_spells += 1

    if patched_spells > 0:
        with open(filename, "wb") as f:
            f.write(data)
        print(f"[+] ÉXITO: Se asignó el bit de Brujo a {patched_spells} raciales específicas de Elfo de la Noche.\n")
    else:
        print("[-] OMITIDO: Las raciales específicas ya están configuradas para Brujo.\n")


if __name__ == "__main__":
    print("=== APLICANDO PARCHES BINARIOS A DBCs (ELFO DE LA NOCHE BRUJO) ===\n")
    patch_char_base_info()
    patch_char_start_outfit()
    patch_skill_line_ability()
    print("=== PROCESO COMPLETADO ===")