# Author: cute-giggle@outlook.com


import numpy as np
import matplotlib.pyplot as plt

from astropy.modeling import models, fitting


class DistributionFitter:
    @staticmethod
    def is_guassian(data: np.ndarray):
        if np.std(data) == 0:
            return False
        skewness, kurtosis = DistributionFitter.calculate_skewness_and_kurtosis(data)
        return abs(skewness) < 0.5 and abs(kurtosis - 3) < 0.5
    
    @staticmethod
    def calculate_skewness_and_kurtosis(data: np.ndarray):
        mean = np.mean(data)
        std = np.std(data)
        skewness = np.mean(((data - mean) / std) ** 3)
        kurtosis = np.mean(((data - mean) / std) ** 4)

        return skewness, kurtosis
    
    @staticmethod
    def fit_gussian(data: np.ndarray, plot: bool = False):
        bins = int(np.sqrt(len(data)))
        y, x = np.histogram(data, bins=bins)

        # remove the last bin and shift the x-axis to the center of the bin
        x = np.delete(x, [-1]) + (x[1] - x[0]) / 2

        init = models.Gaussian1D(amplitude=1., mean=np.mean(data), stddev=np.std(data))
        fitter = fitting.LevMarLSQFitter()
        result = fitter(init, x, y)
        
        if plot:
            plt.plot(x, y, 'ko')
            plt.plot(x, result(x), 'r-')
            plt.show()

        return [result.mean.value, result.stddev.value]
    