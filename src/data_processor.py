import pandas as pd
import numpy as np
from datetime import datetime
from os import path
from scipy.interpolate import interp1d

class SpectralDataProcessor:
    def __init__(self, list_of_paths, wavelength_range=(200, 1050), interpolation_points=3648, shift_300nm=2):  # 3648 is the number of points in the spectrometer
        if wavelength_range[0] < 200 or wavelength_range[1] > 1050:
            raise ValueError("Invalid wavelength range, must be within 200 and 1050 nm")
        self.list_of_paths = list_of_paths
        self.wavelength_range = wavelength_range
        self.interpolation_points = interpolation_points
        self.shift_300nm = shift_300nm
        self.df = self.process_files()

    def read_spectral_data(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        path_name = path.basename(file_path)
        path_name = path.splitext(path_name)[0]

        spectrometer_line = next(line for line in lines if line.startswith('Spectrometer:'))
        spectrometer_id = spectrometer_line.split(':')[1].strip()[-3:]
        
        try:
            name_line = next(line for line in lines if line.startswith('Name:'))
            name = name_line.split(':')[1].strip()
        except StopIteration:
            raise ValueError(f"The file {file_path} is missing the 'Name' line.")

        try:
            integration_time_line = next(line for line in lines if line.startswith('Integration Time (sec):'))
            integration_time = float(integration_time_line.split(':')[1].strip())
        except StopIteration:
            raise ValueError(f"The file {file_path} is missing the 'Integration Time (sec):' line.")
        except ValueError:
            raise ValueError(f"Invalid format for 'Integration Time (sec):' in file {file_path}.")

        start_index = next(i for i, line in enumerate(lines) if '>>>>>Begin Spectral Data<<<<<' in line) + 1
        wavelengths = np.array(lines[start_index].split(), dtype=float)
        spectral_data_lines = lines[start_index + 1:]

        data = []
        for line in spectral_data_lines:
            components = line.split()
            if len(components) < 3:
                continue
            try:
                datetime_str = f"{components[0]} {components[1]}"
                datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')
                values = list(map(float, components[2:]))
                data.append([datetime_obj, path_name, spectrometer_id, name, integration_time] + values)
            except ValueError:
                continue

        column_names = ['datetime', 'file_index', 'spectrometer_id', 'name', 'integration_time'] + list(wavelengths)
        df = pd.DataFrame(data, columns=column_names)
        
        # Adjust the starting wavelength for spectrometer 300
        if spectrometer_id == '300':
            df.columns = df.columns[:5].tolist() + [str(float(w) + self.shift_300nm) for w in df.columns[5:]]

        return df

    def process_files(self):
        all_dfs = []
        for file_path in self.list_of_paths:
            print(f"Processing file: {file_path}")
            try:
                df = self.read_spectral_data(file_path)
                if df.empty:
                    print(f"Warning: {file_path} is empty.")
                    continue

                first_five_columns = df.iloc[:, :5]
                numeric_columns = df.columns[5:].to_series().apply(pd.to_numeric, errors='coerce')
                filtered_columns = numeric_columns[(numeric_columns >= self.wavelength_range[0]) & (numeric_columns <= self.wavelength_range[1])].index
                filtered_df = pd.concat([first_five_columns, df.loc[:, filtered_columns]], axis=1)

                common_wavelengths = np.round(np.linspace(self.wavelength_range[0], self.wavelength_range[1], num=self.interpolation_points), 2)
                interpolated_data = pd.DataFrame(index=filtered_df.index, columns=common_wavelengths)

                for i in range(filtered_df.shape[0]):
                    f = interp1d(filtered_df.columns[5:].astype(float), filtered_df.iloc[i, 5:], kind='linear', fill_value="extrapolate")
                    interpolated_data.iloc[i, :] = np.round(f(common_wavelengths), 2)

                result_df = pd.concat([first_five_columns, interpolated_data], axis=1)
                all_dfs.append(result_df)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")

        if not all_dfs:
            raise ValueError("No valid data files found to process.")
        
        final_df = pd.concat(all_dfs, ignore_index=True)
        return final_df
    
    def export_to_excel(self, file_path):
        self.df.to_excel(file_path, index=False)