# Imports
import os
import glob
from numba import jit
import cv2
import math
import shutil

# Command Line Interface (CLI) variables
BASE_DIR = os.getcwd()
IMPORT_DIR = BASE_DIR + '\\Import'
EXPORT_DIR = BASE_DIR + '\\Tmp'
SAVE_DIR = BASE_DIR + '\\Scores'
DONE_DIR = IMPORT_DIR + '\\Done'
FOLDER_LIST = [EXPORT_DIR, SAVE_DIR, DONE_DIR]

EXIT_CLI = 99
EXIT_PROG = 100

# Editor variables
cv_images = []
HEIGHT_MAX = 500
height_val = math.floor(HEIGHT_MAX/2)
SCALE_MAX = 100
scale_val = math.floor(SCALE_MAX/2)
DISCARD_MAX = 100
discard_val = 0
VIEWPOINT_MAX = 10
viewpoint_val = 0

# Make folders
def make_folder(folder):
    if not os.path.isdir(folder):
        os.makedirs(folder)

for folder in FOLDER_LIST:
    make_folder(folder)

# Command line interface to choose files
cli = True
list_of_files = glob.glob(IMPORT_DIR+'\\*.mp4')
active_files = [0 for x in list_of_files]

while(cli):
    for i, file in enumerate(list_of_files):
        status = '(Skipping)'
        if active_files[i]:
            status = '(Parsing)'
        print(f'[{i}] {os.path.basename(file)[:-4]} {status}')
    print(f"[{len(list_of_files)}] All Files")
    print(f"[{EXIT_CLI}] Continue")
    print(f"[{EXIT_PROG}] Exit Program")
    print(f"\nType any number to activate that file for parsing,"
            f"\n{len(list_of_files)} to activate all files")
    user = input()
    parse_user = user.strip()

    try:
        int_user = int(parse_user)
        if int_user < len(list_of_files):
            active_files[int_user] = not active_files[int_user]
        elif int_user == len(list_of_files):
            active_files = [1 for x in list_of_files]
        elif int_user == EXIT_CLI:
            cli = False
        elif int_user == EXIT_PROG:
            print("Quitting")
            quit()
    except Exception as e:
        print(f'That is not a number or you have an error: {e}')

active_file_names = [file for i, file in enumerate(list_of_files) if active_files[i] == 1]

# Set up video to JPG converter
SKIP_X_FILES = 300

@jit # Jit to enable GPU processing
def extract_images(path):
    export_path = EXPORT_DIR + '\\' + os.path.basename(path)[0:-4]
    make_folder(export_path) # Create savefolder

    capture_image = cv2.VideoCapture(path) 
    frame_count = 0 
    userSkipFrames = SKIP_X_FILES  # each x-th frame is captured

	# Change working dir
    os.chdir(export_path)
    i=userSkipFrames
    j = 0

    # Reading each frame
    while (True): 
        con,frames = capture_image.read() 
        if con:     # con will test until last frame is extracted 
            if(i >= userSkipFrames):
                # Giving names to each frame and printing while extracting
                name = str(j)+'.jpg'
                print('Capturing --- '+name)
                cv2.imwrite(name, frames) 
                i = 1
                j += 1
            else:
                 i += 1
            frame_count = frame_count + 1
        else:
            break
    
    os.chdir(BASE_DIR)

# Main loop after CLI
for file in active_file_names:
    # Extract images
    extract_images(file)

    # Done with extracting, now move file
    shutil.move(file, DONE_DIR)