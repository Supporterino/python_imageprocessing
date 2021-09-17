# python_imageprocessing

A quick repo for my python scripts to process a bunch of images. The following steps are done via the python scripts inside the `scripts` folder.

# Scripts

## `diashow.py`
This is the final step which takes all images inside the `2x` directory and reads them into a custom class which enables blending two images with the `cv2.addWeigthed()` function. With those objects a movie file is created via the `cv2.VideoWriter` inside the `output` directory named `output.mp4`. The width and height for the final video are stored in the variables `HEIGHT` and `WIDTH` at the top of the script. The images get displayed for 100 frames and a transition takes 50 frames. The Video is 30frames/sec.
