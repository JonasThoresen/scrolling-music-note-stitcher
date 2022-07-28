# Imports
import os
import glob
from numba import jit
import cv2
import math

# Vars
cv_images = []

HEIGHT_MAX = 500
height_val = math.floor(HEIGHT_MAX/2)

SCALE_MAX = 100
scale_val = math.floor(SCALE_MAX/2)

DISCARD_MAX = 100
discard_val = 0

VIEWPOINT_MAX = 10
viewpoint_val = 0


def create_score(score_path):
    """
    Creates a score from a series of images. 
    The images must be placed in the tmp folder.
    The images can be created using create_images.py.
    """

    # Starting OPENCV operation
    # Constants
    END_OF_HEADER = 120
    WINDOW_NAME = "Adjustment tool"

    # Create trackbar functions 
    def get_height(val):
        global height_val
        if val == 0:
            val = 1
        height_val = val
        update_image()

    def get_scale(val):
        global scale_val
        if val == 0:
            val = 1
        scale_val = val
        update_image()

    def get_discard(val):
        global discard_val
        discard_val = val
        update_image()

    def get_viewpoint(val):
        global viewpoint_val
        viewpoint_val = val
        update_image()

    # Create main cv2 function
    @jit # Jit specifies GPU processing
    def update_image(ret=False):
        processed_list = []
        global cv_images

        for i, src in enumerate(cv_images):
            if i == len(cv_images)-1:
                w = src.shape[1] # Get image width
                new_height = src.shape[0] # Get image height
                processed_list.append(src[END_OF_HEADER:new_height, 0:w])

            elif i >= len(cv_images) - discard_val:
                pass # Pass the last X amount of frames

            else:
                w = src.shape[1] # Get image width
                new_height = END_OF_HEADER + height_val
                processed_list.append(src[END_OF_HEADER:new_height, 0:w])

        global viewpoint_val
        if viewpoint_val != 0:
            processed_list = processed_list[viewpoint_val:]

        # Stack images
        build_image = cv2.vconcat(processed_list) 

        # Then scale
        cropped_h = build_image.shape[0]
        scaled_h = math.floor(cropped_h * (0.8 + 0.4*scale_val/SCALE_MAX))
        resized = cv2.resize(build_image, (w,scaled_h))

        # And show
        cv2.imshow(WINDOW_NAME, resized)

        if(ret):
            return resized

    # Start
    images = glob.glob(score_path + "\\*.jpg")
    sorted_images = sorted(images, key=lambda x: int(os.path.split(x)[-1].replace(".jpg","")))
    print(sorted_images)
    for image in sorted_images:
        cv_images.append(cv2.imread(image))

    # Process
    cv2.namedWindow(WINDOW_NAME) #, cv2.WINDOW_NORMAL
    cv2.createTrackbar("Height", WINDOW_NAME , height_val, HEIGHT_MAX, get_height)
    cv2.createTrackbar("Scale", WINDOW_NAME , scale_val, SCALE_MAX, get_scale)
    cv2.createTrackbar("Discard", WINDOW_NAME , discard_val, DISCARD_MAX, get_discard)
    cv2.createTrackbar("Viewpoint", WINDOW_NAME , viewpoint_val, VIEWPOINT_MAX, get_viewpoint)

    update_image()

    # Wait until user presses some key
    while(cv2.waitKey() != 113 or cv2.waitKey() != 81 or cv2.waitKey() != 83 or cv2.waitKey() != 115):
        if(cv2.waitKey() == 83 or cv2.waitKey() == 115):
            tmp_dir = SAVE_DIR + f"\\{os.path.basename(os.path.normpath(score_path))}.jpg"
            tmp_img = update_image(True)
            cv2.imwrite(tmp_dir, tmp_img)
            cv2.destroyAllWindows()
            return True
        else:
            cv2.destroyAllWindows()
            return False


# Set up Command Line Interface (CLI)
BASE_DIR = os.getcwd()
EXPORT_DIR = BASE_DIR + "\\Tmp"
SAVE_DIR = BASE_DIR + "\\Scores"
FOLDER_LIST = [SAVE_DIR]

EXIT_CLI = 99
EXIT_PROG = 100

# Make folders
def make_folder(folder):
    """ Creates the input folder if it does not exist """
    if not os.path.isdir(folder):
        os.makedirs(folder)

for folder in FOLDER_LIST:
    make_folder(folder)

cli = True
list_of_folders = [x[0] for x in os.walk(EXPORT_DIR)]
list_of_folders.pop(0) # Pop to remove parent folder
active_folders = [0 for folder in list_of_folders]

while(cli):
    for i, file in enumerate(list_of_folders):
        status = "(Skipping)"
        if active_folders[i]:
            status = "(Parsing)"
        print(f"[{i}] {os.path.basename(os.path.normpath(file))} {status}")
    print(f"[{len(list_of_folders)}] All Files")
    print(f"[{EXIT_CLI}] Continue")
    print(f"[{EXIT_PROG}] Exit Program")
    print(f"\nType any number to activate that file for parsing,"
            f"\n{len(list_of_folders)} to activate all files")
    user = input()
    parse_user = user.strip()

    try:
        int_user = int(parse_user)
        if int_user < len(list_of_folders):
            active_folders[int_user] = not active_folders[int_user]
        elif int_user == len(list_of_folders):
            active_folders = [1 for x in list_of_folders]
        elif int_user == EXIT_CLI:
            cli = False
        elif int_user == EXIT_PROG:
            print("Quitting")
            quit()
    except Exception as e:
        print(f"Not a number, or you have an error. {e}")

active_folder_names = [file for i, file in enumerate(list_of_folders) if active_folders[i] == 1]
for folder in active_folder_names:
    suc = create_score(folder)

    if suc:
        os.remove(folder)
