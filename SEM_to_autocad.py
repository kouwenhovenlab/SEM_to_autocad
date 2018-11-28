import os
import datetime
import subprocess
from os.path import basename
from pathlib import Path
from configparser import ConfigParser

# ======== Prompt =======

not_valid_dir = True
while (not_valid_dir):
    directory = input('Enter the directory with images: ')
    my_dir = Path(directory)
    while (my_dir.is_dir() != True):
        directory = input('Error: Not a directory, enter the directory with images: ')
        my_dir    = Path(directory)

    print("Compatible files in directory:")

    cnt_files = 0
    for filename in os.listdir(directory):
        if filename.endswith(".txt"): 
            # print(os.path.join(directory, filename))
            print(os.path.splitext(filename)[0])
            cnt_files = cnt_files + 1
            continue
        else:
            continue

    if cnt_files == 0:
        print("Error: No compatible files in this directory")
    else:
        not_valid_dir = False

   
    
reference_image = input('Enter the reference image (without extension): ')
my_file = Path(directory + '\\' + reference_image + '.txt')
while (my_file.is_file() != True):
    reference_image = input('Error: Not a file, enter the reference image: ')
    my_file = Path(directory + '\\' + reference_image + '.txt')

cad_x           = float(input('Enter AutoCAD X position: '))
cad_y           = float(input('Enter AutoCAD Y position: '))
cad_rotation    = float(input('Enter AutoCAD rotation: '))
cad_scale       = float(input('Enter AutoCAD scale (bitmarker .5, finemarker .2): '))
# ========================

# Delete current scriptfile
scriptfile = directory + '\\' + 'SEM_to_autocad_ref_'+reference_image+'.scr'
try:
    os.remove(scriptfile)
except OSError:
    pass

# Get reference data
config = ConfigParser()
config.read(directory + "/" + reference_image + ".txt")

if config.has_section('SemImageFile'):
    image_name   = config.get('SemImageFile', 'ImageName')
    ref_x        = config.getfloat('SemImageFile', 'StagePositionX')
    ref_y        = config.getfloat('SemImageFile', 'StagePositionY')
    ref_scale    = config.getfloat('SemImageFile', 'PixelSize')
    ref_rotation = config.getfloat('SemImageFile', 'StagePositionR')
else:
    print('Error: ' + directory + "/" + reference_image + " has no SEM data")
print('Reference image: ' + image_name)
print('AutoCAD position: ' + str(cad_x) + ', ' + str(cad_y))

def append_to_autocad_script(semimage, x, y, scale, rotation):
    global scriptfile
    s = '-ATTACH\n'
    s = s + semimage + '\n'
    s = s + str(x) + ',' + str(y) + '\n'
    s = s + str(scale) + '\n'
    s = s + str(rotation) + '\n'
    
    with open(scriptfile, 'a') as the_file:
        the_file.write(s)

def save_image_positions(filepath, filename):
    global scale
    global directory 
    config = ConfigParser()
    # parse existing file
    config.read(filepath)

    # read values from a section
    if config.has_section('SemImageFile'):
        image_name     = config.get('SemImageFile', 'ImageName')
        stage_x        = config.getfloat('SemImageFile', 'StagePositionX')
        stage_y        = config.getfloat('SemImageFile', 'StagePositionY')
        stage_scale    = config.getfloat('SemImageFile', 'PixelSize')
        stage_rotation = config.getfloat('SemImageFile', 'StagePositionR')
        
        delta_x    = ( stage_x - ref_x ) / 1000
        delta_y    = ( ref_y - stage_y ) / 1000

        orig_x     = float( cad_x + delta_x )
        orig_y     = float( cad_y + delta_y )

        orig_scale    = stage_scale / ref_scale * cad_scale
        orig_rotation = cad_rotation + stage_rotation - ref_rotation 

        print(image_name + ' | ' + str( orig_x ) + ', ' + str( orig_y ) )

        if (image_name != reference_image+'.tif'):
            append_to_autocad_script(directory + '\\' + image_name, orig_x, orig_y, orig_scale, orig_rotation)

# Get image positions
for filename in os.listdir(directory):
    if filename.endswith(".txt"): 
        # print(os.path.join(directory, filename))
        filepath = os.path.join(directory, filename)

        save_image_positions(filepath,filename)
        
        continue
    else:
        continue

print('')
print(' ============= Created SEM_to_autocad.scr ============= ')
print(' Excluded ' + reference_image + ' in import ' )
print('')
print(' Created import script: \n\t' + scriptfile)
print(' Drag the script into your autocad file to import the images')
subprocess.call("explorer "+directory, shell=True)

