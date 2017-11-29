"""
After running all of the single trial models for each subject, this script
will grab all of the single trial betas (e.g. trial#_pe.nii.gz) and concatenate
them into a single 4D nifti
"""

import os
from os.path import join
import sys

# figure out abs path to the TDLS_classify folder
thisDir = os.path.dirname(os.path.abspath(__file__))
pathParts = thisDir.split(os.sep)
EXP_DIR = os.sep.join(pathParts[:-2])

dataDir = join(EXP_DIR, 'data')

def concatenateSingleTrialBetas(subj):
    """
    Grab all of these subjects single trial parameter estimate nifitis and
    concatenate them across the 4th dimension. Save the 4D file in the subject dir
    """

    # path to subjects dir
    subj_dataDir = join(dataDir, subj, 'singleTrialGLM')

    # make a list of all single trial files
    singleTrial_PEs = [join(subj_dataDir, ('trial{:02}_pe.nii.gz'.format(x))) for x in range(1,49)]

    # start fsl commands as list
    fslOpts = ['fslmerge', '-t', join(subj_dataDir, 'singleTrialPEs')]

    # concatenate the two lists
    cmd_str = ' '.join(fslOpts + singleTrial_PEs)

    # run the command
    os.system(cmd_str)

    print('subject {} completed'.format(subj))

# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

for s in subjs:
    concatenateSingleTrialBetas(s)
