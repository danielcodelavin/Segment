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

        
def sweeper(image,black):
    width, height = image.size
    maxblack = tuple(int(x * 1.02) for x in black)
    minblack = tuple(int(x * 0.98) for x in black)
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
                                image = clustereater(image, x, y, black)
                                break
    return image

def clustereater(image, x, y, black):
        maxblack = tuple(int(x * 1.02) for x in black)
        minblack = tuple(int(x * 0.98) for x in black)
        width, height = image.size
        image.putpixel((x, y), (255, 255, 255, 0))
        queue = [(x, y)]
        while queue:
            x, y = queue.pop(0)
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0:
                        continue
                    neighbor_x = x + dx
                    neighbor_y = y + dy
                    if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                        neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
                        if neighbor_pixel > minblack and neighbor_pixel < maxblack:
                            image.putpixel((neighbor_x, neighbor_y), (255, 255, 255, 0))
                            queue.append((neighbor_x, neighbor_y))
        return image
        

