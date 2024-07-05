
import PIL


from naive import obtainblack, sweeper, clustereater, countvalidpixels
import torch
from display import display

path = 'dataset/tester.jpeg'
image = PIL.Image.open(path)
image = image.convert("RGBA")
normalimagesize = image.size
black = obtainblack(image)



nobgimage, backg = clustereater(image, 3, 3, black)

objectsize = countvalidpixels(nobgimage)

objectsize_backup = normalimagesize - backg



naiveimg, clustersizes = sweeper(nobgimage, black)




clusteramount = len(clustersizes)

naiveimg.save("outputrmbg/tester1.png")


display(image, normalimagesize, nobgimage, objectsize, objectsize_backup, naiveimg, clustersizes, clusteramount)
