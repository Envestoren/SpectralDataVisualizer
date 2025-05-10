from datetime import date
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from scipy.signal import savgol_filter


class SpectralDataAnalyzer:
    """
    A class for analyzing spectral data, with methods for standardization, normalization,
    smoothing, and averaging spectra. The input DataFrame must contain metadata columns:
    'name', 'spectrometer_id', 'file_index', 'datetime', and optionally 'integration_time',
    followed by spectral data columns.
    """

    def __init__(self, df):
        """
        Initialize the SpectralDataAnalyzer object.

        Parameters:
        df (DataFrame): Input DataFrame containing spectral data and metadata.
        """
        self.df = df
        self.smooth_data = None

    def _add_metadata_to_dataframe(self, base_df, spectral_df):
        """
        Helper method to add metadata columns back to the transformed spectral data.

        Parameters:
        base_df (DataFrame): Original DataFrame containing metadata and spectral data.
        spectral_df (DataFrame): Transformed DataFrame with only spectral data.

        Returns:
        DataFrame: Combined DataFrame with metadata and spectral data.
        """
        # Identify metadata columns
        metadata_columns = ['name', 'spectrometer_id', 'file_index', 'datetime']
        
        # Create a DataFrame with metadata
        metadata_df = base_df[metadata_columns].reset_index(drop=True)

        # Concatenate metadata and spectral data along the columns (axis=1)
        combined_df = pd.concat([metadata_df, spectral_df.reset_index(drop=True)], axis=1)

        return combined_df

    def standardize_spectral_data(self):
        """
        Standardize the spectral data (z-score scaling).

        Returns:
        DataFrame: DataFrame with standardized spectral data and original metadata.
        """
        spectral_data = self.df.iloc[:, 5:]  # Spectral data starts from column index 5
        scaler = StandardScaler()
        standardized_data = scaler.fit_transform(spectral_data)
        standardized_df = pd.DataFrame(standardized_data, columns=spectral_data.columns)
        return self._add_metadata_to_dataframe(self.df, standardized_df)

    def normalize_spectral_data(self):
        """
        Normalize the spectral data to a range of [0, 1].

        Returns:
        DataFrame: DataFrame with normalized spectral data and original metadata.
        """
        spectral_data = self.df.iloc[:, 5:]
        min_vals = spectral_data.min(axis=1)
        max_vals = spectral_data.max(axis=1)
        normalized_data = (spectral_data.subtract(min_vals, axis=0)).div(max_vals - min_vals, axis=0)
        normalized_df = pd.DataFrame(normalized_data, columns=spectral_data.columns)
        return self._add_metadata_to_dataframe(self.df, normalized_df)

    def average_spectra(self):
        """
        Calculate the average spectrum for each unique file index.

        Returns:
        DataFrame: DataFrame containing the average spectrum for each file index.
        """
        avg_spectra_list = []
        unique_file_indices = self.df['file_index'].unique()

        for file_index in unique_file_indices:
            subset = self.df[self.df['file_index'] == file_index]
            name = subset['name'].iloc[0]
            spectrometer_id = subset['spectrometer_id'].iloc[0]
            datetime = subset['datetime'].iloc[0]
            avg_spectra = subset.iloc[:, 5:].mean(axis=0)
            avg_spectra_list.append([name, spectrometer_id, file_index,  datetime] + avg_spectra.tolist())

        avg_spectra_columns = [ 'name', 'spectrometer_id', 'file_index', "datetime"] + self.df.columns[5:].tolist()
        return pd.DataFrame(avg_spectra_list, columns=avg_spectra_columns)
    
    def smooth_spectral_data(self, window_length=5, polyorder=2):
        """
        Apply Savitzky-Golay filter to smooth the spectral data.

        Parameters:
        window_length (int): The length of the filter window (must be odd).
        polyorder (int): The order of the polynomial used to fit the samples.

        Returns:
        DataFrame: Smoothed spectral data with original metadata.
        """
        spectral_data = self.df.iloc[:, 5:]
        smoothed_data = savgol_filter(spectral_data, window_length=window_length, polyorder=polyorder, axis=1)
        smoothed_df = pd.DataFrame(smoothed_data, columns=spectral_data.columns)
        smoothed_df = self._add_metadata_to_dataframe(self.df, smoothed_df)
        self.smooth_data = smoothed_df
        return smoothed_df

    def normalize_by_integration_time(self):
        """
        Normalize the spectral data by dividing each value by the 'integration_time' column.

        Returns:
        DataFrame: Spectral data normalized by integration time.

        Raises:
        ValueError: If the 'integration_time' column is missing in the DataFrame.
        """
        if 'integration_time' not in self.df.columns:
            raise ValueError("The DataFrame does not contain 'integration_time' column.")

        spectral_columns = self.df.columns[5:]
        self.df[spectral_columns] = self.df[spectral_columns].div(self.df['integration_time'], axis=0)
        return self.df