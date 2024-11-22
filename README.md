# MRI Data Visualizer

A Python-based application for visualizing and analyzing MRI data.

## UI Demo

### Landing Page
![Landing Page](https://raw.githubusercontent.com/Elliot0122/Data-Visualization-for-MRI-Data/main/public/landing%20page.png)
*File selection interface for data upload*

### Main Visualization
![Main Page](https://raw.githubusercontent.com/Elliot0122/Data-Visualization-for-MRI-Data/main/public/main%20page.png)
*Interactive visualization interface featuring:*
- Maximum Strength detection (red point)
- Stiffness calculation (purple line)
- Interactive slope measurement (blue points)
- Yield Point tracking (green point)

## Installation Guide

### Prerequisites

1. Install Anaconda or Miniconda:
   - [Download Miniconda](https://docs.conda.io/en/latest/miniconda.html) (Recommended - lighter weight)

### Installation Steps

1. **Clone or Download the Repository**
   ```bash
   git clone git@github.com:Elliot0122/Data-Visualization-for-MRI-Data.git
   cd Data-Visualization-for-MRI-Data
   ```

2. **Create and Activate Conda Environment**
   ```bash
   #for Windows users
   conda create --name mriviz python=3.9
   #for MacOS users
   conda create --name mriviz python=3.13

   conda activate mriviz
   ```

3. **Install Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python main.py
   ```

