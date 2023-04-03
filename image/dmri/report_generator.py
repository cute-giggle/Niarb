# Author: cute-giggle@outlook.com


import os
import pandas as pd
import numpy as np


class ReportGenerator:
    def __init__(self, benchmark: dict, correlation_matrix: np.ndarray):
        self.benchmark = benchmark
        self.correlation_matrix = correlation_matrix

    def generate(self, save_img_dir=None):
        from image.dmri.network_analyser import NetworkAnalyser
        network_analyser = NetworkAnalyser(self.correlation_matrix)
        item = network_analyser.analyse(save_img_dir)

        report = []
        for key, value in self.benchmark.items():
            if key == 'cosine similarity of weighted degree':
                cos_sim_of_weighted_degree = NetworkAnalyser.cosine_similarity(item['weighted degree'], value['mean_weighted_degree'])
                conclusion = 'normal' if cos_sim_of_weighted_degree >= value['low_bound'] else 'too low'
                report.append([key, cos_sim_of_weighted_degree, value['units'], conclusion])
                continue
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    if item[key][sub_key] >= sub_value['high_bound']:
                        conclusion = 'too high'
                    elif item[key][sub_key] >= sub_value['low_bound']:
                        conclusion = 'normal'
                    else:
                        conclusion = 'too low'
                    report.append([key + ' ' + sub_key, item[key][sub_key], sub_value['units'], conclusion])

        return pd.DataFrame(report, columns=['indicator_name', 'value', 'units', 'conclusion'])
