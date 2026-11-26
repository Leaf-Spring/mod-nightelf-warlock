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

-- 3. Skills (competencia de armas de Brujo para Elfo de la Noche: raceMask = 8, classMask = 256)
DELETE FROM `playercreateinfo_skills`
WHERE `raceMask` = 8 AND `classMask` = 256
  AND `skill` IN (173, 43, 136, 228, 162);

INSERT INTO `playercreateinfo_skills` (`raceMask`, `classMask`, `skill`, `rank`, `comment`) VALUES
(8, 256, 173, 0, 'Night Elf Warlock - Daggers'),
(8, 256, 43,  0, 'Night Elf Warlock - Swords'),
(8, 256, 136, 0, 'Night Elf Warlock - Staves'),
(8, 256, 228, 0, 'Night Elf Warlock - Wands'),
(8, 256, 162, 0, 'Night Elf Warlock - Unarmed');