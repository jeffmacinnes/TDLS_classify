"""
Preprocess the func data in prep for downstream analyses.
    - High pass Filter
    - motion correction
    - registration/normalization
"""
import os
from os.path import join
import sys

feat_template_dir = 'feat_templates'

# figure out abs path to the TDLS_classify folder
thisDir = os.path.dirname(os.path.abspath(__file__))
pathParts = thisDir.split(os.sep)
EXP_DIR = os.sep.join(pathParts[:-2])

data_dir = join(EXP_DIR, 'data')

def preproc_job(subj):
    """
    Modify the preprocessing template to fit this subject's data
    and save the copy.
    Return the path to the modified feat .fsf file
    """

    subj_data_dir = join(data_dir, subj)

    # path to feat template
    template_path = join(feat_template_dir, 'preprocessing.fsf')

    # input vars
    outputDir = join(subj_data_dir, 'preprocessed')
    inputFile = join(subj_data_dir, (subj + '_TDSL2.nii.gz'))
    anatFile = join(subj_data_dir, (subj + '_MPRAGE_brain.nii.gz'))

    # open the template file in 'read' mode, extract all text
    with open(template_path, 'r') as template_file:
        text = template_file.read()

    # make substitutions
    text = text.replace('SUB_OUTPUTDIR_SUB', outputDir)
    text = text.replace('SUB_INPUTFILE_SUB', inputFile)
    text = text.replace('SUB_ANAT_SUB', anatFile)

    # write the temporary template file
    subj_preproc_fsf = join(feat_template_dir, 'tmp_preprocessing.fsf')
    with open(subj_preproc_fsf, 'w') as preproc_design:
        preproc_design.write(text)

    # submit the command
    cmd_str = 'feat ' + subj_preproc_fsf
    os.system(cmd_str)



# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']
subjs = ['13034']

# loop over subjects
for s in subjs:
    preproc_job(s)

    print('subj {} preprocessing complete'.format(s))


# delete tmp_preprocessing
os.remove(join(feat_template_dir, 'tmp_preprocessing.fsf'))
