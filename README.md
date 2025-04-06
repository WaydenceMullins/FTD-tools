## Block Data
BlockDataToTemplateBlocks.py reads data from every block and formats it as it is displayed in-game. Outputs it as [FTD Wiki](https://fromthedepths.wiki.gg/) infoboxes and into CSV file, which can also be found on Google Sheets: [Block Data as of game version 4.2.5](https://docs.google.com/spreadsheets/d/1gyJk6aXZHL1OD40w7u5dHzLXasJrUAi0EHHD6h8X6u8).
## Wiki Icons
Tools used to make block icons. [GIMP3](https://www.gimp.org/downloads/) and [AutoHotkey](https://www.autohotkey.com/) are required.

1. Spawn "greyscreen holder" into the game, spawn one of the greyscreen vehicles, attach it to the tractor beam
2. Turn off fullsreen, resize game window using AHK's Window Spy tool (usually to 900x900)
3. Focus on a greyscreen vehicle, zoom in, take screenshots
4. Open GIMP and create new image, usually 900x900, making sure that "Fill with" in "Advanced options" is set to "Transparency"
5. Drag and drop the screenshots into layers (bottom right)
6. Delete the Background layer, make sure that "Merge filter" is checked (can be found in Colors > Hue-Saturation)
7. Hit Alt+Z, enter the number of screenshots to edit, hit Enter twice
8. When it's done, a window prompting to export it will pop up. Choose a location and click Export.
9. Open the exported file as an archive (rename to .zip or use 7-Zip). The images can be found in data folder.
