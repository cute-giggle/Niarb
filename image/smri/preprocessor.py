# Author: cute-giggle@outlook.com


import os
import subprocess


def preprocess(subj_id: str, subj_dir: str, remove_unused: bool = False):
    
    """Default preprocess script for smri data."""

    preprocess_dir = os.path.join(subj_dir, 'preprocess')
    if not os.path.exists(preprocess_dir):
        os.mkdir(preprocess_dir)
    
    os.environ['SUBJECTS_DIR'] = preprocess_dir
    smri_path = os.path.join(subj_dir, 'smri.nii.gz')

    command = 'recon-all -parallel -s {} -i {} -all'.format(subj_id, smri_path)
    subprocess.call(command, shell=True)

    stat_dir = os.path.join(preprocess_dir, subj_id, 'stats')
    aseg_stat_path = os.path.join(stat_dir, 'aseg.stats')
    lh_aparc_stat_path = os.path.join(stat_dir, 'lh.aparc.stats')
    rh_aparc_stat_path = os.path.join(stat_dir, 'rh.aparc.stats')

    preprocess_result_dir = os.path.join(subj_dir, 'preprocess_result')
    if not os.path.exists(preprocess_result_dir):
        os.makedirs(preprocess_result_dir)
    command = 'cp {} {} {} {}'.format(aseg_stat_path, lh_aparc_stat_path, rh_aparc_stat_path, preprocess_result_dir)
    subprocess.call(command, shell=True)

    if remove_unused:
        os.system('rm -rf {}'.format(os.path.join(subj_dir, 'preprocess')))
