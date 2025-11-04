import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from PIL import Image
import numpy as np
from scipy.ndimage import binary_dilation
import os

class BackgroundRemoverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Microscopy Background Remover")
        self.root.geometry("700x400")
        self.root.resizable(False, False)
        
        # Configure style
        style = ttk.Style()
        style.configure('TLabel', font=('Arial', 10))
        style.configure('TButton', font=('Arial', 10))
        
        # Main frame
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Input Path
        ttk.Label(main_frame, text="Input Path:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.input_path = tk.StringVar(value="dataset/Bilder zum Freistellen_13_05_25/179 1 a.tif")
        self.input_entry = ttk.Entry(main_frame, textvariable=self.input_path, width=60)
        self.input_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_input).grid(row=0, column=2, padx=5, pady=5)
        
        # Output Path
        ttk.Label(main_frame, text="Output Path:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.output_path = tk.StringVar(value="output/freigestellt/179 1 a.tif")
        self.output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=60)
        self.output_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output).grid(row=1, column=2, padx=5, pady=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Aggressiveness Slider
        ttk.Label(main_frame, text="Aggressiveness:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.aggressiveness = tk.IntVar(value=35)
        slider_frame = ttk.Frame(main_frame)
        slider_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.slider = ttk.Scale(slider_frame, from_=10, to=100, variable=self.aggressiveness, 
                                orient=tk.HORIZONTAL, length=400, command=self.update_slider_label)
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.slider_label = ttk.Label(slider_frame, text="35")
        self.slider_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(main_frame, text="(Higher = more background removed)", 
                 font=('Arial', 8, 'italic')).grid(row=4, column=1, sticky=tk.W, padx=5)
        
        # Pure Black Tolerance Slider
        ttk.Label(main_frame, text="Black Tolerance:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.black_tolerance = tk.IntVar(value=10)
        tolerance_frame = ttk.Frame(main_frame)
        tolerance_frame.grid(row=5, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.tolerance_slider = ttk.Scale(tolerance_frame, from_=0, to=50, variable=self.black_tolerance,
                                          orient=tk.HORIZONTAL, length=400, command=self.update_tolerance_label)
        self.tolerance_slider.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        self.tolerance_label = ttk.Label(tolerance_frame, text="10")
        self.tolerance_label.pack(side=tk.LEFT, padx=10)
        
        ttk.Label(main_frame, text="(Removes pure black + this tolerance)", 
                 font=('Arial', 8, 'italic')).grid(row=6, column=1, sticky=tk.W, padx=5)
        
        # Separator
        ttk.Separator(main_frame, orient='horizontal').grid(row=7, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=20)
        
        # Start Button
        self.start_button = ttk.Button(main_frame, text="Start", command=self.process_image)
        self.start_button.grid(row=8, column=1, pady=10)
        
        # Status Label
        self.status_label = ttk.Label(main_frame, text="Ready", foreground="blue")
        self.status_label.grid(row=9, column=0, columnspan=3, pady=5)
        
    def update_slider_label(self, value):
        self.slider_label.config(text=str(int(float(value))))
    
    def update_tolerance_label(self, value):
        self.tolerance_label.config(text=str(int(float(value))))
    
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Input Image",
            filetypes=[("Image files", "*.png *.jpg *.jpeg *.tif *.tiff"), ("All files", "*.*")]
        )
        if filename:
            self.input_path.set(filename)
    
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Output As",
            defaultextension=".png",
            filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
    
    def process_image(self):
        input_file = self.input_path.get()
        output_file = self.output_path.get()
        aggressiveness = self.aggressiveness.get()
        black_tol = self.black_tolerance.get()
        
        # Validation
        if not input_file or not os.path.exists(input_file):
            messagebox.showerror("Error", "Input file does not exist!")
            return
        
        if not output_file:
            messagebox.showerror("Error", "Please specify an output path!")
            return
        
        # Update status
        self.status_label.config(text="Processing...", foreground="orange")
        self.start_button.config(state='disabled')
        self.root.update()
        
        try:
            # Load the image
            img = Image.open(input_file)
            
            # Convert to RGBA if not already
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Convert to numpy array
            img_array = np.array(img)
            height, width = img_array.shape[:2]
            
            # Step 1: Sample 4x4 pixels in top-left corner for base black value
            top_left_sample = img_array[0:4, 0:4, :3]
            base_black = np.mean(top_left_sample, axis=(0, 1))
            
            # Step 2: Define black spectrum with aggressiveness threshold
            max_background = base_black + aggressiveness
            
            # Step 3: Additional check for pure black pixels with tolerance
            # Pure black = RGB values all close to 0
            pure_black_mask = np.all(img_array[:, :, :3] <= black_tol, axis=2)
            
            # Step 4: Find the white overlay box (bottom-right area)
            brightness = np.sum(img_array[:, :, :3], axis=2)
            brightness_threshold = np.percentile(brightness, 95)
            bright_mask = brightness >= brightness_threshold
            
            # Expand the mask to ensure we capture the entire box including text
            bright_mask_expanded = binary_dilation(bright_mask, iterations=5)
            
            # Step 5: Create mask for black spectrum
            black_spectrum_mask = np.all(img_array[:, :, :3] <= max_background, axis=2)
            
            # Combine both masks: regular black spectrum OR pure black
            combined_black_mask = black_spectrum_mask | pure_black_mask
            
            # Step 6: Remove black pixels EXCEPT those in overlay
            pixels_to_remove = combined_black_mask & ~bright_mask_expanded
            
            # Set alpha to 0 for these pixels
            img_array[pixels_to_remove, 3] = 0
            
            # Convert back to PIL Image
            result_img = Image.fromarray(img_array)
            
            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(output_file)
            if output_dir and not os.path.exists(output_dir):
                os.makedirs(output_dir, exist_ok=True)
            
            # Save the result
            result_img.save(output_file)
            
            # Statistics
            total_pixels = height * width
            removed_pixels = np.sum(pixels_to_remove)
            percentage = (removed_pixels / total_pixels) * 100
            
            self.status_label.config(
                text=f"Success! Removed {removed_pixels:,} pixels ({percentage:.1f}%)",
                foreground="green"
            )
            messagebox.showinfo("Success", f"Image saved to:\n{output_file}\n\n"
                                          f"Removed {removed_pixels:,} background pixels ({percentage:.1f}%)")
            
        except Exception as e:
            self.status_label.config(text=f"Error: {str(e)}", foreground="red")
            messagebox.showerror("Error", f"An error occurred:\n{str(e)}")
        
        finally:
            self.start_button.config(state='normal')

if __name__ == "__main__":
    root = tk.Tk()
    app = BackgroundRemoverGUI(root)
    root.mainloop()