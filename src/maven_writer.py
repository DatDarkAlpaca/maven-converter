import csv
from maven_properties import MavenData


def write_csv_maven(filepath: str, maven_data: MavenData):
    headers = [
        'Electron Density (y)',
        'TT2000 Time,Unix Time (x)',
        'Lower Uncertainty (dv)',
        'Upper Uncertainty (dy)',
        'Data Quality Flag (flag)',
        'Instrument Information (info)'
    ]

    with open(filepath, mode='w', newline='') as file:
        writer = csv.writer(file, quoting=csv.QUOTE_ALL)
        writer.writerow(headers)

        for row in zip(maven_data.electron_density_values, maven_data.tt2000_time_values, 
                       maven_data.unix_time_values, maven_data.lower_uncertainty_values, maven_data.upper_uncertainty_values,
                       maven_data.data_quality_values, maven_data.instrument_information_values):
            writer.writerow(row)
