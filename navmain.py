#import rembg
import PIL
from naive import obtainblack , sweeper ,   clustereater, countvalidpixels
#from rembg import remove_background
import torch

path = 'dataset/tester.jpeg' #image goes here
image = PIL.Image.open(path) 
image = image.convert("RGBA")
normalimagesize = image.size
black = obtainblack(image)

#initial cluster removal around the image gives us the "normal" size of the object

nobgimage, backg = clustereater(image, 3, 3, black)

objectsize = countvalidpixels(nobgimage)
objectsize_backup = normalimagesize - backg # these two should be the same in theory at least

#rembg 
#cleaned = remove_background(path,False)

#naive
naiveimg , clustersizes = sweeper(nobgimage,black)

clusteramount = len(clustersizes)


naiveimg.save("outputrmbg/tester1.png")
