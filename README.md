# SEM_to_autocad
Creates a .scr file that imports SEM images into AutoCAD according to the meta files.
*This script is specifically designed for the Hitachi S4800 but you can edit it easily.*

# Needed:
- Directory with SEM images (.tif) and meta files (.txt), they should have the same name!
- Your AutoCAD file should correspond to 1 unit length is 1 um


# Usage:
1. You need to align one of the SEM images to get a relative position
2. Write down the **position** (x and y), **rotation** and **scale**
3. Run the script
4. After the script is done a file is made in the same directory, drag this into your AutoCAD and accept the popup

All the images in the directory are imported into your AutoCAD and you can align them using the **ALIGN** tool
