-- ===========================================================
-- Parche Base acore_world: Night Elf Warlock (Raza 4 / Clase 9)
-- ===========================================================

-- 1. Posición e información de inicio (Teldrassil / Sombragénica)
DELETE FROM `playercreateinfo` WHERE `race` = 4 AND `class` = 9;
INSERT INTO `playercreateinfo` (`race`, `class`, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`)
SELECT 4, 9, `map`, `zone`, `position_x`, `position_y`, `position_z`, `orientation`
FROM `playercreateinfo` WHERE `race` = 4 AND `class` = 1 LIMIT 1;

-- 2. Barras de acción iniciales (Copiadas de Brujo - Gnomo, raza 7 clase 9)
DELETE FROM `playercreateinfo_action` WHERE `race` = 4 AND `class` = 9;
INSERT INTO `playercreateinfo_action` (`race`, `class`, `button`, `action`, `type`)
SELECT 4, 9, `button`, `action`, `type`
FROM `playercreateinfo_action`
WHERE `race` = 7 AND `class` = 9;