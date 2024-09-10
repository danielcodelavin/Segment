import tkinter as tk
from tkinter import filedialog, messagebox
import PIL
from PIL import Image

def naivemain(inputpath='dataset/default.jpg', 
              

              outputpath='outputrmbg/output.png', 
              scriptpath='outputrmbg/report.txt', 
              blacktolerance=0.5, 
              minimumclustersize=30, 
              maxdebrissize=50):
    from naive import obtainblack, sweeper, clustereater, countvalidpixels, debrissweeper

    image = Image.open(inputpath)
    image = image.convert("RGBA")

    black = obtainblack(image)
    normalimagesize = countvalidpixels(image)

    nobgimage, backg = clustereater(image, 3, 3, black, blacktolerance)

    objectsize = countvalidpixels(nobgimage)
    objectsize_backup = normalimagesize - backg

    naiveimg, clustersizes = sweeper(nobgimage, black, blacktolerance, minimumclustersize)
    clustersizes = [int(x) for x in clustersizes]
    average_cluster_size = sum(clustersizes) / len(clustersizes) if clustersizes else 0
    clustersum = sum(clustersizes)
    objectwithoutcluster = objectsize - clustersum

    density = objectwithoutcluster / objectsize_backup if objectsize_backup != 0 else 0

    debrisimage = debrissweeper(naiveimg, maxdebrissize)

    clusteramount = len(clustersizes)

    debrisimage.save(outputpath)

    with open(scriptpath, "w") as f:
        f.write("Copper Report: \n\n")
        f.write("All numbers here are expressed in terms of pixel count. If provided with an image scale and image size,\n one can easily convert these values to meaningful units. \n")
        f.write("Clusters are the holes within the object itself. \n\n")
        f.write(f"Normal Image Size: {normalimagesize}\n")
        f.write(f"Background Pixels (without the holes in the object itself): {backg}\n")
        f.write(f"Object Size: {objectsize}\n")
        f.write(f"Object Size Backup: {objectsize_backup}\n")
        f.write(f"Cluster Amount: {clusteramount}\n")
        f.write(f"Cluster Sizes: {clustersizes}\n")
        f.write(f"Cluster Sum: {clustersum}\n")
        f.write(f"Average Cluster Size: {average_cluster_size}\n")
        f.write(f"Object without Cluster: {objectwithoutcluster}\n")
        f.write(f"Density: {density:.2%}\n")

def compmain(inputpath='dataset/default.jpg', outputpath='outputrmbg/output.png', 
              scriptpath='outputrmbg/report.txt', 
              blacktolerance=0.5, 
              minimumclustersize=30, 
              maxdebrissize=50):
    from naive import obtainblack, sweeper, clustereater, countvalidpixels, debrissweeper, complexblack
    image = Image.open(inputpath)
    image = image.convert("RGBA")
    normalimagesize = countvalidpixels(image)
    backgroundsize = 0
    #removedpixels = 0
    all_cluster_sizes = []
    
    while complexblack(image) != False:
        black , pixel = complexblack(image)
        image , local = clustereater(image, pixel[0], pixel[1], black, blacktolerance)
        backgroundsize += local
        image, clustersizes = sweeper(image, black, blacktolerance, minimumclustersize)
        all_cluster_sizes.append(clustersizes)

    objectsize = countvalidpixels(image)
    clustersizes = [int(x) for x in clustersizes]
    average_cluster_size = sum(clustersizes) / len(clustersizes) if clustersizes else 0
    clustersum = sum(clustersizes)
    objectwithoutcluster = objectsize - clustersum

    density = objectsize/(objectsize + clustersum)

    debrisimage = debrissweeper(image, maxdebrissize)

    clusteramount = len(clustersizes)

    debrisimage.save(outputpath)
    with open(scriptpath, "w") as f:
        f.write("Copper Report: \n\n")
        f.write("All numbers here are expressed in terms of pixel count. If provided with an image scale and image size,\n one can easily convert these values to meaningful units. \n")
        f.write("Clusters are the holes within the object itself. \n\n")
        f.write(f"Normal Image Size: {normalimagesize}\n")
        f.write(f"Background Pixels (without the holes in the object itself): {backgroundsize}\n")
        f.write(f"Object Size: {objectsize}\n")
        f.write(f"Object Size Backup: {objectsize}\n")
        f.write(f"Cluster Amount: {clusteramount}\n")
        f.write(f"Cluster Sizes: {clustersizes}\n")
        f.write(f"Cluster Sum: {clustersum}\n")
        f.write(f"Average Cluster Size: {average_cluster_size}\n")
        f.write(f"Object without Cluster: {objectwithoutcluster}\n")
        f.write(f"Density: {density:.2%}\n")

