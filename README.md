# Metal Sample Analysis Tools

Welcome! This folder contains two different programs designed to help you clean up images of metal samples and analyze them. 

Since metal samples can look very different (some are solid blocks, others are scattered powder), we have two separate tools. Read **Section 1** below to decide which one you need.

---

## 1. Which Tool Should I Use?

Look at your image and ask yourself: **"Is this one solid object with holes in it, or many scattered little pieces?"**

### Option A: The "Swiss Cheese" Case
**Use: `metal_porosity_analyzer.py`**

* **Best for:** A single, solid piece of metal that has "pores" (holes) inside it.
* **What it does:** It finds the border of your metal object, cuts away the background, and then counts/measures the black holes inside the metal. It gives you a density report at the end.

### Option B: The "Salt on a Table" Case
**Use: `sparse_drops.py`**

* **Best for:** Disjoint, scattered drops, powder, or particles that are not touching each other.
* **What it does:** It aggressively removes the background between all the little scattered pieces. It does **not** give a density report because there is no single "object" to measure against.

---

## 2. Guide: Metal Porosity Analyzer (Option A)
**File:** `metal_porosity_analyzer.py`

Use this for solid shapes. When you open the window, you will see several sliders. Here is what they do:

* **Black Tolerance (0.1 - 1.0)**
    * *What it does:* Decides what counts as a "hole."
    * *Intuition:* Think of this as a strictness filter.
    * *Example:* If set **High (0.9)**, dark grey spots are counted as holes. If set **Low (0.2)**, only pitch-black spots are counted. If your image is failing to pick up holes, turn this UP.
* **Minimum Cluster Size**
    * *What it does:* Decides how big a spot needs to be to matter.
    * *Intuition:* A "Dust Filter."
    * *Example:* If set to **25**, the program ignores tiny pixel specks (dust/noise) and only counts actual holes larger than 25 pixels.
* **Edge Width**
    * *What it does:* Creates a "Safety Zone" around the outer border of your metal object.
    * *Intuition:* This stops the program from accidentally thinking the edge of your sample is a hole.
    * *Example:* If your sample has a rough, dark edge and the program keeps trying to delete it, **increase** this number to tell the program: "Don't touch the outer 40 pixels."
* **Show Hole Detection Overlay**
    * *Check this box:* It paints the detected holes **green** on the screen so you can visually check if the settings are correct before saving.

---

## 3. Guide: Sparse Drops / Background Remover (Option B)
**File:** `sparse_drops.py`

Use this for scattered particles.

* **Aggressiveness (10 - 100)**
    * *What it does:* How hard the program tries to scrub away the background color.
    * *Intuition:* Like the strength of an eraser.
    * *Example:* If you still see faint shadows or "haze" around your particles, **increase** this number. If the particles themselves are disappearing, **decrease** it.
* **Black Tolerance**
    * *What it does:* Specifically targets pure black artifacts or dust.
    * *Intuition:* A "Spot Cleaner" for dark specks.
    * *Example:* Usually, you can leave this low (around 10). Increase it only if you have distinct black specks on the background that aren't part of the metal.

---

## 4. How to Install and Run (Step-by-Step)

If you have never run a Python script before, follow these exact steps.

### Step 1: Install Python
1.  Go to [python.org/downloads](https://www.python.org/downloads/).
2.  Download the latest version for Windows.
3.  **CRITICAL:** When the installer opens, check the box at the bottom that says **"Add Python to PATH"**. (If you miss this, the commands below won't work).
4.  Click "Install Now".

### Step 2: Install the "Helper" Libraries
These scripts need specific math and image tools to work. You need to install them once.

1.  Open the terminal, either by searching for "cmd" on windows or by pressing on "Terminal" within VSCode
2.  Copy and paste the following line into that black window and press **Enter**:

    ```text
    pip install numpy scipy Pillow rembg
    ```

  
### Step 3: Run the Program
1.  Make sure all your files (`sparse_drops.py`, `metal_porosity_analyzer.py`, and the helper files `naive.py` and `removebg.py`) are in the **same folder**.
2.  Open that folder.
3.  Either open the files via the terminal by running `python sparse_drops.py` or run them within VSCode directly
