import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk, ImageOps
import numpy as np
import cv2
from rembg import remove
import io
import os

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
        self.min_hole_size = tk.IntVar(value=30)
        self.max_hole_size = tk.IntVar(value=5000)
        self.color_tolerance = tk.IntVar(value=50)
        self.show_overlay = tk.BooleanVar(value=True)
        
        # State variables
        self.current_image = None
        self.current_holes = None
        self.processed_image = None
        
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
        
    def create_input_section(self):
        input_frame = ttk.LabelFrame(self.control_panel, text="File Selection", padding="10")
        input_frame.grid(row=0, column=0, sticky="ew", pady=5)
        
        ttk.Label(input_frame, text="Input Image:").grid(row=0, column=0, sticky="w")
        ttk.Entry(input_frame, textvariable=self.input_path).grid(row=1, column=0, sticky="ew")
        ttk.Button(input_frame, text="Browse", command=self.browse_input).grid(row=1, column=1, padx=5)
        
        ttk.Label(input_frame, text="Output Directory:").grid(row=2, column=0, sticky="w", pady=(10,0))
        ttk.Entry(input_frame, textvariable=self.output_dir).grid(row=3, column=0, sticky="ew")
        ttk.Button(input_frame, text="Browse", command=self.browse_output).grid(row=3, column=1, padx=5)
        
    def create_parameter_section(self):
        param_frame = ttk.LabelFrame(self.control_panel, text="Processing Parameters", padding="10")
        param_frame.grid(row=1, column=0, sticky="ew", pady=5)
        
        # Min hole size
        ttk.Label(param_frame, text="Minimum Hole Size:").grid(row=0, column=0, sticky="w")
        min_frame = ttk.Frame(param_frame)
        min_frame.grid(row=1, column=0, sticky="ew")
        
        self.min_size_label = tk.Label(min_frame, text=self.min_hole_size.get())
        self.min_size_label.grid(row=0, column=1, padx=5)
        
        min_scale = ttk.Scale(min_frame, from_=10, to=100, variable=self.min_hole_size,
                            orient="horizontal", command=lambda v: self.min_size_label.config(text=f"{int(float(v))}"))
        min_scale.grid(row=0, column=0, sticky="ew")
        
        # Max hole size
        ttk.Label(param_frame, text="Maximum Hole Size:").grid(row=2, column=0, sticky="w", pady=(10,0))
        max_frame = ttk.Frame(param_frame)
        max_frame.grid(row=3, column=0, sticky="ew")
        
        self.max_size_label = tk.Label(max_frame, text=self.max_hole_size.get())
        self.max_size_label.grid(row=0, column=1, padx=5)
        
        max_scale = ttk.Scale(max_frame, from_=100, to=5000, variable=self.max_hole_size,
                            orient="horizontal", command=lambda v: self.max_size_label.config(text=f"{int(float(v))}"))
        max_scale.grid(row=0, column=0, sticky="ew")
        
        # Color tolerance
        ttk.Label(param_frame, text="Color Tolerance (%):").grid(row=4, column=0, sticky="w", pady=(10,0))
        tolerance_frame = ttk.Frame(param_frame)
        tolerance_frame.grid(row=5, column=0, sticky="ew")
        
        self.tolerance_label = tk.Label(tolerance_frame, text=self.color_tolerance.get())
        self.tolerance_label.grid(row=0, column=1, padx=5)
        
        tolerance_scale = ttk.Scale(tolerance_frame, from_=0, to=100, variable=self.color_tolerance,
                                  orient="horizontal", command=lambda v: self.tolerance_label.config(text=f"{int(float(v))}"))
        tolerance_scale.grid(row=0, column=0, sticky="ew")
        
        # Show overlay checkbox
        ttk.Checkbutton(param_frame, text="Show Hole Detection Overlay", 
                       variable=self.show_overlay,
                       command=self.toggle_overlay).grid(row=6, column=0, sticky="w", pady=5)
        
        # Process button
        ttk.Button(param_frame, text="Process Image", 
                  command=self.process_image).grid(row=7, column=0, sticky="ew", pady=20)
        
    def create_preview_section(self):
        preview_frame = ttk.LabelFrame(self.preview_panel, text="Preview", padding="10")
        preview_frame.grid(row=0, column=0, sticky="nsew")
        
        self.preview_canvas = tk.Canvas(preview_frame, bg='white')
        self.preview_canvas.grid(row=0, column=0, sticky="nsew")
        
        self.preview_panel.grid_rowconfigure(0, weight=1)
        self.preview_panel.grid_columnconfigure(0, weight=1)
        preview_frame.grid_rowconfigure(0, weight=1)
        preview_frame.grid_columnconfigure(0, weight=1)
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.tif *.tiff *.bmp")])
        if filename:
            self.input_path.set(filename)
            self.load_and_preview(filename)
            
    def browse_output(self):
        dirname = filedialog.askdirectory()
        if dirname:
            self.output_dir.set(dirname)
            
    def load_and_preview(self, image_path):
        try:
            image = Image.open(image_path)
            self.current_image = image
            self.update_preview(image)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {str(e)}")
            
    def update_preview(self, image, holes=None):
        if self.processed_image and not holes:
            display_image = self.processed_image
        else:
            display_image = image
            
        # Calculate aspect ratio and resize maintaining ratio
        aspect_ratio = display_image.width / display_image.height
        max_size = 600
        
        if aspect_ratio > 1:
            new_width = max_size
            new_height = int(max_size / aspect_ratio)
        else:
            new_height = max_size
            new_width = int(max_size * aspect_ratio)
            
        display_image = display_image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # If holes provided and overlay enabled, draw them
        if holes and self.show_overlay.get():
            display_array = np.array(display_image)
            scale_factor = new_width / image.width
            
            # Draw semi-transparent green overlay
            overlay = np.zeros_like(display_array)
            for hole in holes:
                for y, x in hole:
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
        self.preview_canvas.delete("all")
        self.preview_canvas.create_image(
            self.preview_canvas.winfo_width()/2,
            self.preview_canvas.winfo_height()/2,
            image=photo, anchor="center")
        self.preview_canvas.image = photo
        
    def toggle_overlay(self):
        if self.current_image and self.current_holes:
            self.update_preview(self.current_image, self.current_holes)
            
    def process_image(self):
        if not self.input_path.get():
            messagebox.showerror("Error", "Please select an input image.")
            return
            
        try:
            # Create output directory
            os.makedirs(self.output_dir.get(), exist_ok=True)
            
            # Get paths
            base_name = os.path.splitext(os.path.basename(self.input_path.get()))[0]
            output_image_path = os.path.join(self.output_dir.get(), f"{base_name}_processed.png")
            output_report_path = os.path.join(self.output_dir.get(), f"{base_name}_report.txt")
            
            # Process image
            cleaned_image, stats = self.analyze_porosity(
                self.input_path.get(),
                self.min_hole_size.get(),
                self.max_hole_size.get(),
                self.color_tolerance.get() / 100.0
            )
            
            # Save results
            cleaned_image.save(output_image_path)
            self.generate_report(output_report_path, stats)
            
            # Update preview with processed image
            self.processed_image = cleaned_image
            self.update_preview(cleaned_image)
            
            messagebox.showinfo("Success", "Image processed successfully!")
            
        except Exception as e:
            messagebox.showerror("Error", f"Processing failed: {str(e)}")
            
    def analyze_porosity(self, input_path, min_size, max_size, tolerance):
        # Load and remove background
        with open(input_path, 'rb') as f:
            input_data = f.read()
            
        # Get both original and background-removed images
        orig_image = Image.open(io.BytesIO(input_data))
        output_data = remove(input_data)
        no_bg_image = Image.open(io.BytesIO(output_data))
        
        # Convert to numpy arrays
        orig_array = np.array(orig_image)
        no_bg_array = np.array(no_bg_image)
        
        # Get mask from alpha channel
        mask = no_bg_array[:,:,3] > 0
        
        # Convert to grayscale
        gray = cv2.cvtColor(orig_array, cv2.COLOR_RGB2GRAY)
        
        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        # Use adaptive thresholding to detect holes
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                     cv2.THRESH_BINARY_INV, 11, 2)
        
        # Apply morphological operations to clean up the thresholded image
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5,5))
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        
        # Find contours
        contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        holes = []
        for contour in contours:
            area = cv2.contourArea(contour)
            if min_size <= area <= max_size:
                # Get coordinates of the contour
                coords = np.argwhere(cv2.drawContours(np.zeros_like(closed), [contour], -1, 255, -1))
                holes.append([tuple(coord) for coord in coords])
        
        self.current_holes = holes
        
        # Calculate statistics
        total_pixels = np.sum(mask)
        hole_pixels = sum(len(hole) for hole in holes)
        density = 1 - (hole_pixels / total_pixels) if total_pixels > 0 else 1
        
        # Remove holes using inpainting
        cleaned_image = self.remove_holes(no_bg_image.copy(), holes)
        
        stats = {
            'total_pixels': total_pixels,
            'hole_pixels': hole_pixels,
            'hole_count': len(holes),
            'density': density,
            'hole_sizes': [len(hole) for hole in holes]
        }
        
        return cleaned_image, stats
        
    def remove_holes(self, image, holes):
        """Remove holes using inpainting"""
        if not holes:
            return image
        
        # Convert to OpenCV format
        img = cv2.cvtColor(np.array(image), cv2.COLOR_RGBA2BGRA)
        height, width = img.shape[:2]
        
        # Create inpaint mask
        mask = np.zeros((height, width), dtype=np.uint8)
        for hole in holes:
            for y, x in hole:
                mask[y, x] = 255
                
        # Inpaint using Navier-Stokes method
        inpainted = cv2.inpaint(img[:, :, :3], mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
        
        # Merge with original alpha channel
        result = cv2.merge((inpainted, img[:, :, 3]))
        
        # Convert back to PIL Image
        return Image.fromarray(cv2.cvtColor(result, cv2.COLOR_BGRA2RGBA))
    
    def generate_report(self, report_path, stats):
        """Generate analysis report with statistics."""
        with open(report_path, 'w') as f:
            f.write("Porosity Analysis Report\n")
            f.write("=======================\n\n")
            
            f.write("Analysis Results:\n")
            f.write(f"- Total Object Pixels: {stats['total_pixels']}\n")
            f.write(f"- Total Hole Pixels: {stats['hole_pixels']}\n")
            f.write(f"- Number of Holes: {stats['hole_count']}\n")
            f.write(f"- Material Density: {stats['density']:.2%}\n\n")
            
            if stats['hole_sizes']:
                f.write("Hole Size Distribution:\n")
                f.write(f"- Minimum: {min(stats['hole_sizes'])} pixels\n")
                f.write(f"- Maximum: {max(stats['hole_sizes'])} pixels\n")
                f.write(f"- Average: {sum(stats['hole_sizes']) / len(stats['hole_sizes']):.1f} pixels\n")
                f.write("\nDetailed Hole Sizes:\n")
                f.write(str(sorted(stats['hole_sizes'], reverse=True)))

def main():
    root = tk.Tk()
    app = PorosityAnalyzer(root)
    root.mainloop()

if __name__ == "__main__":
    main()