# Author: cute-giggle@outlook.com


import os
import sys
import glob
import nibabel as nib
import numpy as np
import json

from nibabel.nifti1 import Nifti1Image
from nilearn.maskers import NiftiLabelsMasker
from nilearn.connectome import ConnectivityMeasure


DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../data')
WORKING_DIR = os.path.join(DATA_DIR, 'working/fmri/subjects')
FIXED_ATLAS_PATH = os.path.join(DATA_DIR, 'mni/parcellation/shaefer2018/Schaefer2018_200Parcels_17Networks_order_FSLMNI152_1mm.nii.gz')
BENCHMARK_PATH = os.path.join(DATA_DIR, 'benchmark/fmri/benchmark.json')
FIXED_MNI_TEMPLATE_PATH = os.path.join(DATA_DIR, 'mni/template/MNI152_T1_1mm_Brain.nii.gz')


def prepare_env():
    image_pkg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..')
    if image_pkg_dir not in sys.path:
        sys.path.append(image_pkg_dir)


class Processor:
    def __init__(self, subj_id: str):
        self.subj_id = subj_id
        self.subj_dir = os.path.join(WORKING_DIR, self.subj_id)
        self.mni_tepmlate_path = FIXED_MNI_TEMPLATE_PATH
        self.atlas_path = FIXED_ATLAS_PATH

    def load_benchmark(self):
        with open(BENCHMARK_PATH, 'r') as f:
            benchmark = json.load(f)
        return benchmark

    def load_correlation_matrix(self):
        preprocessed_result_dir = os.path.join(self.subj_dir, 'preprocess_result')
        fmri_path_list = glob.glob(os.path.join(preprocessed_result_dir, 'fmri-r0[1-3]*.nii.gz'))
        fmri_img_list = [nib.load(fmri_path) for fmri_path in fmri_path_list]

        masker = NiftiLabelsMasker(labels_img=nib.load(self.atlas_path), standardize=True)
        time_series = np.mean([masker.fit_transform(fmri_img) for fmri_img in fmri_img_list], axis=0)
        correlation_measure = ConnectivityMeasure(kind='correlation')
        correlation_matrix = correlation_measure.fit_transform([time_series])[0]

        return correlation_matrix

    def run(self, preprocessed: bool = False):
        prepare_env()
        from image.fmri.preprocess import rsfMRI_preprocess
        from image.dmri.report_generator import ReportGenerator

        if not preprocessed:
            rsfMRI_preprocess(self.subj_id, self.subj_dir, self.mni_tepmlate_path, True, True)
        
        correlation_matrix = self.load_correlation_matrix()
        benchmark = self.load_benchmark()

        report_dir = os.path.join(self.subj_dir, 'report_result')
        if not os.path.exists(report_dir):
            os.makedirs(report_dir)

        report = ReportGenerator(benchmark, correlation_matrix).generate(report_dir)
        report.to_csv(os.path.join(report_dir, 'report.csv'), index=False)

        # print(report)

        return report


if __name__ == '__main__':
    subj_id = 'giggle_1680253056260'
    Processor(subj_id).run(True)
