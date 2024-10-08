from PIL import Image
import torch

def complexblack(image):
    width, height = image.size
    border_distance = 2

    # Check top and bottom borders
    for x in range(border_distance, width - border_distance):
        top_pixel = image.getpixel((x, border_distance))
        if top_pixel[3] != 0:  # Check alpha value
            return top_pixel , [x, border_distance]
        
        bottom_pixel = image.getpixel((x, height - border_distance - 1))
        if bottom_pixel[3] != 0:
            return bottom_pixel , [x, height - border_distance - 1]

    # Check left and right borders
    for y in range(border_distance, height - border_distance):
        left_pixel = image.getpixel((border_distance, y))
        if left_pixel[3] != 0:
            return left_pixel , [border_distance, y]
        
        right_pixel = image.getpixel((width - border_distance - 1, y))
        if right_pixel[3] != 0:
            return right_pixel , [width - border_distance - 1, y]

    # If no pixel with non-zero alpha is found
    return False

def collect_border_pixels(image, top=True, bottom=True, left=True, right=True):
    width, height = image.size
    border_distance = 2
    pixel_values = []

    # Check top and bottom borders
    if top or bottom:
        for x in range(border_distance, width - border_distance):
            if top:
                top_pixel = image.getpixel((x, border_distance))
                if top_pixel[3] != 0:  # Check alpha value
                    pixel_values.append(top_pixel)
            
            if bottom:
                bottom_pixel = image.getpixel((x, height - border_distance - 1))
                if bottom_pixel[3] != 0:
                    pixel_values.append(bottom_pixel)

    # Check left and right borders
    if left or right:
        for y in range(border_distance, height - border_distance):
            if left:
                left_pixel = image.getpixel((border_distance, y))
                if left_pixel[3] != 0:
                    pixel_values.append(left_pixel)
            
            if right:
                right_pixel = image.getpixel((width - border_distance - 1, y))
                if right_pixel[3] != 0:
                    pixel_values.append(right_pixel)

    # Remove duplicates by converting to a set and back to a list
    unique_pixel_values = list(set(pixel_values))

    return unique_pixel_values
