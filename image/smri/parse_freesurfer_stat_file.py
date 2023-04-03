# Author: cute-giggle@outlook.com


import pandas as pd
import os
import numpy as np


DATA_DIR = os.path.join(os.path.dirname(__file__), '../../data')
BENCHMARK_DIR = os.path.join(DATA_DIR, 'benchmark/smri')


def load_aparc_part_ext_indicator_description():

    """Load description of aparc part extended indicator."""

    aparc_part_ext_mapping_path = os.path.join(BENCHMARK_DIR, 'mapping', 'aparc_part_ext_mapping.csv')
    aparc_part_ext_mapping_data = pd.read_csv(aparc_part_ext_mapping_path)

    result = {}
    for _, row in aparc_part_ext_mapping_data.iterrows():
        result[row['indicator_name']] = row['description']
    
    return result


def load_aseg_part_ext_indicator_description():

    """Load description of aseg part extended indicator."""

    aseg_part_ext_mapping_path = os.path.join(BENCHMARK_DIR, 'mapping', 'aseg_part_ext_mapping.csv')
    aseg_part_ext_mapping_data = pd.read_csv(aseg_part_ext_mapping_path)

    result = {}
    for _, row in aseg_part_ext_mapping_data.iterrows():
        result[row['indicator_name']] = row['description']
    
    return result


def parse_aseg_stat_file(file_path: str):
    
    """Parse aseg stat file."""

    stat_data = []

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('# Measure'):
                contents = lines[i].strip().split(',')
                if contents[-4] == 'SupraTentorialVolNotVent':
                    contents[-3] = 'SupraTentorialVolNotVent'
                stat_data.append([contents[-3], np.float32(contents[-2])])
            elif lines[i].startswith('# ColHeaders'):
                part_header = lines[i].replace('# ColHeaders', '').strip().split()
                part_table = []
                for j in range(i + 1, len(lines)):
                    part_table.append(lines[j].strip().split())
                part_table = pd.DataFrame(part_table, columns=part_header)
                # print(part_table)
                aseg_part_ext_indicator_description = load_aseg_part_ext_indicator_description()
                for i in range(len(part_table['StructName'])):
                    for indicator_part_ext_name, indicator_part_ext_description in aseg_part_ext_indicator_description.items():
                        indicator_name = part_table['StructName'][i] + ' ' + indicator_part_ext_description
                        indicator_value = np.float32(part_table[indicator_part_ext_name][i])
                        stat_data.append([indicator_name, indicator_value])

    stat_data = pd.DataFrame(stat_data, columns=['indicator_name', 'value'])
    # print(stat_data)
    return stat_data


def parse_aparc_stat_file(file_path: str):

    """Parse aparc stat file."""

    side = 'left' if file_path.split('/')[-1].split('.')[0] == 'lh' else 'right'
    stat_data = []

    with open(file_path, 'r') as f:
        lines = f.readlines()
        for i in range(len(lines)):
            if lines[i].startswith('# ColHeaders'):
                part_header = lines[i].replace('# ColHeaders', '').strip().split()
                part_table = []
                for j in range(i + 1, len(lines)):
                    part_table.append(lines[j].strip().split())
                part_table = pd.DataFrame(part_table, columns=part_header)
                # print(part_table)
                aparc_ext_indicator_description = load_aparc_part_ext_indicator_description()
                for i in range(len(part_table['StructName'])):
                    for indicator_ext_name, indicator_ext_description in aparc_ext_indicator_description.items():
                        indicator_name = side + ' ' + part_table['StructName'][i] + ' ' + indicator_ext_description
                        indicator_value = np.float32(part_table[indicator_ext_name][i])
                        stat_data.append([indicator_name, indicator_value])
    
    stat_data = pd.DataFrame(stat_data, columns=['indicator_name', 'value'])
    # print(stat_data)
    return stat_data
