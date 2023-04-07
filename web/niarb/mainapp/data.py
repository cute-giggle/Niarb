# Author: cute-giggle@outlook.com


import os
import json
import numpy as np


BENCHMARK_DIR = os.path.join(os.path.dirname(__file__), '../../../data/benchmark')
FSAVERAGE_DIR = os.path.join(os.path.dirname(__file__), '../../../data/fsaverage')


class IndicatorGuide:
    def __init__(self):
        smri_guide_path = os.path.join(BENCHMARK_DIR, 'smri/guide.json')
        with open(smri_guide_path, 'r') as f:
            self.smri_guide = json.load(f)
        fmri_guide_path = os.path.join(BENCHMARK_DIR, 'fmri/guide.json')
        with open(fmri_guide_path, 'r') as f:
            self.fmri_guide = json.load(f)
        dmri_guide_path = os.path.join(BENCHMARK_DIR, 'dmri/guide.json')
        with open(dmri_guide_path, 'r') as f:
            self.dmri_guide = json.load(f)

    def get_guide(self, category):
        if category == 'smri':
            return self.smri_guide
        elif category == 'fmri':
            return self.fmri_guide
        elif category == 'dmri':
            return self.dmri_guide
        else:
            return None
        
    def get_indicator_guide(self, category, indicator, conclusion):
        guide = self.get_guide(category)
        if guide and indicator in guide and conclusion in guide[indicator]:
            return guide[indicator][conclusion]
        return None


class FsaverageMesh:
    def __init__(self, mesh_name: str='pial.mesh'):

        if mesh_name not in ['orig.mesh', 'pial.mesh', 'white.mesh', 'inflated.mesh']:
            raise Exception('Mesh name not supported: {}'.format(mesh_name))
        
        self.mesh_path = os.path.join(FSAVERAGE_DIR, 'surface', mesh_name)
        if not os.path.exists(self.mesh_path):
            raise Exception('Mesh file not found: {}'.format(self.mesh_path))
        
        with open(self.mesh_path, 'rb') as f:
            vertex_count = np.fromfile(f, dtype=np.int32, count=1)[0]
            self.vertices = np.fromfile(f, dtype=np.float32, count=vertex_count*3)
            face_count = np.fromfile(f, dtype=np.int32, count=1)[0]
            self.faces = np.fromfile(f, dtype=np.int32, count=face_count*3).tolist()

        # normalize vertices
        self.vertices = self.vertices.reshape(-1, 3)
        self.vertices = self.vertices - self.vertices.mean(axis=0)
        self.vertices = self.vertices / np.linalg.norm(self.vertices, axis=1).max()
        self.vertices = self.vertices.reshape(-1).tolist()

    def get_data(self):
        return {
            'vertices': self.vertices,
            'faces': self.faces
        }
    

class FsaverageAnnot:
    def __init__(self, annot_name: str='shaefer-200-17.annot'):

        if annot_name not in ['aparc.annot', 'brodmann.annot', 'shaefer-200-17.annot']:
            raise Exception('Annot name not supported: {}'.format(annot_name))
        
        self.annot_path = os.path.join(FSAVERAGE_DIR, 'annotation', annot_name)
        if not os.path.exists(self.annot_path):
            raise Exception('Annot file not found: {}'.format(self.annot_path))
        
        with open(self.annot_path, 'rb') as f:
            color_count = np.fromfile(f, dtype=np.int32, count=1)[0]
            self.color_table = []
            for i in range(color_count):
                color = np.fromfile(f, dtype=np.int32, count=4).tolist()
                name_length = np.fromfile(f, dtype=np.int32, count=1)[0]
                name = f.read(name_length).decode('utf-8')
                self.color_table.append([color, name])
            label_count = np.fromfile(f, dtype=np.int32, count=1)[0]
            self.label = np.fromfile(f, dtype=np.int32, count=label_count).tolist()

    def get_data(self):
        return {
            'color_table': self.color_table,
            'label': self.label
        }


indicator_guide = IndicatorGuide()
