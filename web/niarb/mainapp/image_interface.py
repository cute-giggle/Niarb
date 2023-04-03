# Author: cute-giggle@outlook.com


import os
import sys
import argparse


WORKING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../data/working')


def prepare_env():
    image_pkg_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../..')
    if image_pkg_dir not in sys.path:
        sys.path.append(image_pkg_dir)


def smri_process(subj_id: str):
    prepare_env()
    from image.smri.processor import Processor
    try:
        processor = Processor(subj_id)
        processor.run()
    except Exception as e:
        print(e)
    
    subj_dir = os.path.join(WORKING_DIR, 'smri/subjects', subj_id)
    with open(os.path.join(subj_dir, 'completed.txt'), 'w') as f:
        f.write('completed!')


def fmri_process(subj_id: str):
    prepare_env()
    from image.fmri.processor import Processor
    try:
        processor = Processor(subj_id)
        processor.run()
    except Exception as e:
        print(e)

    subj_dir = os.path.join(WORKING_DIR, 'fmri/subjects', subj_id)
    with open(os.path.join(subj_dir, 'completed.txt'), 'w') as f:
        f.write('completed!')


def dmri_process(subj_id: str):
    prepare_env()
    from image.dmri.processor import Processor
    try:
        processor = Processor(subj_id)
        processor.run()
    except Exception as e:
        print(e)

    subj_dir = os.path.join(WORKING_DIR, 'dmri/subjects', subj_id)
    with open(os.path.join(subj_dir, 'completed.txt'), 'w') as f:
        f.write('completed!')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--subj_id', type=str, required=True)
    parser.add_argument('--category', type=str, required=True)
    args = parser.parse_args()

    if args.category == 'smri':
        smri_process(args.subj_id)
    elif args.category == 'fmri':
        fmri_process(args.subj_id)
    elif args.category == 'dmri':
        dmri_process(args.subj_id)
    else:
        print('Invalid category!')


if __name__ == '__main__':
    main()
