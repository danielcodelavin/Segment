import PIL
from PIL import Image



    #idea, brute force, take samples every two steps and check if they are background or black, get the definition of black from the corners
    # try to more or less compare to the black (a range) and if so, start a new function which clusters them together

def obtainblack(image):
    width, height = image.size
    corners = [image.getpixel((2, 2)), 
                image.getpixel((0, height-1)),
                image.getpixel((width-1, height-1)),
                image.getpixel((width-1, 0))]
    average = sum(corners, (0, 0, 0)) // 4
    return average # we get a three element tuple

        
def randomsampler():
        pass