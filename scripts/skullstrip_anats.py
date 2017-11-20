"""
use FSL BET tool to skullstrip anat images
"""

# python2/3 compatibility
from __future__ import print_function

import os
import sys
from os.path import join
import subprocess

dataDir = '../data'
fractionalIntensity = 0.25


def skullstrip_anat(subj):

    # create the output directory if needed
    outputDir = join(dataDir, subj, 'masks')

    # setup input/output paths
    inputVol = join(dataDir, subj, (subj + '_MPRAGE'))
    outputName = '{}_brain'.format(inputVol)

    # submit the command
    cmd_str = ' '.join(['bet',
                    inputVol, outputName,
                    '-f', str(fractionalIntensity)])
    os.system(cmd_str)

    print('Subj {} completed...'.format(subj))

# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

for s in subjs:
    skullstrip_anat(s)