def ai_main(inputpath, outputpath, 
              scriptpath, 
              blacktolerance=0.5, 
              minimumclustersize=30, 
              maxdebrissize=50):
    from naive import obtainblack, sweeper, clustereater, countvalidpixels, debrissweeper, complexblack, collect_border_pixels
    from removebg import remove_background

    rawimage = Image.open(inputpath)
    rawimage = rawimage.convert("RGBA")
    normalimagesize = countvalidpixels(rawimage)
    no_bg_image = remove_background(inputpath,False)
    borderpixels = collect_border_pixels(rawimage)
    cleaned_image = no_bg_image
    clusters = []
    for pixel in borderpixels:
        cleaned_image, tempclusters = sweeper(cleaned_image, pixel, blacktolerance, minimumclustersize)
        clusters.extend(tempclusters)
    density = countvalidpixels(cleaned_image) / countvalidpixels(no_bg_image)
    clusters = [int(x) for x in clusters]
    clustersum = sum(clusters)
    avg_cluster_size = sum(clusters) / len(clusters) if clusters else 0
    clusteramount = len(clusters)
    cleaned_image.save(outputpath)
    with open(scriptpath, "w") as f:
        f.write("Report: \n\n")
        f.write("All numbers here are expressed in terms of pixel count. If provided with an image scale and image size,\n one can easily convert these values to meaningful units. \n")
        f.write("Clusters are the holes within the object itself. \n\n")
        f.write(f"Normal Image Size: {normalimagesize}\n")
        f.write(f"Cluster Amount: {clusteramount}\n")
        f.write(f"Cluster Sizes: {clusters}\n")
        f.write(f"Cluster Sum: {clustersum}\n")
        f.write(f"Average Cluster Size: {avg_cluster_size}\n")
        f.write(f"Density: {density:.2%}\n")


def browse_input():
    input_path.set(filedialog.askopenfilename())

def browse_output():
    output_path.set(filedialog.askdirectory())

def browse_script():
    script_path.set(file ,dialog.asksaveasfilename(defaultextension=".txt"))

def run_function():


    try:
        input_file = input_path.get()
        output_dir = output_path.get()
        script_file = script_path.get()
        black_tol = float(black_tolerance.get())
        min_cluster = int(min_cluster_size.get())
        max_debris = int(max_debris_size.get())
        
        if not input_file or not output_dir or not script_file:
            raise ValueError("Input, output, and script paths are required.")
        
        naivemain(input_file, output_dir, script_file, black_tol, min_cluster, max_debris)
        messagebox.showinfo("Success", "Function executed successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


def run_comp_function():
    try:
        input_file = input_path.get()
        output_dir = output_path.get()
        script_file = script_path.get()
        black_tol = float(black_tolerance.get())
        min_cluster = int(min_cluster_size.get())
        max_debris = int(max_debris_size.get())
        
        if not input_file or not output_dir or not script_file:
            raise ValueError("Input, output, and script paths are required.")
        
        compmain(input_file, output_dir, script_file, black_tol, min_cluster, max_debris)
        messagebox.showinfo("Success", "Function executed successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")

def run_ai_main():
  
        input_file = input_path.get()
        output_dir = output_path.get()
        script_file = script_path.get()
        black_tol = float(black_tolerance.get())
        min_cluster = int(min_cluster_size.get())
        max_debris = int(max_debris_size.get())
        
        if not input_file or not output_dir or not script_file:
            raise ValueError("Input, output, and script paths are required.")
        
        ai_main(input_file, output_dir, script_file, black_tol, min_cluster, max_debris)
        messagebox.showinfo("Success", "Function executed successfully!")
   
# Create the main window
root = tk.Tk()
root.title("Naive Main GUI")
root.geometry("1200x900")

# Create and set up variables with default values
input_path = tk.StringVar(value='dataset/onceler.jpeg')
output_path = tk.StringVar(value='outputrmbg/aaoutput.png')
script_path = tk.StringVar(value='outputrmbg/aareport.txt')
black_tolerance = tk.StringVar(value="0.5")
min_cluster_size = tk.StringVar(value="30")
max_debris_size = tk.StringVar(value="50")

tk.Label(root, text="Input Path:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=input_path, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_input).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output Path:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_output).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Script Path:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=script_path, width=50).grid(row=2, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_script).grid(row=2, column=2, padx=5, pady=5)

tk.Label(root, text="Black Tolerance:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=black_tolerance, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Minimum Cluster Size:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=min_cluster_size, width=10).grid(row=4, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Max Debris Size:").grid(row=5, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=max_debris_size, width=10).grid(row=5, column=1, sticky="w", padx=5, pady=5)

# Place the buttons next to each other
tk.Button(root, text="Run Naive Function", command=run_function).grid(row=6, column=1, pady=10, sticky="e", padx=(0, 10))
tk.Button(root, text="Run Complex Function", command=run_comp_function).grid(row=6, column=2, pady=10, sticky="w", padx=(10, 0))
tk.Button(root, text="AI-Function", command=run_ai_main).grid(row=6, column=3, pady=10, sticky="w", padx=(10, 0))


# Create a Text widget for static text
static_text = tk.Text(root, height=50, width=150, wrap=tk.WORD)
static_text.grid(row=7, column=0, columnspan=3, padx=5, pady=5)
static_text.insert(tk.END, """
# Naive Image Processing Tool

This tool removes image backgrounds and identifies clusters.

## Parameters:

1. **Black Tolerance** (default: 0.5, range: 0.0-1.0):
   - Defines how lenient we are when removing background - Higher : More removed.
2. **Minimum Cluster Size** (default: 30):
   - A cluster of background pixel has to be this size to be removed - Higher : Keep more smaller clusters

3. **Max Debris Size** (default: 50):
   - Leftover Clusters of frontground pixels have to be smaller than this to be removed - Higher : Keep fewer small clusters

## Process:

1. Identifies background color
2. Removes background
3. Processes clusters - removes clusters
4. Removes small debris
5. Saves image and report

## Tips:

- Start with defaults, then adjust.
- Increase Black Tolerance if too much background remains.
- Adjust Minimum Cluster Size for detail vs. noise balance.
- Use Max Debris Size for final clean-up.

Click "Run Function" to process with current settings.
""")
static_text.config(state=tk.DISABLED)  # Make it read-

if __name__ == "__main__":
    root.mainloop()