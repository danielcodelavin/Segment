# Metal Porosity Analyzer

A Tkinter application for analyzing porosity in metal samples using image processing techniques.

## Description

This application provides a user interface for detecting and analyzing pores (holes) in metal samples from images. It uses background removal and color-based clustering to identify porous regions, calculate porosity statistics, and generate reports.

Key features:
- Background removal to isolate the metal sample
- Edge protection to prevent false detections at boundaries
- Black color detection for hole identification
- Adjustable parameters for processing control
- Visual overlay of detected pores
- Detailed analysis report generation

## Requirements

```
pillow==10.3.0
numpy==1.26.4
scipy==1.14.1
rembg==2.0.59
opencv-python-headless==4.10.0.84
```

Additional dependencies of these packages will be installed automatically.

## Installation

1. It's recommended to create a virtual environment:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```
   pip install pillow==10.3.0 numpy==1.26.4 scipy==1.14.1 rembg==2.0.59 opencv-python-headless==4.10.0.84
   ```

## Usage

1. Run the application:
   ```
   python metal_porosity_analyzer.py
   ```

2. Use the interface to:
   - Load an input image
   - Set the output directory and filenames
   - Adjust processing parameters
   - Process the image
   - View results and save the analysis

## Processing Parameters

- **Black Tolerance**: Determines how close a pixel must be to the detected "black" color to be considered a hole
- **Minimum Cluster Size**: The minimum size a connected group of pixels must be to be counted as a hole
- **Edge Width**: Width of the protected border zone where holes are not detected
- **Edge Samples**: Number of points to sample when determining the reference black color

## Output Files

- Processed image with holes removed
- Debug visualization showing the edge protection zone
- Analysis report with porosity statistics

## Analysis Report

The report includes:
- Original image size (in pixels)
- Object size after background removal
- Final object size after hole removal
- Number of holes detected
- Size of each hole (in pixels)
- Total area of all holes
- Average hole size
- Density (ratio of final to initial object size)