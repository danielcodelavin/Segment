
import PIL
#import tkinter
from PIL import Image
from naive import obtainblack, sweeper, clustereater, countvalidpixels, debrissweeper
import torch
from rembg import remove
import io
#from display import display

path = 'dataset/onceler.jpeg'
outputpath = 'outputrmbg/testermini50deb.png'
image = PIL.Image.open(path)
image = image.convert("RGBA")
minimumcluster = 30
black = obtainblack(image)
tolerance = 0.5

maxdebrissize = 50
##### remove background with rembg before passing onto the clustereater
with open(path, 'rb') as i:
    input = i.read()
    output = remove(input)
    pil_image = Image.open(io.BytesIO(output))
    image = pil_image.convert("RGBA")

##### apply gaussian blur to the image before passing onto the clustereater

normalimagesize = countvalidpixels(image)

nobgimage, backg = clustereater(image, 3, 3, black, tolerance)

objectsize = countvalidpixels(nobgimage)

objectsize_backup = normalimagesize - backg

naiveimg, clustersizes = sweeper(nobgimage, black, tolerance, minimumcluster)
clustersizes = [int(x) for x in clustersizes]
average_cluster_size = sum(clustersizes) / len(clustersizes)
clustersum = sum(clustersizes)
objectwithoutcluster = objectsize - clustersum

density = objectwithoutcluster / objectsize_backup

###remove the debris stuff


#debrisimage = debrissweeper(naiveimg, maxdebrissize)
#etwa 40% farbtoleranz gut, check nochmal mit 0.3-0.5 in 0.02 schritten
# 0.3 seems a little more  lenient and kills fewer false clusters. maybe try to implement dynamic tolerance next
#0.5 better, 0.3 leaves artifacts

#######################################
#                 Todo                #
# add a "remnanteater" that kills the little specks of pixels around the image that are not part of the object
# this carries no mathematical purpose, but to produce a cleaner image
#######################################
clusteramount = len(clustersizes)

#debrisimage.save(outputpath)
with open("outputrmbg/reporttestermini50deb.txt", "w") as f:
    f.write("Copper Report: \n\n")
    f.write("All numbers here are expressed in terms of pixel count. If provided with an image scale and image size,\n one can easily convert these values to meaningful units. \n")
    f.write("Clusters are the holes within the object itself. \n\n")
    f.write("Normal Image Size: " + str(normalimagesize) + "\n")
    f.write("Background Pixels (without the holes in the object itself): " + str(backg) + "\n")
    f.write("Object Size: " + str(objectsize) + "\n")
    f.write("Object Size Backup: " + str(objectsize_backup) + "\n")
    f.write("Cluster Amount: " + str(clusteramount) + "\n")
    f.write("Cluster Sizes: " + str(clustersizes) + "\n")
    f.write("Cluster Sum: " + str(clustersum) + "\n")
    f.write("Average Cluster Size: " + str(average_cluster_size) + "\n")
    f.write("Object without Cluster: " + str(objectwithoutcluster) + "\n")
    f.write("Density: " + str(density) + "% \n")


#display(image, normalimagesize, nobgimage, objectsize, objectsize_backup, naiveimg, clustersizes, clusteramount)
