import PIL
from PIL import Image
import torch
#import tkinter
#from tkinter import ImageTk


def obtainblack(image):
    width, height = image.size
    corners = [image.getpixel((2, 2)), 
                image.getpixel((0, height-1)),
                image.getpixel((width-1, height-1)),
                image.getpixel((width-1, 0))]
    average = tuple(sum(x) // 4 for x in zip(*corners))
    return average # we get a three element tuple

def sweeper(image,black,tolerance):
    width, height = image.size
    maxblack = tuple(int(x * (1 + tolerance)) for x in black)
    minblack = tuple(int(x * (1 - tolerance)) for x in black)
    
    cluster_sizes = torch.tensor([])
    
    for x in range (0, width):
        for y in range (0, height):
            pixel = image.getpixel((x, y))
            if pixel > minblack and pixel < maxblack:
                # Check the 8 pixels around the current pixel
                for dx in [-1, 0, 1]:
                    for dy in [-1, 0, 1]:
                        if dx == 0 and dy == 0:
                            continue
                        neighbor_x = x + dx
                        neighbor_y = y + dy
                        if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                            neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
                            if neighbor_pixel > minblack and neighbor_pixel < maxblack:
                                # Start clustermode and call a new function
                                image, clusterlarge = clustereater(image, x, y, black, tolerance)
                                cluster_sizes = torch.cat((cluster_sizes, torch.tensor([clusterlarge])), 0)
                                break
                                
    return image, cluster_sizes
def clustereater(image, x, y, black, tolerance):
        clustersize: int = 0
        maxblack = tuple(int(x * (1 + tolerance)) for x in black)
        minblack = tuple(int(x * (1 - tolerance)) for x in black)
        width, height = image.size
        image.putpixel((x, y), (255, 255, 255, 0))
        #display.update(image)
        queue = [(x, y)]
        visited = set()
        visited.add((x, y))
        while queue:
            x, y = queue.pop(0)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor_x = x + dx
                    neighbor_y = y + dy
                    if 0 <= neighbor_x < width and 0 <= neighbor_y < height and (neighbor_x, neighbor_y) not in visited:
                        neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
                        if neighbor_pixel > minblack and neighbor_pixel < maxblack:
                            image.putpixel((neighbor_x, neighbor_y), (255, 255, 255, 0))
                            clustersize += 1
                            #display.update(image)
                            queue.append((neighbor_x, neighbor_y))
                            visited.add((neighbor_x, neighbor_y))
        return image , clustersize

def countvalidpixels(image):
        width, height = image.size
        count : int = 0
        for x in range(width):
            for y in range(height):
                r, g, b, a = image.getpixel((x, y))
                if a != 0:
                    count += 1
        return count



# def display(image):
#     root = tkinter.Tk()
#     def startdisp():
#         root = tkinter.Tk()
#         root.title("Image Viewer")
#         root.geometry("500x500")
#         label = tkinter.Label(root)
#         label.pack()
#     def update(image):
#         global label
#         img = ImageTk.PhotoImage(image)
#         label.configure(image=img)
#         label.image = img
#         root.update()

#     root.title("Image Viewer")
#     root.geometry("500x500")
#     label = tkinter.Label(root)
#     label.pack()












# import PIL
# from PIL import Image
# import torch
# #import tkinter
# #from tkinter import ImageTk


# def obtainblack(image):
#     width, height = image.size
#     corners = [image.getpixel((2, 2)), 
#                 image.getpixel((0, height-1)),
#                 image.getpixel((width-1, height-1)),
#                 image.getpixel((width-1, 0))]
#     average = tuple(sum(x) // 4 for x in zip(*corners))
#     return average # we get a three element tuple

# def sweeper(image,black,tolerance):
#     width, height = image.size
#     maxblack = tuple(int(x * (1 + tolerance)) for x in black)
#     minblack = tuple(int(x * (1 - tolerance)) for x in black)
    
#     cluster_sizes = torch.tensor([])
    
#     for x in range (0, width):
#         for y in range (0, height):
#             pixel = image.getpixel((x, y))
#             if pixel > minblack and pixel < maxblack:
#                 # Check the 8 pixels around the current pixel
#                 for dx in [-1, 0, 1]:
#                     for dy in [-1, 0, 1]:
#                         if dx == 0 and dy == 0:
#                             continue
#                         neighbor_x = x + dx
#                         neighbor_y = y + dy
#                         if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
#                             neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
#                             if neighbor_pixel > minblack and neighbor_pixel < maxblack:
#                                 # Start clustermode and call a new function
#                                 image, clusterlarge = clustereater(image, x, y, black, tolerance)
#                                 cluster_sizes = torch.cat((cluster_sizes, torch.tensor([clusterlarge])), 0)
#                                 break
                                
#     return image, cluster_sizes

# def clustereater(image, x, y, black, tolerance):
#         clustersize: int = 0
#         maxblack = tuple(int(x * (1 + tolerance)) for x in black)
#         minblack = tuple(int(x * (1 - tolerance)) for x in black)
#         width, height = image.size
#         image.putpixel((x, y), (255, 255, 255, 0))
#         #display.update(image)
#         queue = [(x, y)]
#         while queue:
#             x, y = queue.pop(0)
#             for dx in [-1, 0, 1]:
#                 for dy in [-1, 0, 1]:
#                     if dx == 0 and dy == 0:
#                         continue
#                     neighbor_x = x + dx
#                     neighbor_y = y + dy
#                     if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
#                         neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
#                         if neighbor_pixel > minblack and neighbor_pixel < maxblack:
#                             image.putpixel((neighbor_x, neighbor_y), (255, 255, 255, 0))
#                             clustersize += 1
#                             #display.update(image)
#                             queue.append((neighbor_x, neighbor_y))
#         return image , clustersize
        

# def countvalidpixels(image):
#         width, height = image.size
#         count : int = 0
#         for x in range(width):
#             for y in range(height):
#                 r, g, b, a = image.getpixel((x, y))
#                 if a != 0:
#                     count += 1
#         return count