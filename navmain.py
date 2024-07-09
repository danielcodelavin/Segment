
import PIL
#import tkinter

from naive import obtainblack, sweeper, clustereater, countvalidpixels
import torch
#from display import display

path = 'dataset/onceler.jpeg'
outputpath = 'outputrmbg/testermini50.png'
image = PIL.Image.open(path)
image = image.convert("RGBA")
minimumcluster = 50
black = obtainblack(image)
tolerance = 0.5

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

#etwa 40% farbtoleranz gut, check nochmal mit 0.3-0.5 in 0.02 schritten
# 0.3 seems a little more  lenient and kills fewer false clusters. maybe try to implement dynamic tolerance next


clusteramount = len(clustersizes)

naiveimg.save(outputpath)
with open("outputrmbg/reporttestermini50.txt", "w") as f:
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
