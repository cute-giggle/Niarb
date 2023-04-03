# Author: cute-giggle@outlook.com


import os
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


class NetworkAnalyser:
    def __init__(self, correlation_matrix: np.ndarray):
        assert(correlation_matrix.shape[0] == correlation_matrix.shape[1])
        self.correlation_matrix = correlation_matrix
        self.preprocess()

    @staticmethod
    def normalise(matrix: np.ndarray):
        range = np.max(matrix) - np.min(matrix)
        return (matrix - np.min(matrix)) / range

    def preprocess(self):
        self.correlation_matrix = np.where(self.correlation_matrix < 0, 0, self.correlation_matrix)
        np.fill_diagonal(self.correlation_matrix, 0)
        self.correlation_matrix = self.normalise(self.correlation_matrix)
        np.fill_diagonal(self.correlation_matrix, 0)

    def calculate_weighted_degree(self):
        return np.sum(self.correlation_matrix, axis=0)

    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def binarise(self, threshold: float):
        return np.where(self.correlation_matrix > threshold, 1, 0)
    
    @staticmethod
    def get_edge_percent_dict():
        return {
            '10.0 percent edges count': 0.100,
            '15.0 percent edges count': 0.150,
        }

    def analyse(self, save_img_dir=None):
        result = {}
        result['weighted degree'] = self.calculate_weighted_degree()

        edge_percent_dict = self.get_edge_percent_dict()

        for edge_percent_name, edge_percent in edge_percent_dict.items():
            keep_edge_num = int(self.correlation_matrix.shape[0] * self.correlation_matrix.shape[1] * edge_percent)
            threshold = np.sort(self.correlation_matrix.flatten())[-keep_edge_num]
            print('Edge percent: {}%, threshold: {}'.format(edge_percent * 100, threshold))
            binarised_correlation_matrix = self.binarise(threshold)
            if save_img_dir is not None:
                plt.title(edge_percent_name)
                plt.imshow(binarised_correlation_matrix)
                figname = '_'.join(edge_percent_name.split(' '))
                plt.savefig(os.path.join(save_img_dir, '{}.png'.format(figname)))
                plt.close()
            graph = nx.Graph(binarised_correlation_matrix)

            result[edge_percent_name] = {
                'global efficiency': nx.global_efficiency(graph),
                'local efficiency': nx.local_efficiency(graph),
                'average clustering': nx.average_clustering(graph),
            }
            print(result[edge_percent_name])

        return result
