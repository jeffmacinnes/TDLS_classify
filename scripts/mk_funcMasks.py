"""
use FSL BET tool to create a brain-mask for functional data from each subject
"""
# python2/3 compatibility
from __future__ import print_function

import os
import sys
from os.path import join
import subprocess

dataDir = '../data'
fractionalIntensity = 0.4


def mk_func_mask(subj):
    # create the output directory if needed
    outputDir = join(dataDir, subj, 'masks')
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    # setup input/output paths
    inputVol = join(dataDir, subj, (subj + '_TDSL2'))
    outputName = join(outputDir, 'TDSL2_brain')  # will have '_mask' appended

    # submit the command
    cmd_str = ' '.join(['bet',
                    inputVol, outputName,
                    '-f', str(fractionalIntensity),
                    '-n', '-m'])
    os.system(cmd_str)

    print('Subj {} completed...'.format(subj))

# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

for s in subjs:
    mk_func_mask(s)
