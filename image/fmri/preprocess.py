# Author: cute-giggle@outlook.com


from typing import List
import glob
import os
import subprocess
import nibabel as nib


def modify_space(img: nib.Nifti1Image):

    img.header['qform_code'] = 1
    img.header['sform_code'] = 1


def get_default_rsfMRI_command(subj_id: str, dsets: List[str], copy_anat: str, out_dir: str, mni_template: str):

    """Get default command to generate shell for rsfMRI preprocessing using AFNI"""

    params = '-subj_id ' + subj_id + ' -dsets ' + ' '.join(dsets) + ' -copy_anat ' + copy_anat + ' -out_dir ' + out_dir
    params += ' -blocks despike tshift align tlrc volreg -tcat_remove_first_trs 2 -align_opts_aea -giant_move'
    params += ' -tlrc_base ' + mni_template + ' -tlrc_NL_warp -volreg_align_to MIN_OUTLIER -volreg_align_e2a -volreg_tlrc_warp'
    
    return 'afni_proc.py ' + params + '\n'


def rsfMRI_preprocess(subj_id: str, subj_dir: str, mni_template=None, remove_shell: bool = False, remove_unused: bool = False):

    """Preprocess rsfMRI using AFNI"""

    if mni_template is None:
        mni_template = 'MNI_avg152T1+tlrc'
        print('Using default MNI template: MNI_avg152T1+tlrc')

    dsets = glob.glob(os.path.join(subj_dir, 'fmri-r0[1-3].nii.gz'))
    copy_anat = os.path.join(subj_dir, 'smri.nii.gz')
    out_dir = os.path.join(subj_dir, 'preprocess')

    anat_img = nib.load(copy_anat)
    modify_space(anat_img)
    nib.save(anat_img, copy_anat)

    for dset in dsets:
        epi_img = nib.load(dset)
        modify_space(epi_img)
        nib.save(epi_img, dset)

    generate_shell_command = get_default_rsfMRI_command(subj_id, dsets, copy_anat, out_dir, mni_template)
    subprocess.call(generate_shell_command, shell=True)

    shell_path = os.path.abspath('proc.' + subj_id)
    subprocess.call('mv ' + shell_path + ' ' + subj_dir, shell=True)
    shell_path = os.path.join(subj_dir, 'proc.' + subj_id)
    subprocess.call(shell_path, shell=True)

    if remove_shell:
        os.system('rm ' + shell_path)

    result_save_dir = os.path.join(subj_dir, 'preprocess_result')
    if not os.path.exists(result_save_dir):
        os.mkdir(result_save_dir)

    target_sMRI_path = os.path.join(out_dir, 'anat_final.' + subj_id + '+tlrc')
    result_sMRI_path = os.path.join(result_save_dir, 'smri.nii.gz')
    subprocess.call('3dAFNItoNIFTI -prefix ' + result_sMRI_path + ' ' + target_sMRI_path, shell=True)

    target_fMRI_names = [os.path.basename(name) for name in glob.glob(os.path.join(out_dir, '*.volreg+tlrc.HEAD'))]
    for target_fMRI_name in target_fMRI_names:
        target_fMRI_path = os.path.join(out_dir, target_fMRI_name)
        result_fMRI_path = os.path.join(result_save_dir, 'fmri-' + target_fMRI_name.split('.')[2] + '.nii.gz')
        subprocess.call('3dAFNItoNIFTI -prefix ' + result_fMRI_path + ' ' + target_fMRI_path, shell=True)

    if remove_unused:
        os.system('rm -r ' + out_dir)
