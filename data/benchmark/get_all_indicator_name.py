# Author: cute-giggle@outlook.com


import os
import pandas as pd
import json


def get_smri_indicator_name():
    benchmark_path = os.path.join(os.path.dirname(__file__), 'smri/benchmark.csv')
    benchmark = pd.read_csv(benchmark_path)
    return benchmark['indicator_name'].to_list()


def get_fmri_indicator_name():
    benchmark_path = os.path.join(os.path.dirname(__file__), 'fmri/benchmark.json')
    with open(benchmark_path, 'r') as f:
        benchmark = json.load(f)
    indicator_name = []
    for key, value in benchmark.items():
        if 'distribution' in value:
            indicator_name.append(key)
        else:
            for k, v in value.items():
                indicator_name.append(key + ' ' + k)
    return indicator_name


def get_dmri_indicator_name():
    benchmark_path = os.path.join(os.path.dirname(__file__), 'dmri/benchmark.json')
    with open(benchmark_path, 'r') as f:
        benchmark = json.load(f)
    indicator_name = []
    for key, value in benchmark.items():
        if 'distribution' in value:
            indicator_name.append(key)
        else:
            for k, v in value.items():
                indicator_name.append(key + ' ' + k)
    return indicator_name


def get_all_indicator_name():
    smri_indicator_name = get_smri_indicator_name()
    fmri_indicator_name = get_fmri_indicator_name()
    dmri_indicator_name = get_dmri_indicator_name()
    return pd.DataFrame(smri_indicator_name + fmri_indicator_name + dmri_indicator_name, columns=['indicator_name'])


def main():
    all_indicator_name = get_all_indicator_name()
    all_indicator_name.to_csv(os.path.join(os.path.dirname(__file__), 'all_indicator_name.csv'), index=False)


if __name__ == '__main__':
    main()