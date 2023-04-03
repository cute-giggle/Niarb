# Author: cute-giggle@outlook.com


import os
import sys
import numpy as np
import subprocess


class DefaultPreprocessor:
    def __init__(self, subj_id: str, subj_dir: str, atlas_path: str):
        self.subj_id = subj_id
        self.subj_dir = subj_dir
        self.atlas_path = atlas_path
        self.shell_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'preprocess.sh')

    def remove_unused(self):
        preprocess_dir = os.path.join(self.subj_dir, 'preprocess')
        if os.path.exists(preprocess_dir):
            subprocess.run('rm -r {}'.format(preprocess_dir), shell=True)

    def run(self, remove_unused: bool = True):
        subprocess.run('sh {} {} {}'.format(self.shell_path, self.subj_dir, self.atlas_path), shell=True)
        if remove_unused:
            self.remove_unused()
