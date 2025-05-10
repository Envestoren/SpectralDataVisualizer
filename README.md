# Spectral Data Analysis and Visualization

This project is a tool for processing, analyzing, and visualizing spectral data from optical spectrometers. It provides scripts to generate individual plots and comparison subplots from spectral measurements, with options for smoothing, interpolation, and custom visualization.

## Features

- Read and process spectral data files
- Interpolate and smooth spectral curves
- Visualize individual or grouped spectra
- Create subplots comparing different sensors or setups
- Save figures to organized folders

## Folder Structure

```
project_root/
│
├── test_data/
│   └── [4] testday_4/
│       └── [2] eq/
│           ├── lower/
│           └── upper/
├── plots/
│   ├── my_first_plot/
│   └── my_first_subplot/
├── src/
│   ├── data_processor.py
│   ├── data_analyzer.py
│   ├── visualizer.py
│   └── ...
├── main.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone this repository:

```bash
git clone <your-repo-url>
cd <your-project-folder>
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Use

Run the `main.py` script to generate plots.

```bash
python main.py
```

This will:

- Generate and save a single spectral plot from `[2] eq/`
- Generate and save a subplot comparing `lower/` and `upper/` spectrometer data

## Example Output

The plots will be saved under:

- `plots/my_first_plot/spectral_data.png`
- `plots/my_first_subplot/spectral_subplot.png`

## Requirements

See `requirements.txt`:

```
pandas
numpy
matplotlib
scipy
scikit-learn
```

## Customization

You can modify the following:

- **Data folder paths** in `main.py`
- **Smoothing settings**: window size, polynomial order
- **Plot options**: color backgrounds, labels, normalization, etc.

## License

MIT License – free to use, modify, and share.

---

Created by Even Storeheier
