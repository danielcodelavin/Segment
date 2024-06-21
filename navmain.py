import rembg
import PIL
from naive import Naive
from rembg import remove_background

path = 'input.png' #image goes here
image = PIL.Image.open(path) 
image = image.convert("RGBA")
black = Naive().obtainblack(image)


#rembg 
#cleaned = remove_background(path,False)

#naive
naive = Naive().sweeper(cleaned,black)
