import rembg
import PIL
from naive import Naive
from rembg import remove_background


image = PIL.Image.open('input.png') #image goes here
black = Naive().obtainblack(image)
