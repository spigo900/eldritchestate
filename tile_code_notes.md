If the TCOD-layout fonts index as if each row has 32 columsn, the code for fat
walls should start at 0x6F and go up to 0x79. The slim walls should go from 0x4F
up to 0x49. There are no fat-flat connector pieces in this font, as far as I can
see.

If it bases it on the CP437, it's 9, 12 (8, 11 if zero-indexed). That's 12*16+9,
or 0xC9.
 * The straight vertical piece is 0xBA.
 * The straight horizontal piece is 0xCD.
 * SE connector/NW corner is 0xC9.
 * SW connector/NE corner is 0xBB.
 * NE connector/SW corner is 0xC8.
 * NW connector/SE corner is 0xBC.

 * NWE connector is 0xCA.
 * SWE connector is 0xC9.
 * NSE connector is 0xCC.
 * NSW connector is 0xB9.
 * Four-way intersection is 0xCE.

In addition,
 * The vertical-fat horizontal-flat-right corner is 0xE6.
 * The flat horizontal line is 0xD5.
 * The vertical-fat horizontal-flat-left corner is 0xC7.


For thin pieces:
 * The straight vertical piece is 0xB3.
 * The straight horizontal piece is 0xC4.
 * SE connector/NW corner is 0xDA.
 * SW connector/NE corner is 0xBF.
 * NE connector/SW corner is 0xC0.
 * NW connector/SE corner is 0xD9.

 * NWE connector is 0xC1.
 * SWE connector is 0xC2.
 * NSE connector is 0xC3.
 * NSW connector is 0xB4.
 * Four-way intersection is 0xC6.
