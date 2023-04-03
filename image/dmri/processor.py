# Author: cute-giggle@outlook.com


import os
import sys
import scipy.io as sio
import json

def prepare_env():
    image_pkg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
    if image_pkg_dir not in sys.path:
        sys.path.append(image_pkg_dir)


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
WORKING_DIR = os.path.join(DATA_DIR, 'working/dmri/subjects')
FIXED_ATLAS_PATH = os.path.join(DATA_DIR, 'mni/parcellation/shaefer2018/Schaefer2018_200Parcels_17Networks_order_FSLMNI152_1mm.nii.gz')
BENCHMARK_PATH = os.path.join(DATA_DIR, 'benchmark/dmri/benchmark.json')


class Processor:
    def __init__(self, subj_id: str):
        self.subj_id = subj_id
        self.subj_dir = os.path.join(WORKING_DIR, self.subj_id)
        self.atlas_path = FIXED_ATLAS_PATH

    def load_benchmark(self):
        with open(BENCHMARK_PATH, 'r') as f:
            benchmark = json.load(f)
        return benchmark

    def run(self, preprocessed: bool = False):
        prepare_env()
        from image.dmri.preprocessor import DefaultPreprocessor
        from image.dmri.report_generator import ReportGenerator
        
        if not preprocessed:
            DefaultPreprocessor(self.subj_id, self.subj_dir, self.atlas_path).run()

        correlation_matrix_path = os.path.join(self.subj_dir, 'preprocess_result/connectivity_matrix.mat')
        correlation_matrix = sio.loadmat(correlation_matrix_path)['connectivity']
        benchmark = self.load_benchmark()

        report_dir = os.path.join(self.subj_dir, 'report_result')
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        report = ReportGenerator(benchmark, correlation_matrix).generate(report_dir)
        report.to_csv(os.path.join(report_dir, 'report.csv'), index=False)
        
        # print(report)
        
        return report


if __name__ == '__main__':
    subj_id = 'demo_001'
    Processor(subj_id).run()
