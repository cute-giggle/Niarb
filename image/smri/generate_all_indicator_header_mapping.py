# Author: cute-giggle@outlook.com


import pandas as pd
import os


DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
BENCHMARK_DIR = os.path.join(DATA_DIR, 'benchmark/smri')


def drop_unuseful_rows(data: pd.DataFrame):

    """Drop rows that have 'None' or 'disable' in the second or third column."""

    data.drop(index=data[(data['header_name'] == 'None')].index, inplace=True)
    data.drop(index=data[(data['is_enabled'] == 'disable')].index, inplace=True)


def generate_all_indicator_header_mapping():
    
    """Generate all indicator-header mapping."""
    
    aseg_global_mapping_data = pd.read_csv(os.path.join(BENCHMARK_DIR, 'mapping', 'aseg_global_mapping.csv'))
    drop_unuseful_rows(aseg_global_mapping_data)
    aseg_part_mapping_data = pd.read_csv(os.path.join(BENCHMARK_DIR, 'mapping', 'aseg_part_mapping.csv'))
    drop_unuseful_rows(aseg_part_mapping_data)
    aseg_part_ext_mapping_data = pd.read_csv(os.path.join(BENCHMARK_DIR, 'mapping', 'aseg_part_ext_mapping.csv'))
    drop_unuseful_rows(aseg_part_ext_mapping_data)

    aparc_part_mapping_data = pd.read_csv(os.path.join(BENCHMARK_DIR, 'mapping', 'aparc_part_mapping.csv'))
    drop_unuseful_rows(aparc_part_mapping_data)
    aparc_part_ext_mapping_data = pd.read_csv(os.path.join(BENCHMARK_DIR, 'mapping', 'aparc_part_ext_mapping.csv'))
    drop_unuseful_rows(aparc_part_ext_mapping_data)

    buffer = []
    for _, row in aseg_global_mapping_data.iterrows():
        buffer.append([row['indicator_name'], row['header_name'], row['units']])
    for _, row1 in aseg_part_mapping_data.iterrows():
        for _, row2 in aseg_part_ext_mapping_data.iterrows():
            indicator_name = row1['indicator_name'] + ' ' + row2['description']
            header_name = row1['header_name'] + '_' + row2['header_name']
            buffer.append([indicator_name, header_name, row2['units']])
    for _, row1 in aparc_part_mapping_data.iterrows():
        for _, row2 in aparc_part_ext_mapping_data.iterrows():
            indicator_name = row1['indicator_name'] + ' ' + row2['description']
            header_name = row1['header_name'] + '_' + row2['header_name']
            buffer.append([indicator_name, header_name, row2['units']])

    result = pd.DataFrame(buffer, columns=['indicator_name', 'header_name', 'units'])
    print(result)
    result.to_csv(os.path.join(BENCHMARK_DIR, 'mapping', 'all_indicator_header_mapping.csv'), index=False)


if __name__ == '__main__':
    generate_all_indicator_header_mapping()
