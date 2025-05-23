from re import sub
from turtle import pos
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib import lines as mlines
from .data_analyzer import SpectralDataAnalyzer


class SpectralDataVisualizer:
    """
    A class for visualizing spectral data, with methods for plotting individual spectra,
    average spectra, and enhanced visualizations with wavelength-specific color backgrounds.
    """

    def __init__(self, df):
        """
        Initialize the SpectralDataVisualizer object.

        Parameters:
        df (DataFrame): Input DataFrame containing spectral data and metadata.
        """
        self.df = df
        self.analyzer = SpectralDataAnalyzer(df)

        # Set global font size for better readability
        self._set_plot_defaults()

    def _set_plot_defaults(self):
        """
        Set global matplotlib configurations for consistent and readable plots.
        """
        plt.rcParams.update({
            'font.size': 20,
            'axes.titlesize': 20,
            'axes.labelsize': 20,
            'xtick.labelsize': 20,
            'ytick.labelsize': 20,
            'legend.fontsize': 20,
            'figure.titlesize': 24
        })

    def _get_standardized_data(self):
        """
        Compute and return the standardized DataFrame using SpectralDataAnalyzer.

        Returns:
        DataFrame: Standardized spectral data.
        """
        return self.analyzer.standardize_spectral_data()

    def _get_normalized_data(self):
        """
        Compute and return the normalized DataFrame using SpectralDataAnalyzer.

        Returns:
        DataFrame: Normalized spectral data.
        """
        return self.analyzer.normalize_spectral_data()

    def _add_color_backgrounds(self, ax, min_wavelength, max_wavelength, subplot=False):
        """
        Adds color-coded backgrounds to represent UV, visible, and IR ranges.
        """
        uv_range, visible_range, ir_range = (200, 400), (400, 700), (700, 1050)
        color_ranges = {
            'Violet': (400, 450), 'Blue': (450, 485), 'Cyan': (485, 500),
            'Green': (500, 565), 'Yellow': (565, 590), 'Orange': (590, 625), 'Red': (625, 700),
        }

        # Add UV and IR backgrounds
        self._add_background(ax, uv_range, min_wavelength, max_wavelength, 'purple', alpha=0.2)
        self._add_background(ax, ir_range, min_wavelength, max_wavelength, 'red', alpha=0.2)

        # Add visible spectrum backgrounds
        for color, (start, end) in color_ranges.items():
            self._add_background(ax, (start, end), min_wavelength, max_wavelength, color.lower(), alpha=0.4)

        # Add labels for color ranges
        self._add_color_labels(ax, min_wavelength, max_wavelength, uv_range, ir_range, color_ranges, subplot)

    def _add_background(self, ax, range_, min_wavelength, max_wavelength, color, alpha):
        """
        Adds a background color for a specific wavelength range.
        """
        start, end = range_
        if min_wavelength <= end and max_wavelength >= start:
            ax.axvspan(max(min_wavelength, start), min(max_wavelength, end), facecolor=color, alpha=alpha)

    def _add_color_labels(self, ax, min_wavelength, max_wavelength, uv_range, ir_range, color_ranges, subplot):
        """
        Adds top x-ticks with color labels for UV, visible, and IR ranges.
        """
        if subplot is False:
            ax2 = ax.twiny()
            ax2.set_xlim(ax.get_xlim())
            xticks, xticklabels = [], []

            # Add visible spectrum labels
            for color, (start, end) in color_ranges.items():
                if min_wavelength <= end and max_wavelength >= start:
                    xticks.append((start + end) / 2)
                    xticklabels.append(color)

            # Add UV and IR labels
            if min_wavelength <= uv_range[1]:
                xticks.append((uv_range[0] + uv_range[1]) / 2)
                xticklabels.append("UV")
            if max_wavelength >= ir_range[0]:
                xticks.append((ir_range[0] + ir_range[1]) / 2)
                xticklabels.append("IR")

            ax2.set_xticks(xticks)
            ax2.set_xticklabels(xticklabels, rotation=45, ha="center", color='gray')

    def _plot_individual_spectra(self, ax, df, cmap, plot_gradient):
        """
        Helper method to plot individual spectral lines with optional gradient coloring.
        Includes a global colorbar labeled 'Start' and 'End' if gradient is enabled.
        """
        unique_file_indices = df[['name', 'spectrometer_id']].drop_duplicates()

        # Use a shared colormap and normalization for consistent coloring and global colorbar
        if plot_gradient:
            shared_cmap = plt.get_cmap('viridis')  # Choose a continuous colormap
            all_datetimes = pd.to_datetime(df['datetime'])
            norm = plt.Normalize(all_datetimes.min().timestamp(), all_datetimes.max().timestamp())
        else:
            shared_cmap = cmap
            norm = None  # Not needed when not plotting gradient

        for i, (name, spectrometer_id) in enumerate(unique_file_indices.values):
            subset = df[(df['name'] == name) & (df['spectrometer_id'] == spectrometer_id)]
            wavelengths = subset.columns[5:].astype(float)
            datetimes = pd.to_datetime(subset['datetime'])

            for j, (_, row) in enumerate(subset.iterrows()):
                label = f'{name}' if j == 0 else None
                color = self._get_line_color(shared_cmap, i, plot_gradient, datetimes, norm, j)
                ax.plot(wavelengths, row[5:], label=label, color=color, lw=1)

        # Add one global colorbar if using gradient
        if plot_gradient:
            sm = plt.cm.ScalarMappable(cmap=shared_cmap, norm=norm)
            sm.set_array([])
            cbar = plt.colorbar(sm, ax=ax, orientation='horizontal', pad=0.2)
            cbar.set_ticks([norm.vmin, norm.vmax])
            cbar.set_ticklabels(['Start', 'End'])
    


    def _get_line_color(self, cmap, i, plot_gradient, datetimes, norm, index, fig=None, ax=None):
        """
        Get the color for a spectral line using either a shared colormap and normalization
        or a static colormap if gradient coloring is disabled.

        Parameters:
        cmap (Colormap): The shared colormap for assigning colors.
        i (int): Index of the current plot (used only when gradient is False).
        plot_gradient (bool): Whether to use gradient coloring.
        datetimes (Series): Datetime data for the spectra.
        norm (Normalize): A normalization object for mapping timestamps to [0, 1].
        index (int): Index of the current data point.
        fig (Figure): Unused (kept for compatibility).
        ax (Axes): Unused (kept for compatibility).

        Returns:
        color: The color for the plotted line.
        """
        if plot_gradient:
            timestamp = datetimes.iloc[index].timestamp()
            return cmap(norm(timestamp))

        return cmap(i % cmap.N)

    def _plot_by_spectrometer_id(self, ax, df, cmap, show_color_background, title, plot_average=False, subplot=False):
        """
        Plot spectral data grouped by spectrometer ID, with the ability to plot averages.

        Parameters:
        ax (Axes): Matplotlib Axes object to plot on.
        df (DataFrame): The DataFrame containing spectral data to plot.
        cmap (Colormap): Colormap for assigning colors to the plots.
        show_color_background (bool): Whether to add color-coded backgrounds.
        title (str): Title for the plot.
        plot_average (bool): Whether to plot average spectra for each spectrometer ID.
        """
        # Get the minimum and maximum wavelengths from the data
        wavelength_columns = df.columns[5:].astype(float)
        min_wavelength, max_wavelength = wavelength_columns.min(), wavelength_columns.max()
        

        # Add color background and labels if enabled
        if show_color_background:
            self._add_color_backgrounds(ax, min_wavelength, max_wavelength, subplot)

        spectrometer_ids = df['spectrometer_id'].unique()
        
        color_map = {spectrometer_id: cmap(i) for i, spectrometer_id in enumerate(spectrometer_ids)}

        for spectrometer_id in spectrometer_ids:
            subset = df[df['spectrometer_id'] == spectrometer_id]
            name = "Upper spectrometer" if spectrometer_id == '300' else "Lower spectrometer"

            if plot_average:                
                mean_spectrum = subset.iloc[:, 5:].mean(axis=0)
                wavelengths = mean_spectrum.index.astype(float)
                label = f"Average {name}"
                ax.plot(wavelengths, mean_spectrum, label=label, color=color_map[spectrometer_id], lw=2)
            else:
                # Plot individual spectra
                for j, (_, row) in enumerate(subset.iterrows()):
                    wavelengths = row.index[5:].astype(float)
                    label = f'{name}' if j == 0 else None
                    ax.plot(wavelengths, row[5:], label=label, color=color_map[spectrometer_id], lw=0.5)

        # Set plot labels and title
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Spectral Value')
        ax.set_title(title if title else 'Spectral Data Grouped by Spectrometer ID')
        ax.grid(True, which='both', linewidth=1, alpha=1)

    def _plot_average_spectra(self, ax, cmap):
        """
        Plot average spectra computed from the data.

        Parameters:
        ax (Axes): Matplotlib Axes object to plot on.
        cmap (Colormap): Colormap for assigning colors to the plots.
        """
        # Compute average spectra using the analyzer
        avg_spectra_df = self.analyzer.average_spectra()
        
        # Get the wavelength columns (starting after metadata columns)
        wavelengths = avg_spectra_df.columns[5:].astype(float)
        
        # Plot each average spectrum
        for i, row in avg_spectra_df.iterrows():
            ax.plot(wavelengths, row[5:], label=f"Average {row['name']}", color=cmap(i % cmap.N), lw=2)

    def plot_spectra(self, use_standardized=False, use_normalized=False, plot_average=False, 
                     group_by_spectrometer_id=False, show_color_background=True, 
                     plot_gradient=False, title=None, save_path=None):
        """
        Main plotting function to visualize individual or average spectra, or group by spectrometer ID.

        Parameters:
        use_standardized (bool): Whether to use standardized spectral data.
        use_normalized (bool): Whether to use normalized spectral data.
        plot_average (bool): Whether to plot average spectra.
        group_by_spectrometer_id (bool): Whether to group data by spectrometer ID.
        show_color_background (bool): Whether to show wavelength-specific color backgrounds.
        plot_gradient (bool): Whether to apply gradient coloring based on timestamps.
        title (str): Title for the plot.
        save_path (str): File path to save the plot. If None, the plot will be displayed.
        """

        if use_standardized:
            df_to_plot = self._get_standardized_data()
        elif use_normalized:
            df_to_plot = self._get_normalized_data()
        else:
            df_to_plot = self.df

        cmap = plt.get_cmap('tab10')
        fig, ax = plt.subplots(figsize=(16, 12))

        if group_by_spectrometer_id:
            self._plot_by_spectrometer_id(ax, df_to_plot, cmap, show_color_background, title, plot_average)
        else:
            self._plot_spectra(ax, df_to_plot, title, show_color_background, plot_gradient, plot_average, subplot=False)

        
            # Add legend with customized linewidth
        legend = ax.legend(loc='upper left', fontsize=20)  # Explicitly create the legend
        if legend:
            for line in legend.get_lines():
                line.set_linewidth(4.0)  # Set the linewidth of the legend lines



        # Save or show the plot
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()

    def _plot_spectra(self, ax, df, title, show_color_background, plot_gradient=False, plot_average=False, subplot=False):
        """
        Internal method for plotting spectra with customization.

        Parameters:
        ax (Axes): Matplotlib Axes object.
        df (DataFrame): The DataFrame containing spectral data to plot.
        plot_average (bool): Whether to plot average spectra.
        show_color_background (bool): Whether to show wavelength-specific color backgrounds.
        plot_gradient (bool): Whether to apply gradient coloring based on timestamps.
        title (str): Title for the plot.
        subplot (bool): Whether this is a subplot, used to deactivate the top color labels on x-axis for the lower subplot.
        """
        # Compute wavelength range
        wavelength_columns = df.columns[5:].astype(float)
        min_wavelength, max_wavelength = wavelength_columns.min(), wavelength_columns.max()

        # Add color backgrounds if enabled
        if show_color_background:
            self._add_color_backgrounds(ax, min_wavelength, max_wavelength, subplot)

        # Plot individual or average spectra
        cmap = plt.get_cmap('tab10')
        if plot_average:
            self._plot_average_spectra(ax, cmap)
        else:
            self._plot_individual_spectra(ax, df, cmap, plot_gradient)

        # Set labels and title
        ax.set_xlabel('Wavelength (nm)')
        ax.set_ylabel('Spectral Value')
        ax.set_title(title if title else 'Spectral Data')
        # Add gridlines to the plot
        ax.grid(True, which='both', linewidth=1, alpha=1)


    def plot_subplots(self, processor1_df, processor2_df, processor1_label="Processor 1", processor2_label="Processor 2",
                    use_standardized=False, use_normalized=False, show_color_background=True, title=None, save_path=None,
                    group_by_spectrometer_id=False, gradient=False):
        """
        Plot spectral data from two different processors in subplots with specific formatting.

        Parameters:
        processor1_df (DataFrame): Spectral data from processor 1.
        processor2_df (DataFrame): Spectral data from processor 2.
        processor1_label (str): Label for the first processor's data.
        processor2_label (str): Label for the second processor's data.
        use_standardized (bool): Whether to use standardized spectral data.
        use_normalized (bool): Whether to use normalized spectral data.
        show_color_background (bool): Whether to show wavelength-specific color backgrounds.
        show_color_labels (bool): Whether to show color labels (UV, visible, IR) for the upper subplot.
        save_path (str): File path to save the plot. If None, the plot will be displayed.
        """
        # Validate inputs
        if not isinstance(processor1_df, pd.DataFrame):
            raise TypeError(f"Expected processor1_df to be a pandas DataFrame, but got {type(processor1_df).__name__}")
        if not isinstance(processor2_df, pd.DataFrame):
            raise TypeError(f"Expected processor2_df to be a pandas DataFrame, but got {type(processor2_df).__name__}")

        # Determine which data to use
        if use_standardized:
            analyzer1 = SpectralDataAnalyzer(processor1_df)
            analyzer2 = SpectralDataAnalyzer(processor2_df)
            processor1_df = analyzer1.standardize_spectral_data()
            processor2_df = analyzer2.standardize_spectral_data()
        if use_normalized:
            analyzer1 = SpectralDataAnalyzer(processor1_df)
            analyzer2 = SpectralDataAnalyzer(processor2_df)
            processor1_df = analyzer1.normalize_spectral_data()
            processor2_df = analyzer2.normalize_spectral_data()

        # Create subplots
        cmap = plt.get_cmap('tab10')
        fig, axs = plt.subplots(2, 1, figsize=(16, 10), sharex=True)
        fig.suptitle(title if title else 'Spectral Data Comparison')


        # How to plot the data
        if group_by_spectrometer_id:
            self._plot_by_spectrometer_id(axs[0], processor1_df, cmap, show_color_background, title, plot_average=False, subplot=False)
            self._plot_by_spectrometer_id(axs[1], processor2_df, cmap, show_color_background, title, plot_average=True, subplot=True)
        elif gradient:
            self._plot_individual_spectra(axs[0], processor1_df, cmap, plot_gradient=True)
            self._plot_individual_spectra(axs[1], processor2_df, cmap, plot_gradient=True)
        else:
             self._plot_spectra(axs[0], processor1_df, title=processor1_label, show_color_background=show_color_background, subplot=False)
             self._plot_spectra(axs[1], processor2_df, title=processor2_label, show_color_background=show_color_background, subplot=True)


        # Plot data from processor 1
        axs[0].set_title(processor1_label, fontsize=20)  # Add subtitle for the upper subplot
        legend = axs[0].legend(loc='upper left', title='Data')  # Create the legend
        if legend:
            for line in legend.get_lines():
                line.set_linewidth(4.0)  # Increase the linewidth of legend lines
        axs[0].set_xlabel("")  # Remove x-axis label for the upper subplot

        # Plot data from processor 2
        axs[1].set_title(processor2_label, fontsize=20)  # Add subtitle for the lower subplot
        legend = axs[1].legend(loc='upper left', title='Data')  # Create the legend
        if legend:
            for line in legend.get_lines():
                line.set_linewidth(4.0)  # Increase the linewidth of legend lines
        axs[1].set_xlabel('Wavelength (nm)')  # Add x-axis label only for the lower subplot



        # Ensure no upper x-axis (color labels) is added for the lower subplot
        #axs[1].tick_params(axis='x', which='both', top=False, labeltop=False)

        # Add y-axis labels for both subplots
        axs[0].set_ylabel('Spectral Value')
        axs[1].set_ylabel('Spectral Value')

        # Adjust layout
        plt.tight_layout()
        

        # Save or display the plot
        if save_path:
            plt.savefig(save_path)
        else:
            plt.show()