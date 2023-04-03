# Author: cute-giggle@outlook.com


import os
import sys


DMRI_BENCHMARK_DIR = os.path.join(os.path.dirname(__file__), '../../data/benchmark/dmri')
CORRELATION_MATRIX_NAME = 'Counts.csv'


if __name__ == '__main__':
    image_pkg_dir = os.path.join(os.path.dirname(__file__), '../../')
    if image_pkg_dir not in sys.path:
        sys.path.append(image_pkg_dir)
    from image.dmri.benchmark_genetator import DefaultBenchmarkGenerator
    benchmark_generator = DefaultBenchmarkGenerator(DMRI_BENCHMARK_DIR, CORRELATION_MATRIX_NAME)
    benchmark_generator.generate()
