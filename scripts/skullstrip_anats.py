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


def skullstrip_anat(subj,centerCoord):
    """
    Skull strip the anatomical image for this subj. Use the center
    Coord option in BET to help remove neck
    """

    # create the output directory if needed
    outputDir = join(dataDir, subj, 'masks')

    # setup input/output paths
    inputVol = join(dataDir, subj, (subj + '_MPRAGE'))
    outputName = '{}_brain'.format(inputVol)

    # submit the command
    cmd_str = ' '.join(['bet',
                    inputVol, outputName,
                    '-f', str(fractionalIntensity),
                    '-c', ' '.join([str(x) for x in centerCoord])
                    ])
    print(cmd_str)
    os.system(cmd_str)

    print('Subj {} completed...'.format(subj))

# create list of subjects, along with the coords to the (appx) center of the brain
subjs = {'13034':[140,141,87],
        '13035':[137,166,85],
        '13036':[149,154,90],
        '13038':[146,148,88],
        '13039':[138,147,88],
         '13040':[143,154,88]
         }

for s in subjs.keys():
    centerCoord = subjs[s]
    skullstrip_anat(s, centerCoord)
