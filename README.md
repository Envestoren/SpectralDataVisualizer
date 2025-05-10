# Spectral Data Analysis and Visualization

This project is a tool for processing, analyzing, and visualizing spectral data from optical spectrometers. It provides scripts to generate individual plots and comparison subplots from spectral measurements, with options for smoothing, interpolation, and custom visualization.

## Features

* **Data Processing:** Reads and processes spectral data files.
* **Data Analysis:** Interpolates and smooths spectral curves using techniques from libraries like SciPy.
* **Visualization:**
    * Visualizes individual spectra.
    * Creates subplots comparing different sensors or setups.
    * Saves figures to organized folders.
* **Customization:** Offers options for customizing plots, including color backgrounds, labels, and normalization.

## Table of Contents

* [Features](#features)
* [Folder Structure](#folder-structure)
* [Installation](#installation)
* [How to Use](#how-to-use)
* [Example Output](#example-output)
* [Requirements](#requirements)
* [Customization](#customization)
* [License](#license)
* [Contact](#contact)

## Folder Structure

    project_root/
    │
    ├── test_data/
    │   └── \[4\] testday_4/
    │       └── \[2\] eq/
    │           ├── lower/
    │           └── upper/
    ├── plots/
    │   ├── my_first_plot/
    │   └── my_first_subplot/
    ├── src/
    │   ├── data_processor.py  # Handles data loading and processing
    │   ├── data_analyzer.py   # Contains functions for interpolation, smoothing, and analysis
    │   ├── visualizer.py      #  Handles plot generation and saving
    │   └── ...
    ├── main.py          # Main script to run the analysis and generate plots
    ├── requirements.txt # List of Python dependencies
    └── README.md        # Project documentation (this file)

## Installation

1.  **Clone the repository:**

    ```
    git clone <your-repo-url>
    cd <your-project-folder>
    ```

    * Replace `<your-repo-url>` with the actual URL of your Git repository.
    * Replace `<your-project-folder>` with the name of the directory where the repository is cloned.

2.  **Install the dependencies:**

    ```
    pip install -r requirements.txt
    ```

    This command uses `pip`, the Python package installer, to install all the libraries listed in the `requirements.txt` file.  This ensures you have all the necessary software to run the project.

## How to Use

1.  **Run the `main.py` script:**

    ```
    python main.py
    ```

    This script executes the core logic of the project, processing the spectral data and generating the plots.

2.  **View the output:** The generated plots are saved in the `plots/` directory.

    * `plots/my_first_plot/spectral_data.png`: Contains a single spectral plot.
    * `plots/my_first_subplot/spectral_subplot.png`: Contains a subplot comparing different spectral data.

## Example Output

The script generates the following plots, saved under the `plots/` directory:

* `spectral_data.png`: A plot of the spectral data from the `[2] eq/` directory.
* `spectral_subplot.png`: A subplot comparing the spectral data from the `lower/` and `upper/` directories within `[2] eq/`.

## Requirements

The project uses the following Python libraries, which are listed in `requirements.txt`:

    pandas       # For data manipulation and analysis
    numpy        # For numerical computations
    matplotlib   # For creating plots and visualizations
    scipy        # For scientific computing, including interpolation and signal processing
    scikit-learn # For machine learning (if used for any analysis)

To install these, use the command: `pip install -r requirements.txt`

## Customization

The project offers several ways to customize the analysis and visualization:

* **Data Paths:** Modify the data folder paths in `main.py` to point to your specific spectral data files.
* **Smoothing Settings:** Adjust the smoothing parameters (e.g., window size, polynomial order) in `data_analyzer.py` to control how the spectral curves are smoothed.
* **Plot Options:** Customize the appearance of the plots by modifying the options in `visualizer.py`. This includes:
    * Changing color backgrounds.
    * Adding or modifying labels and titles.
    * Normalizing the data.
    * Adjusting other plot aesthetics.

## License

This project is licensed under the MIT License. This means you are free to use, modify, and share the code, even for commercial purposes. See the full `LICENSE` file for details.

## Contact

Created by Even Storeheier. Feel free to reach out with any questions, suggestions, or contributions. (Add contact info here, like email or a link to your website/profile).
