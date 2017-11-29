"""
Submit all of the single trial models for each subject
"""

import os
import shutil
from os.path import join
import sys

feat_template_dir = 'feat_templates'

# figure out abs path to the TDLS_classify folder
thisDir = os.path.dirname(os.path.abspath(__file__))
pathParts = thisDir.split(os.sep)
EXP_DIR = os.sep.join(pathParts[:-2])

data_dir = join(EXP_DIR, 'data')

def submitModel(subj, trialNum):
    """
    modify the single trial GLM template for this
    subject/trial combo, and submit
    """

    # path to feat template
    template_path = join(feat_template_dir, 'singleTrialGLM.fsf')

    # open the template file in 'read' mode, extract all text
    with open(template_path, 'r') as template_file:
        text = template_file.read()

    # set up input vars
    tmp_outputDir = join(data_dir, subj, 'singleTrialGLM', ('tmp_trial{:02}'.format(trialNum)))
    inputFile = join(data_dir, subj, 'preprocessed.feat/filtered_func_data.nii.gz')
    trialEV = join(data_dir, subj, 'timingFiles/trialRegressors', 'trial_{:02}.txt'.format(trialNum))
    nuisEV = join(data_dir, subj, 'timingFiles/trialRegressors', 'allBut_trial{:02}.txt'.format(trialNum))

    # make substitutions
    text = text.replace('SUB_OUTPUTDIR_SUB', tmp_outputDir)
    text = text.replace('SUB_INPUTFILE_SUB', inputFile)
    text = text.replace('SUB_TRIALEV_SUB', trialEV)
    text = text.replace('SUB_NUISEV_SUB', nuisEV)

    # write the temporary template file
    subj_design_fsf = join(feat_template_dir, 'tmp_design.fsf')
    with open(subj_design_fsf, 'w') as design_fsf:
        design_fsf.write(text)

    # submit the command
    cmd_str = 'feat ' + subj_design_fsf
    os.system(cmd_str)

    ### copy the important files
    src_PE = join((tmp_outputDir + '.feat'), 'stats/pe1.nii.gz')
    dst_PE = join(data_dir, subj, 'singleTrialGLM', 'trial{:02}_pe.nii.gz'.format(trialNum))
    shutil.copy(src_PE, dst_PE)

    src_design = join((tmp_outputDir + '.feat'), 'design.fsf')
    dst_design = join(data_dir, subj, 'singleTrialGLM', 'trial{:02}_design.fsf'.format(trialNum))
    shutil.copy(src_design, dst_design)

    ### remove the original output dir
    shutil.rmtree((tmp_outputDir + '.feat'))

    print('subject {} trial {} complete...'.format(subj, trialNum))



def submit_subj(subj):
    # submit model for each trial

    # setup output dir, delete the existing one if found
    subjOutputDir = join(data_dir, subj, 'singleTrialGLM')
    if os.path.isdir(subjOutputDir):
        shutil.rmtree(subjOutputDir)
    os.makedirs(subjOutputDir)

    # loop over all trials
    for trialNum in range(1, 49):
        submitModel(subj, trialNum)

    # combine all outputs into single image, delete the rest to save space



# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

for s in subjs:
    submit_subj(s)
