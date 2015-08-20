If the TCOD-layout fonts index as if each row has 32 columsn, the code for fat
walls should start at 0x6F and go up to 0x79. The slim walls should go from 0x4F
up to 0x49. There are no fat-flat connector pieces in this font, as far as I can
see.

If it bases it on the CP437, it's 9, 12 (8, 11 if zero-indexed). That's 12*16+9,
or 0xC9.
 * The straight vertical piece is 0xCA.
 * The straight horizontal piece is 0xDC.
 * SE connector/NW corner is 0xD8.
 * SW connector/NE corner is 0xCB.
 * NE connector/SW corner is 13*16 + 7, or 0xD7.
 * NW connector/SE corner is 0xCC.
 * NWE connector is 0xD9.
 * SWE connector is 0xDA.
 * NSE connector is 0xDB.
 * NSW connector is 0xC9.
 * Four-way intersection is 0xDD.

In addition,
 * The vertical-fat horizontal-flat-right corner is 0xE6.
 * The flat horizontal line is 0xD5.
 * The vertical-fat horizontal-flat-left corner is 0xC7.
