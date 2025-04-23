import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import os
import io
from scipy import ndimage

# Import functions from naive.py
from naive import (
    obtainblack, sweeper, clustereater, countvalidpixels, 
    collect_border_pixels, find_border_clusters, is_black
)
from removebg import remove_background

class PorosityAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Metal Porosity Analyzer")
        self.root.geometry("1200x800")
        
        # Style configuration
        self.style = ttk.Style()
        self.style.configure('TButton', padding=6)
        self.style.configure('TLabel', padding=4)
        self.style.configure('TFrame', padding=8)
        
        # Variables
        self.input_path = tk.StringVar()
        self.output_dir = tk.StringVar(value='output')
        self.output_file = tk.StringVar(value='processed_image.png')
        self.report_file = tk.StringVar(value='report.txt')
        self.black_tolerance = tk.DoubleVar(value=0.6)
        self.min_cluster_size = tk.IntVar(value=25)
        self.edge_width = tk.IntVar(value=35)  # Default edge width of 40 pixels
        
        # Border variables
        self.top_var = tk.BooleanVar(value=True)
        self.bottom_var = tk.BooleanVar(value=True)
        self.left_var = tk.BooleanVar(value=True)
        self.right_var = tk.BooleanVar(value=True)
        
        # State variables
        self.current_image = None
        self.processed_image = None
        self.no_bg_image = None
        self.current_holes = None
        self.show_overlay = tk.BooleanVar(value=True)
        
        # Create UI
        self.create_frames()
        self.create_input_section()
        self.create_parameter_section()
        self.create_preview_section()
        
    def create_frames(self):
        # Main container
        self.main_container = ttk.Frame(self.root, padding="10")
        self.main_container.grid(row=0, column=0, sticky="nsew")
        
        # Left panel for controls
        self.control_panel = ttk.Frame(self.main_container)
        self.control_panel.grid(row=0, column=0, sticky="nsew", padx=10)
        
        # Right panel for preview
        self.preview_panel = ttk.Frame(self.main_container)
        self.preview_panel.grid(row=0, column=1, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.main_container.grid_columnconfigure(1, weight=3)
        self.main_container.grid_rowconfigure(0, weight=1)
        
    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.control_panel, text="File Selection", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Label(input_frame, text="Input Image:").grid(row=0, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.input_path).grid(row=1, column=0, sticky="ew")
        ttk.Button(input_frame, text="Browse", command=self.browse_input).grid(row=1, column=1, padx=5)
        
        ttk.Label(input_frame, text="Output Directory:").grid(row=2, column=0, sticky="w", pady=(10,0))
        ttk.Entry(input_frame, textvariable=self.output_dir).grid(row=3, column=0, sticky="ew")
        ttk.Button(input_frame, text="Browse", command=self.browse_output_dir).grid(row=3, column=1, padx=5)
        
        ttk.Label(input_frame, text="Output Filename:").grid(row=4, column=0, sticky="w", pady=(10,0))
        ttk.Entry(input_frame, textvariable=self.output_file).grid(row=5, column=0, sticky="ew")
        
        ttk.Label(input_frame, text="Report Filename:").grid(row=6, column=0, sticky="w", pady=(10,0))
        ttk.Entry(input_frame, textvariable=self.report_file).grid(row=7, column=0, sticky="ew")
        
    def create_parameter_section(self):
        param_frame = ttk.LabelFrame(self.control_panel, text="Processing Parameters", padding="10")
        param_frame.grid(row=1, column=0, sticky="ew", pady=5)
        
        # Black tolerance
        ttk.Label(param_frame, text="Black Tolerance:").grid(row=0, column=0, sticky="w")
        tol_frame = ttk.Frame(param_frame)
        tol_frame.grid(row=1, column=0, sticky="ew")
        
        self.tol_label = tk.Label(tol_frame, text=f"{self.black_tolerance.get():.2f}")
        self.tol_label.grid(row=0, column=1, padx=5)
        
        tol_scale = ttk.Scale(tol_frame, from_=0.1, to=1.0, variable=self.black_tolerance,
                            orient="horizontal", command=lambda v: self.tol_label.config(text=f"{float(v):.2f}"))
        tol_scale.grid(row=0, column=0, sticky="ew")
        
        # Minimum cluster size
        ttk.Label(param_frame, text="Minimum Cluster Size:").grid(row=2, column=0, sticky="w", pady=(10,0))
        min_frame = ttk.Frame(param_frame)
        min_frame.grid(row=3, column=0, sticky="ew")
        
        self.min_size_label = tk.Label(min_frame, text=self.min_cluster_size.get())
        self.min_size_label.grid(row=0, column=1, padx=5)
        
        min_scale = ttk.Scale(min_frame, from_=10, to=100, variable=self.min_cluster_size,
                            orient="horizontal", command=lambda v: self.min_size_label.config(text=f"{int(float(v))}"))
        min_scale.grid(row=0, column=0, sticky="ew")
        
        # Edge width slider
        ttk.Label(param_frame, text="Edge Width (pixels):").grid(row=4, column=0, sticky="w", pady=(10,0))
        edge_frame = ttk.Frame(param_frame)
        edge_frame.grid(row=5, column=0, sticky="ew")
        
        self.edge_width_label = tk.Label(edge_frame, text=self.edge_width.get())
        self.edge_width_label.grid(row=0, column=1, padx=5)
        
        edge_scale = ttk.Scale(edge_frame, from_=5, to=100, variable=self.edge_width,
                            orient="horizontal", command=lambda v: self.edge_width_label.config(text=f"{int(float(v))}"))
        edge_scale.grid(row=0, column=0, sticky="ew")
        
        # Border checkboxes
        border_frame = ttk.LabelFrame(param_frame, text="Border Selection", padding="10")
        border_frame.grid(row=6, column=0, sticky="ew", pady=(10,0))
        
        ttk.Checkbutton(border_frame, text="Top", variable=self.top_var).grid(row=0, column=0, sticky="w")
        ttk.Checkbutton(border_frame, text="Bottom", variable=self.bottom_var).grid(row=0, column=1, sticky="w")
        ttk.Checkbutton(border_frame, text="Left", variable=self.left_var).grid(row=1, column=0, sticky="w")
        ttk.Checkbutton(border_frame, text="Right", variable=self.right_var).grid(row=1, column=1, sticky="w")
        
        # Show overlay checkbox
        ttk.Checkbutton(param_frame, text="Show Hole Detection Overlay", 
                       variable=self.show_overlay,
                       command=self.toggle_overlay).grid(row=7, column=0, sticky="w", pady=5)
        
        # Process buttons
        button_frame = ttk.Frame(param_frame)
        button_frame.grid(row=8, column=0, sticky="ew", pady=10)
        
        ttk.Button(button_frame, text="Process Image", 
                  command=self.process_image_ui).grid(row=0, column=0, padx=5, sticky="ew")
        ttk.Button(button_frame, text="Save No-BG Only", 
                  command=self.save_nobg_only).grid(row=0, column=1, padx=5, sticky="ew")
                  
        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)
        
    def create_preview_section(self):
        preview_frame = ttk.LabelFrame(self.preview_panel, text="Preview", padding="10")
        preview_frame.grid(row=0, column=0, sticky="nsew")
        
        self.preview_canvas = tk.Canvas(preview_frame, bg='white')
        self.preview_canvas.grid(row=0, column=0, sticky="nsew")
        
        self.preview_panel.grid_rowconfigure(0, weight=1)
        self.preview_panel.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
        # Add explanation text below canvas
        explanation_frame = ttk.LabelFrame(self.preview_panel, text="Process Information", padding="10")
        explanation_frame.grid(row=1, column=0, sticky="ew", pady=10)
        
        explanation_text = """
Improved Porosity Analysis Workflow:

1. Remove background with rembg
2. Create a protected edge zone to avoid processing edge artifacts
3. Obtain reference "black" color for hole detection
4. Identify and remove holes in the interior region only
5. Generate comprehensive porosity report

Parameters:
- Black Tolerance: Defines how lenient we are when detecting holes (higher = more removed)
- Minimum Cluster Size: Clusters smaller than this won't be considered holes
- Edge Width: Width of the border zone that will be protected from hole detection (pixels)
- Border Selection: Choose which borders to analyze for initial color reference

This approach preserves edges while accurately identifying and measuring porosity in interior regions.
"""
        ttk.Label(explanation_frame, text=explanation_text, justify="left", wraplength=600).grid(row=0, column=0, sticky="ew")
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp")])
        if filename:
            self.input_path.set(filename)
            self.load_and_preview(filename)
            
    def browse_output_dir(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.output_dir.set(dirname)
            
    def load_and_preview(self, image_path):
        try:
            image = Image.open(image_path)
            self.current_image = image.convert("RGBA")
            self.update_preview(self.current_image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def update_preview(self, image, holes=None):
        if image:
            # Calculate aspect ratio and resize maintaining ratio
            aspect_ratio = image.width / image.height
            max_size = 600
            
            if aspect_ratio > 1:
                new_width = max_size
                new_height = int(max_size / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(max_size * aspect_ratio)
                
            display_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # If holes provided and overlay enabled, draw them
            if holes and self.show_overlay.get():
                display_array = np.array(display_image)
                scale_factor = new_width / image.width
                
                # Draw semi-transparent green overlay
                overlay = np.zeros_like(display_array)
                for y, x in holes:
                    new_y = int(y * scale_factor)
                    new_x = int(x * scale_factor)
                    if 0 <= new_y < new_height and 0 <= new_x < new_width:
                        if display_array[new_y, new_x, 3] > 0:  # Only overlay non-transparent pixels
                            overlay[new_y, new_x] = [0, 255, 0, 128]
                
                # Blend overlay with display image
                mask = overlay[:, :, 3:4] / 255.0
                display_array = display_array * (1 - mask) + overlay * mask
                display_image = Image.fromarray(display_array.astype(np.uint8))
            
            photo = ImageTk.PhotoImage(display_image)
            
            # Update canvas
            self.preview_canvas.config(width=new_width, height=new_height)
            self.preview_canvas.delete("all")
            self.preview_canvas.create_image(new_width/2, new_height/2, image=photo, anchor="center")
            self.preview_canvas.image = photo  # Keep a reference to prevent garbage collection
    
    def toggle_overlay(self):
        if self.processed_image and self.current_holes:
            self.update_preview(self.processed_image, self.current_holes)
    
    def save_nobg_only(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input image.")
            return
            
        try:
            # Create output directory
            os.makedirs(self.output_dir.get(), exist_ok=True)
            
            # Get paths
            input_path = self.input_path.get()
            output_path = os.path.join(self.output_dir.get(), "nobg_" + self.output_file.get())
            
            # Remove background only
            no_bg_image = remove_background(input_path, False)
            no_bg_image.save(output_path)
            
            # Update preview
            self.no_bg_image = no_bg_image
            self.update_preview(no_bg_image)
            
            messagebox.showinfo("Success", "Background removed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
    
    def process_image_ui(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input image.")
            return
            
        try:
            # Create output directory
            os.makedirs(self.output_dir.get(), exist_ok=True)
            
            # Get paths
            input_path = self.input_path.get()
            output_path = os.path.join(self.output_dir.get(), self.output_file.get())
            report_path = os.path.join(self.output_dir.get(), self.report_file.get())
            
            # Process image
            processed_image, hole_pixels, stats = self.process_image(
                input_path, 
                self.black_tolerance.get(),
                self.min_cluster_size.get(),
                self.top_var.get(),
                self.bottom_var.get(),
                self.left_var.get(),
                self.right_var.get()
            )
            
            # Save results
            processed_image.save(output_path)
            self.generate_report(report_path, stats)
            
            # Update preview with processed image
            self.processed_image = processed_image
            self.current_holes = hole_pixels
            self.update_preview(processed_image, hole_pixels if self.show_overlay.get() else None)
            
            messagebox.showinfo("Success", "Image processed successfully!")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
    
    def process_image(self, input_path, black_tolerance, minimum_cluster_size, top, bottom, left, right):
        """Process the image using a simpler, more reliable approach that ignores edge regions"""
        # Step 1: Load the image
        raw_image = Image.open(input_path)
        raw_image = raw_image.convert("RGBA")
        normal_image_size = countvalidpixels(raw_image)
        
        # Step 2: Remove background using rembg
        no_bg_image = remove_background(input_path, False)
        no_bg_size = countvalidpixels(no_bg_image)
        
        # Step 3: Create a mask of the non-transparent pixels
        width, height = no_bg_image.size
        object_mask = np.zeros((height, width), dtype=bool)
        for y in range(height):
            for x in range(width):
                object_mask[y, x] = no_bg_image.getpixel((x, y))[3] > 0
        
        # Step 4: Create an interior mask by eroding the object mask
        # This gives us a "safe zone" that's definitely not edge pixels
        # Use the edge width from the slider
        edge_width = self.edge_width.get()
        interior_mask = ndimage.binary_erosion(object_mask, iterations=edge_width)
        
        # Step 5: Obtain the black color reference from the original image
        black = obtainblack(raw_image)
        maxblack = tuple(int(min(x * (1 + black_tolerance), 255)) for x in black)
        minblack = tuple(int(max(x * (1 - black_tolerance), 0)) for x in black)
        
        # Step 6: Detect and remove holes in the interior region only
        cleaned_image = no_bg_image.copy()
        clusters = []
        
        # Create a debug image showing the interior mask
        debug_image = no_bg_image.copy()
        for y in range(height):
            for x in range(width):
                if object_mask[y, x] and not interior_mask[y, x]:
                    # This is an edge pixel (in the border zone) - color it red
                    debug_image.putpixel((x, y), (255, 0, 0, 255))
        
        debug_path = os.path.join(self.output_dir.get(), "debug_mask.png")
        debug_image.save(debug_path)
        
        # Find hole candidates inside the interior mask
        potential_holes = []
        for y in range(height):
            for x in range(width):
                if interior_mask[y, x]:  # Only look in the interior region
                    pixel = no_bg_image.getpixel((x, y))
                    r, g, b, a = pixel
                    # Check if it's a potential hole based on color
                    if all(minblack[i] <= [r, g, b][i] <= maxblack[i] for i in range(3)):
                        potential_holes.append((x, y))
        
        # Process each potential hole using connected components
        visited = set()
        for start_x, start_y in potential_holes:
            if (start_x, start_y) in visited or cleaned_image.getpixel((start_x, start_y))[3] == 0:
                continue
                
            # Start a new cluster
            cluster = []
            queue = [(start_x, start_y)]
            local_visited = set([(start_x, start_y)])
            
            # Flood fill to find the entire connected component
            while queue:
                x, y = queue.pop(0)
                visited.add((x, y))
                pixel = cleaned_image.getpixel((x, y))
                r, g, b, a = pixel
                
                # If this is a hole pixel (dark enough)
                if a > 0 and all(minblack[i] <= [r, g, b][i] <= maxblack[i] for i in range(3)):
                    cluster.append((x, y))
                    
                    # Check neighbors (4-connected)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < width and 0 <= ny < height and 
                            (nx, ny) not in local_visited and 
                            interior_mask[ny, nx]):  # Only check interior pixels
                            queue.append((nx, ny))
                            local_visited.add((nx, ny))
            
            # Remove the cluster if it's large enough
            if len(cluster) >= minimum_cluster_size:
                for x, y in cluster:
                    cleaned_image.putpixel((x, y), (0, 0, 0, 0))  # Make transparent
                clusters.append(len(cluster))
        
        # Collect all hole pixels for visualization
        all_hole_pixels = []
        for y in range(height):
            for x in range(width):
                if (no_bg_image.getpixel((x, y))[3] != 0 and 
                    cleaned_image.getpixel((x, y))[3] == 0):
                    all_hole_pixels.append((y, x))  # Note: y,x order for visualization
        
        # Calculate statistics
        stats = self.check_results(cleaned_image, clusters, normal_image_size, no_bg_size)
        
        return cleaned_image, all_hole_pixels, stats
    
    def check_results(self, cleaned_image, clusters, normal_image_size, no_bg_size):
        """Calculate statistics from processed image"""
        # Convert cluster sizes to integers
        clusters = [int(x) for x in clusters]
        
        # Calculate statistics
        final_image_size = countvalidpixels(cleaned_image)
        density = final_image_size / no_bg_size if no_bg_size > 0 else 1
        cluster_sum = sum(clusters)
        avg_cluster_size = sum(clusters) / len(clusters) if clusters else 0
        cluster_amount = len(clusters)
        
        stats = {
            'normal_image_size': normal_image_size,
            'no_bg_size': no_bg_size,
            'final_image_size': final_image_size,
            'cluster_amount': cluster_amount,
            'clusters': clusters,
            'cluster_sum': cluster_sum,
            'avg_cluster_size': avg_cluster_size,
            'density': density
        }
        
        return stats
    
    def generate_report(self, report_path, stats):
        """Generate analysis report with statistics."""
        with open(report_path, 'w') as f:
            f.write("Metal Porosity Analysis Report\n")
            f.write("=======================\n\n")
            
            f.write("All numbers here are expressed in terms of pixel count. If provided with an image scale and image size,\n")
            f.write("one can easily convert these values to meaningful units.\n")
            f.write("Clusters are the holes within the object itself.\n\n")
            
            f.write(f"Normal Image Size: {stats['normal_image_size']}\n")
            f.write(f"Object Size (after bg removal): {stats['no_bg_size']}\n")
            f.write(f"Final Object Size (after hole removal): {stats['final_image_size']}\n")
            f.write(f"Cluster Amount: {stats['cluster_amount']}\n")
            f.write(f"Cluster Sizes: {stats['clusters']}\n")
            f.write(f"Cluster Sum: {stats['cluster_sum']}\n")
            f.write(f"Average Cluster Size: {stats['avg_cluster_size']:.2f}\n")
            f.write(f"Density: {stats['density']:.2%}\n")

def main():
    root = tk.Tk()
    app = PorosityAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()