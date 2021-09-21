# python_imageprocessing

A quick repo for my python scripts to process a bunch of images. The following steps are done via the python scripts inside the `scripts` folder.

# Scripts

## `info.py`
This script iterates over the pictures inside the given folder (`path` variable) and print out the width and height of the pictures. Additionaly at the end the scripts reports how many pictures didn't satisfy the height and width condition or both.

## `pngify.py`
This script converts all pictures inside the given folder (`path` variable) to `.png`. The pictures are save in the directory specified in the `output` variable.

## `rename.py`
Just renames all files in the directory (`path` variable) to a numeric sequence.

## `check_duplicate.py`
This script simple uses this [github repo](https://github.com/elisemercury/Duplicate-Image-Finder/blob/main/dupl_image_finder.py) and adds a part to execute it to check for duplicate pictures inside the folder

## `upscale.py`
This script reads the files inside the folder defined in the `path` variable and upscales the picture by the factor 2. This done with the `dnn_superres` from `cv2` with the `ESPCN_x2` model. The upscaled images are saved in the directory specified in the `output` variable.

## `diashow.py`
This is the final step which takes all images inside the `2x` directory and reads them into a custom class which enables blending two images with the `cv2.addWeigthed()` function. With those objects a movie file is created via the `cv2.VideoWriter` inside the `output` directory named `output.mp4`. The width and height for the final video are stored in the variables `HEIGHT` and `WIDTH` at the top of the script. The images get displayed for 100 frames and a transition takes 50 frames. The Video is 30frames/sec.