def obtainblack(image):
    width, height = image.size
    corners = [image.getpixel((2, 2)), 
               image.getpixel((0, height-1)),
               image.getpixel((width-1, height-1)),
               image.getpixel((width-1, 0))]
    average = tuple(sum(x) // 4 for x in zip(*corners))
    return average  # we get a three-element tuple

def pixel_within_tolerance(pixel, minblack, maxblack):
    return all(minblack[i] <= pixel[i] <= maxblack[i] for i in range(3))
def pixel_transparent_checker(pixel):
    if isinstance(pixel, tuple) and len(pixel) == 4:
        return pixel[3] == 0
    else:
        return False

def sweeper(image, black, tolerance, minimumcluster):
    width, height = image.size
    maxblack = tuple(int(x * (1 + tolerance)) for x in black)
    minblack = tuple(int(x * (1 - tolerance)) for x in black)
    
    cluster_sizes = []
    
    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            if pixel_within_tolerance(pixel, minblack, maxblack):
                # Check if the cluster is large enough and doesn't border alpha == 0 pixels
                if miniclusterchecker(image, x, y, black, tolerance, min_size=minimumcluster):
                    # Start clustereater if cluster is large enough
                    image, cluster_size = clustereater(image, x, y, black, tolerance)
                    cluster_sizes.append(cluster_size)
                                
    return image, cluster_sizes

def miniclusterchecker(image, start_x, start_y, black, tolerance, min_size):
    maxblack = tuple(int(x * (1 + tolerance)) for x in black)
    minblack = tuple(int(x * (1 - tolerance)) for x in black)
    width, height = image.size
    
    queue = [(start_x, start_y)]
    visited = set()
    visited.add((start_x, start_y))
    cluster_size = 0
    borders_alpha_zero = False
    
    while queue and cluster_size < min_size:
        x, y = queue.pop(0)
        cluster_size += 1
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor_x = x + dx
                neighbor_y = y + dy
                if 0 <= neighbor_x < width and 0 <= neighbor_y < height and (neighbor_x, neighbor_y) not in visited:
                    neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
                    if pixel_transparent_checker(neighbor_pixel):
                        return False
                    if pixel_within_tolerance(neighbor_pixel, minblack, maxblack):
                    
                        queue.append((neighbor_x, neighbor_y))
                        visited.add((neighbor_x, neighbor_y))

    # Check if the cluster borders any alpha == 0 pixels
    return cluster_size >= min_size 

def clustereater(image, x, y, black, tolerance):
    clustersize = 1  # Initialize with 1 to count the starting pixel
    maxblack = tuple(int(x * (1 + tolerance)) for x in black)
    minblack = tuple(int(x * (1 - tolerance)) for x in black)
    width, height = image.size
    image.putpixel((x, y), (255, 255, 255, 0))
    queue = [(x, y)]
    visited = set()
    visited.add((x, y))
    
    while queue:
        cx, cy = queue.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor_x = cx + dx
                neighbor_y = cy + dy
                if 0 <= neighbor_x < width and 0 <= neighbor_y < height and (neighbor_x, neighbor_y) not in visited:
                    neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
                    if pixel_within_tolerance(neighbor_pixel, minblack, maxblack):
                        clustersize += 1
                        queue.append((neighbor_x, neighbor_y))
                        visited.add((neighbor_x, neighbor_y))
                    image.putpixel((neighbor_x, neighbor_y), (255, 255, 255, 0))
                        
    return image, clustersize

def countvalidpixels(image):
    width, height = image.size
    count = 0
    for x in range(width):
        for y in range(height):
            r, g, b, a = image.getpixel((x, y))
            if a != 0:
                count += 1
    return count



#ONLY FOR DERBIS -  DERELICT
def debrissweeper(image, min_cluster_size):
    width, height = image.size
    visited = set()
    
    for x in range(width):
        for y in range(height):
            if (x, y) not in visited:
                r, g, b, a = image.getpixel((x, y))
                if a != 0:  # Non-deleted pixel
                    cluster, size = check_cluster_size(image, x, y, visited)
                    if size < min_cluster_size:
                        # Remove the cluster if it's too small
                        for cx, cy in cluster:
                            image.putpixel((cx, cy), (255, 255, 255, 0))
    
    return image
#ONLY FOR DERBIS -  DERELICT
def check_cluster_size(image, start_x, start_y, visited):
    width, height = image.size
    queue = [(start_x, start_y)]
    cluster = set()
    cluster.add((start_x, start_y))
    visited.add((start_x, start_y))
    
    while queue:
        x, y = queue.pop(0)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                neighbor_x = x + dx
                neighbor_y = y + dy
                if 0 <= neighbor_x < width and 0 <= neighbor_y < height and (neighbor_x, neighbor_y) not in visited:
                    r, g, b, a = image.getpixel((neighbor_x, neighbor_y))
                    if a != 0:  # Non-deleted pixel
                        queue.append((neighbor_x, neighbor_y))
                        cluster.add((neighbor_x, neighbor_y))
                        visited.add((neighbor_x, neighbor_y))
    
    return cluster, len(cluster)
















# from PIL import Image
# import torch

# def complexblack(image):
#     width, height = image.size
#     border_distance = 2

#     # Check top and bottom borders
#     for x in range(border_distance, width - border_distance):
#         top_pixel = image.getpixel((x, border_distance))
#         if top_pixel[3] != 0:  # Check alpha value
#             return top_pixel , [x, border_distance]
        
#         bottom_pixel = image.getpixel((x, height - border_distance - 1))
#         if bottom_pixel[3] != 0:
#             return bottom_pixel , [x, height - border_distance - 1]

#     # Check left and right borders
#     for y in range(border_distance, height - border_distance):
#         left_pixel = image.getpixel((border_distance, y))
#         if left_pixel[3] != 0:
#             return left_pixel , [border_distance, y]
        
#         right_pixel = image.getpixel((width - border_distance - 1, y))
#         if right_pixel[3] != 0:
#             return right_pixel , [width - border_distance - 1, y]

#     # If no pixel with non-zero alpha is found
#     return False

# def obtainblack(image):
#     width, height = image.size
#     corners = [image.getpixel((2, 2)), 
#                image.getpixel((0, height-1)),
#                image.getpixel((width-1, height-1)),
#                image.getpixel((width-1, 0))]
#     average = tuple(sum(x) // 4 for x in zip(*corners))
#     return average  # we get a three-element tuple

# def pixel_within_tolerance(pixel, minblack, maxblack):
#     return all(minblack[i] <= pixel[i] <= maxblack[i] for i in range(3))

# def sweeper(image, black, tolerance,minimumcluster):
#     width, height = image.size
#     maxblack = tuple(int(x * (1 + tolerance)) for x in black)
#     minblack = tuple(int(x * (1 - tolerance)) for x in black)
    
#     cluster_sizes = []
    
#     for x in range(width):
#         for y in range(height):
#             pixel = image.getpixel((x, y))
#             if pixel_within_tolerance(pixel, minblack, maxblack):
#                 # Check if the cluster is large enough
#                 if miniclusterchecker(image, x, y, black, tolerance, min_size=minimumcluster):
#                     # Start clustereater if cluster is large enough
#                     image, cluster_size = clustereater(image, x, y, black, tolerance)
#                     cluster_sizes.append(cluster_size)
                                
#     return image, cluster_sizes

# def miniclusterchecker(image, start_x, start_y, black, tolerance, min_size):
#     maxblack = tuple(int(x * (1 + tolerance)) for x in black)
#     minblack = tuple(int(x * (1 - tolerance)) for x in black)
#     width, height = image.size
    
#     queue = [(start_x, start_y)]
#     visited = set()
#     visited.add((start_x, start_y))
#     cluster_size = 0
    
#     while queue and cluster_size < min_size:
#         x, y = queue.pop(0)
#         cluster_size += 1
#         for dx in [-1, 0, 1]:
#             for dy in [-1, 0, 1]:
#                 if dx == 0 and dy == 0:
#                     continue
#                 neighbor_x = x + dx
#                 neighbor_y = y + dy
#                 if 0 <= neighbor_x < width and 0 <= neighbor_y < height and (neighbor_x, neighbor_y) not in visited:
#                     neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
#                     if pixel_within_tolerance(neighbor_pixel, minblack, maxblack):
#                         queue.append((neighbor_x, neighbor_y))
#                         visited.add((neighbor_x, neighbor_y))
    
#     return cluster_size >= min_size

# def clustereater(image, x, y, black, tolerance):
#     clustersize = 1  # Initialize with 1 to count the starting pixel
#     maxblack = tuple(int(x * (1 + tolerance)) for x in black)
#     minblack = tuple(int(x * (1 - tolerance)) for x in black)
#     width, height = image.size
#     image.putpixel((x, y), (255, 255, 255, 0))
#     queue = [(x, y)]
#     visited = set()
#     visited.add((x, y))
#     while queue:
#         cx, cy = queue.pop(0)
#         for dx in [-1, 0, 1]:
#             for dy in [-1, 0, 1]:
#                 if dx == 0 and dy == 0:
#                     continue
#                 neighbor_x = cx + dx
#                 neighbor_y = cy + dy
#                 if 0 <= neighbor_x < width and 0 <= neighbor_y < height and (neighbor_x, neighbor_y) not in visited:
#                     neighbor_pixel = image.getpixel((neighbor_x, neighbor_y))
#                     image.putpixel((neighbor_x, neighbor_y), (255, 255, 255, 0))
#                     if pixel_within_tolerance(neighbor_pixel, minblack, maxblack):
                        
#                         clustersize += 1
#                         queue.append((neighbor_x, neighbor_y))
#                         visited.add((neighbor_x, neighbor_y))
                        
#     return image, clustersize

# def countvalidpixels(image):
#     width, height = image.size
#     count = 0
#     for x in range(width):
#         for y in range(height):
#             r, g, b, a = image.getpixel((x, y))
#             if a != 0:
#                 count += 1
#     return count

# def debrissweeper(image, min_cluster_size):
#     width, height = image.size
#     visited = set()
    
#     for x in range(width):
#         for y in range(height):
#             if (x, y) not in visited:
#                 r, g, b, a = image.getpixel((x, y))
#                 if a != 0:  # Non-deleted pixel
#                     cluster, size = check_cluster_size(image, x, y, visited)
#                     if size < min_cluster_size:
#                         # Remove the cluster if it's too small
#                         for cx, cy in cluster:
#                             image.putpixel((cx, cy), (255, 255, 255, 0))
    
#     return image

# def check_cluster_size(image, start_x, start_y, visited):
#     width, height = image.size
#     queue = [(start_x, start_y)]
#     cluster = set()
#     cluster.add((start_x, start_y))
#     visited.add((start_x, start_y))
    
#     while queue:
#         x, y = queue.pop(0)
#         for dx in [-1, 0, 1]:
#             for dy in [-1, 0, 1]:
#                 if dx == 0 and dy == 0:
#                     continue
#                 neighbor_x = x + dx
#                 neighbor_y = y + dy
#                 if 0 <= neighbor_x < width and 0 <= neighbor_y < height and (neighbor_x, neighbor_y) not in visited:
#                     r, g, b, a = image.getpixel((neighbor_x, neighbor_y))
#                     if a != 0:  # Non-deleted pixel
#                         queue.append((neighbor_x, neighbor_y))
#                         cluster.add((neighbor_x, neighbor_y))
#                         visited.add((neighbor_x, neighbor_y))
    
#     return cluster, len(cluster)

