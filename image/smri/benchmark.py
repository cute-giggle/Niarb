# Author: cute-giggle@outlook.com


import pandas as pd
import os
import numpy as np
import sys


DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
BENCHMARK_DIR = os.path.join(DATA_DIR, 'benchmark/smri')

HCP_DIR = os.path.join(DATA_DIR, 'hcp')
HCP_1200_GROUP_AVERAGE_DIR = os.path.join(HCP_DIR, 'HCP_1200_GroupAverage')
HCP_1200_GROUP_AVERAGE_FREESURFER_DATA_PATH = os.path.join(HCP_1200_GROUP_AVERAGE_DIR, 'unrestricted_hcp_freesurfer.csv')


def get_all_header_mapping():

    """Load all header-indicator and header-units mapping."""

    all_indicator_header_mapping_path = os.path.join(BENCHMARK_DIR, 'mapping', 'all_indicator_header_mapping.csv')
    all_indicator_header_mapping_data = pd.read_csv(all_indicator_header_mapping_path)

    all_header_indicator_mapping = {}
    all_header_units_mapping = {}

    for _, row in all_indicator_header_mapping_data.iterrows():
        all_header_indicator_mapping[row['header_name']] = row['indicator_name']
        all_header_units_mapping[row['header_name']] = row['units']

    return all_header_indicator_mapping, all_header_units_mapping


def load_hcp_1200_group_average_freesurfer_data():

    """Load HCP 1200 Group Average Freesurfer stat data."""

    hcp_1200_group_average_freesurfer_data = pd.read_csv(HCP_1200_GROUP_AVERAGE_FREESURFER_DATA_PATH)
    # print(hcp_1200_group_average_freesurfer_data)

    return hcp_1200_group_average_freesurfer_data


def save_benchmark(benchmark_data: pd.DataFrame):

    """Save benchmark data to csv file."""

    benchmark_data.to_csv(os.path.join(BENCHMARK_DIR, 'benchmark.csv'), index=False, header=True)


def load_benchmark():

    """Load benchmark data from csv file."""

    benchmark_data = pd.read_csv(os.path.join(BENCHMARK_DIR, 'benchmark.csv'))
    # print(benchmark_data)

    return benchmark_data


def load_benchmark_dict():
    
    """Load benchmark data from csv file and convert to dict."""

    benchmark_data = load_benchmark()
    benchmark = {}
    
    for index, row in benchmark_data.iterrows():
        benchmark[row['indicator_name']] = {
            'mean': row['mean'],
            'stddev': row['stddev'],
            'max': row['max'],
            'min': row['min'],
            'distribution': row['distribution'],
            'units': row['units'],
            'low_bound': row['low_bound'],
            'high_bound': row['high_bound'],
        }
    
    return benchmark


def generate_benchmark():

    """Generate benchmark data."""

    image_pkg_dir = os.path.join(os.path.dirname(__file__), '../../')
    if image_pkg_dir not in sys.path:
        sys.path.append(image_pkg_dir)
    from image.dmri.distribution_fitter import DistributionFitter

    hcp_1200_group_average_freesurfer_data = load_hcp_1200_group_average_freesurfer_data()

    header_indicator_mapping, header_units_mapping = get_all_header_mapping()

    header_list = hcp_1200_group_average_freesurfer_data.columns
    benchmark_data = []

    for header_name in header_list:
        if header_name not in header_indicator_mapping:
            continue

        indicator_name = header_indicator_mapping[header_name]
        units = header_units_mapping[header_name]
        data = np.array(hcp_1200_group_average_freesurfer_data[header_name].values, dtype=np.float32)

        if not DistributionFitter.is_guassian(data):
            this_benchmark_data = [indicator_name, np.mean(data), np.std(data), np.min(data), np.max(data), units, 'None', np.min(data), np.max(data)]
        else:
            mean, stddev = DistributionFitter.fit_gussian(data, plot=False)
            this_benchmark_data = [indicator_name, np.mean(data), np.std(data), np.min(data), np.max(data), units, 'Gaussian', mean - 3 * stddev, mean + 3 * stddev]

        benchmark_data.append(this_benchmark_data)

    benchmark_data = pd.DataFrame(benchmark_data, columns=['indicator_name', 'mean', 'stddev', 'min', 'max', 'units', 'distribution', 'low_bound', 'high_bound'])
    # print(benchmark_data)
    save_benchmark(benchmark_data)


if __name__ == '__main__':    
    generate_benchmark()