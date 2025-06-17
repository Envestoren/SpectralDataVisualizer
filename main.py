import os
from src import SpectralDataProcessor, SpectralDataAnalyzer, SpectralDataVisualizer


def get_all_file_paths(folder_paths):
    """
    Retrieve all file paths from the given list of folder paths.

    Parameters:
    folder_paths (list): A list of folder paths to scan for files.

    Returns:
    list: A list of full file paths.
    """
    all_file_paths = []
    for folder_path in folder_paths:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                all_file_paths.append(file_path)
    return all_file_paths


def plot():
    # Define the base path and the path to the specific data folder
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_folder = os.path.join(base_path, 'test_data', '[1] testday_1', '[4] cooling', 'upper')

    # Retrieve all file paths from the specified data folder
    list_of_paths = get_all_file_paths([data_folder])

    # Check if the data folder exists
    if not os.path.exists(data_folder):
        raise FileNotFoundError(f"Data folder not found: {data_folder}")
    
    # Define the folder where plots will be saved and create it if it doesn't exist
    save_folder = "my_first_plot"
    save_folder_path = os.path.join('plots', save_folder)
    os.makedirs(save_folder_path, exist_ok=True)

    # Load and preprocess the spectral data
    processor = SpectralDataProcessor(
        list_of_paths,
        wavelength_range=(200, 1050),        # Set the range of wavelengths to analyze
        interpolation_points=3648,           # Define number of points for interpolation
        shift_300nm=3                        # Apply a shift for spectrometer calibration at 300 nm
    )

    # Initialize analyzer and smooth the data to reduce noise
    analyzer = SpectralDataAnalyzer(processor.df)
    analyzer.smooth_spectral_data(window_length=301, polyorder=1)

    # Prepare the visualizer with the smoothed data
    visualizer = SpectralDataVisualizer(processor.df)

    # Generate a single spectral plot using the selected options
    visualizer.plot_spectra(
        plot_average=False,                  # Choose to show all spectra instead of the average
        use_standardized=False,              # Use raw data without standardization
        use_normalized=False,                # Use raw intensity values without normalization
        plot_gradient=True,                 # Choose to display raw spectra without their gradients
        group_by_spectrometer_id=False,      # Treat all spectra as a single group regardless of spectrometer ID
        show_color_background=True,          # Add background color bands to indicate wavelength ranges
        title='Ammonia flow stopped',        # Set the plot title
        save_path=os.path.join(save_folder_path, 'spectral_data.png')  # Define path to save the plot
    )


def subplot():
    # Define the base path and two subfolders for comparison
    base_path = os.path.dirname(os.path.abspath(__file__))
    data_folder_1 = os.path.join(base_path, 'test_data', '[4] testday_4', '[6] all')
    data_folder_2 = os.path.join(base_path, 'test_data', '[4] testday_4', '[6] all')

    # Retrieve all file paths from both data folders
    list_of_paths_1 = get_all_file_paths([data_folder_1])
    list_of_paths_2 = get_all_file_paths([data_folder_2])

    # Validate that both folders exist
    if not os.path.exists(data_folder_1):
        raise FileNotFoundError(f"Data folder not found: {data_folder_1}")
    if not os.path.exists(data_folder_2):
        raise FileNotFoundError(f"Data folder not found: {data_folder_2}")

    # Create directory for saving the subplot figure
    save_folder = "my_first_subplot"
    save_folder_path = os.path.join('plots', save_folder)
    os.makedirs(save_folder_path, exist_ok=True)

    # Process spectral data from both sources
    processor_1 = SpectralDataProcessor(
        list_of_paths_1,
        wavelength_range=(300, 1050),
        interpolation_points=3648,
        shift_300nm=3
    )
    processor_2 = SpectralDataProcessor(
        list_of_paths_2,
        wavelength_range=(300, 1050),
        interpolation_points=3648,
        shift_300nm=3
    )

    # Smooth both datasets to reduce noise and highlight trends
    analyzer_1 = SpectralDataAnalyzer(processor_1.df)
    analyzer_1.smooth_spectral_data(window_length=51, polyorder=2)

    analyzer_2 = SpectralDataAnalyzer(processor_2.df)
    analyzer_2.smooth_spectral_data(window_length=51, polyorder=2)

    
    # Slice the first 20 rows from the smoothed data for both datasets
    #analyzer_2.smooth_data = analyzer_2.smooth_data.groupby('name').head(20)
    #analyzer_1.smooth_data = analyzer_1.smooth_data.groupby('name').head(20)


    # Create subplot comparing the two datasets
    visualizer = SpectralDataVisualizer(analyzer_1.smooth_data)
    visualizer.plot_subplots(
        processor1_df=analyzer_1.smooth_data,        # First subplot data (e.g. upper sensor)
        processor2_df=analyzer_2.smooth_data,        # Second subplot data (e.g. lower sensor)
        title='All spectra from 4th test day',                          # Title for the figure
        processor1_label="All spectra",       # Label for the first subplot
        processor2_label="Average spectra",       # Label for the second subplot
        use_standardized=False,                      # Use raw data for plotting
        use_normalized=False,                        # Avoid normalization to keep original intensity
        show_color_background=True,                  # Include wavelength-based color shading
        group_by_spectrometer_id=True,              # Combine data across spectrometers if needed
        save_path=os.path.join(save_folder_path, 'spectral_subplot.png'),  # Output path
        gradient=False                               # Choose to show original spectra without derivative
    )


if __name__ == "__main__":
    #plot()
    subplot()
    print("Plotting complete.")
