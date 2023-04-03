# Author: cute-giggle@outlook.com


import os
import sys
import pandas as pd


def prepare_env():
    image_pkg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
    if image_pkg_dir not in sys.path:
        sys.path.append(image_pkg_dir)


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
WORKING_DIR = os.path.join(DATA_DIR, 'working/smri/subjects')
BENCHMARK_DIR = os.path.join(DATA_DIR, 'benchmark/smri')


class Processor:
    def __init__(self, subj_id):
        self.subj_id = subj_id
        self.subj_dir = os.path.join(WORKING_DIR, self.subj_id)
        os.environ['SUBJECTS_DIR'] = self.subj_dir

    def load_stat_data(self):
        from .parse_freesurfer_stat_file import parse_aseg_stat_file, parse_aparc_stat_file

        aseg_data_path = os.path.join(self.subj_dir, 'preprocess_result/aseg.stats')
        lh_aparc_data_path = os.path.join(self.subj_dir, 'preprocess_result/lh.aparc.stats')
        rh_aparc_data_path = os.path.join(self.subj_dir, 'preprocess_result/rh.aparc.stats')

        aseg_data = parse_aseg_stat_file(aseg_data_path)
        lh_aparc_data = parse_aparc_stat_file(lh_aparc_data_path)
        rh_aparc_data = parse_aparc_stat_file(rh_aparc_data_path)

        return pd.concat([aseg_data, lh_aparc_data, rh_aparc_data], axis=0)
    
    def load_benchmark(self):
        from .benchmark import load_benchmark_dict
        return load_benchmark_dict()

    def run(self, preprocessed: bool = False):
        from .preprocessor import preprocess
        from .report_generator import ReportGenerator

        if not preprocessed:
            preprocess(self.subj_id, self.subj_dir, True)

        stat_data = self.load_stat_data()
        benchmark_data = self.load_benchmark()

        report = ReportGenerator(benchmark_data, stat_data).generate()

        report_dir = os.path.join(self.subj_dir, 'report_result')
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)
        report.to_csv(os.path.join(report_dir, 'report.csv'), index=False)

        print(report)

        return report


if __name__ == '__main__':
    subj_id = 'demo_001'
    report = Processor(subj_id).run(True)
