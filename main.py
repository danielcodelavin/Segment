import tkinter as tk
from tkinter import filedialog, messagebox

def browse_input():
    input_path.set(filedialog.askopenfilename())

def browse_output():
    output_path.set(filedialog.askdirectory())

def run_function():
    try:
        input_file = input_path.get()
        output_dir = output_path.get()
        black_tol = float(black_tolerance.get())
        min_cluster = int(min_cluster_size.get())
        max_debris = int(max_debris_size.get())
        
        if not input_file or not output_dir:
            raise ValueError("Input and output paths are required.")
        
        # Call the naivemain function with the parameters
        naivemain(input_file, output_dir, black_tol, min_cluster, max_debris)
        messagebox.showinfo("Success", "Function executed successfully!")
    except ValueError as e:
        messagebox.showerror("Error", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")



# Create the main window
root = tk.Tk()
root.title("Naive Main GUI")
root.geometry("500x400")

# Create and set up variables
input_path = tk.StringVar()
output_path = tk.StringVar()
black_tolerance = tk.StringVar()
min_cluster_size = tk.StringVar()
max_debris_size = tk.StringVar()

# Create and place widgets
tk.Label(root, text="Input Path:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=input_path, width=50).grid(row=0, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_input).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Output Path:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=output_path, width=50).grid(row=1, column=1, padx=5, pady=5)
tk.Button(root, text="Browse", command=browse_output).grid(row=1, column=2, padx=5, pady=5)

tk.Label(root, text="Black Tolerance:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=black_tolerance, width=10).grid(row=2, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Minimum Cluster Size:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=min_cluster_size, width=10).grid(row=3, column=1, sticky="w", padx=5, pady=5)

tk.Label(root, text="Max Debris Size:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
tk.Entry(root, textvariable=max_debris_size, width=10).grid(row=4, column=1, sticky="w", padx=5, pady=5)

tk.Button(root, text="Run Function", command=run_function).grid(row=5, column=1, pady=10)

# Create a Text widget for static text
static_text = tk.Text(root, height=10, width=60)
static_text.grid(row=6, column=0, columnspan=3, padx=5, pady=5)
static_text.insert(tk.END, "Your static text goes here.")
static_text.config(state=tk.DISABLED)  # Make it read-only

root.mainloop()