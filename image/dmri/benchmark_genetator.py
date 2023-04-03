# Author: cute-giggle@outlook.com

import os
import json
import numpy as np

from image.dmri.network_analyser import NetworkAnalyser
from image.dmri.distribution_fitter import DistributionFitter


class DefaultBenchmarkGenerator:
    def __init__(self, benchmark_dir, correlation_matrix_name):
        self.benchmark_dir = benchmark_dir
        subjects_dir = os.path.join(self.benchmark_dir, 'subjects')
        print('Subjects dir: {}'.format(subjects_dir))
        subjects = [os.path.join(subjects_dir, subject) for subject in os.listdir(subjects_dir) if subject[0] != '.']
        print('Subjects count: {}'.format(len(subjects)))
        self.correlation_matrix_list = [np.loadtxt(os.path.join(subject, correlation_matrix_name), dtype=float) for subject in subjects]
        print("Load correlation matrix list done.")

    def save(self, benchmark):
        with open(os.path.join(self.benchmark_dir, 'benchmark.json'), 'w') as f:
            json.dump(benchmark, f, indent=4)

    def generate_cos_sim_of_weighted_degree_benchmark(self, weighted_degree_list):
        cos_sim_list = []
        mean_weighted_degree = np.mean(weighted_degree_list, axis=0)
        for degree in weighted_degree_list:
            cos_sim_list.append(NetworkAnalyser.cosine_similarity(degree, mean_weighted_degree))
        
        if DistributionFitter.is_guassian(np.array(cos_sim_list)):
            mean, stddev = DistributionFitter.fit_gussian(np.array(cos_sim_list), plot=True)
            distribution = 'gaussian'
            low_bound = -3 * stddev + mean
            high_bound = 3 * stddev + mean
        else:
            mean, stddev = np.mean(cos_sim_list), np.std(cos_sim_list)
            distribution = 'None'
            low_bound = np.min(cos_sim_list)
            high_bound = np.max(cos_sim_list)
        
        return {
            'mean': mean,
            'stddev': stddev,
            'min': np.min(cos_sim_list),
            'max': np.max(cos_sim_list),
            'distribution': distribution,
            'units': 'None',
            'mean_weighted_degree': mean_weighted_degree.tolist(),
            'low_bound': low_bound,
            'high_bound': high_bound
        }


    def generate(self):
        buffer = None
        for correlation_matrix in self.correlation_matrix_list:
            network_analyser = NetworkAnalyser(correlation_matrix)
            item = network_analyser.analyse()
            if buffer is None:
                buffer = item
                for key, value in buffer.items():
                    if not isinstance(value, dict):
                        buffer[key] = [value]
                    else:
                        for k, v in value.items():
                            buffer[key][k] = [v]
                continue
            for key, value in item.items():
                if not isinstance(value, dict):
                    buffer[key].append(value)
                else:
                    for k, v in value.items():
                        buffer[key][k].append(v)

        benchmark = {}
        if 'weighted degree' in buffer:
            benchmark['cosine similarity of weighted degree'] = self.generate_cos_sim_of_weighted_degree_benchmark(buffer['weighted degree'])
        
        for key, value in buffer.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    if DistributionFitter.is_guassian(np.array(v)):
                        mean, stddev = DistributionFitter.fit_gussian(np.array(v), plot=True)
                        distribution = 'gaussian'
                        low_bound = -3 * stddev + mean
                        high_bound = 3 * stddev + mean
                    else:
                        mean, stddev = (np.mean(v), np.std(v))
                        distribution = 'None'
                        low_bound = np.min(v)
                        high_bound = np.max(v)
                    if key not in benchmark:
                        benchmark[key] = {}
                    benchmark[key][k] = {
                        'mean': mean,
                        'stddev': stddev,
                        'min': np.min(v),
                        'max': np.max(v),
                        'distribution': distribution,
                        'units': 'None',
                        'low_bound': low_bound,
                        'high_bound': high_bound
                    }
        self.save(benchmark)
