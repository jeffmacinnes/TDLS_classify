"""
Covert raw scans from the PAR/REC files ../RRF13/Scans directory
into nii.gz files and store in the local data dir
"""
# python2/3 compatibility
from __future__ import print_function

import subprocess
import os
from os.path import join
import sys
import glob


def convertFile(input_fname, output_fname):
    """
    convert the specified input file to a compressed nifti with the
    specified output name
    """
    output_dir, output_prefix = os.path.split(output_fname)

    cmd_str = ' '.join(['dcm2niix',
                    '-z y',
                    '-f {}'.format(output_prefix),
                    '-o {}'.format(output_dir),
                    input_fname])

    print(cmd_str)
    os.system(cmd_str)
    print('Converted {}'.format(output_prefix))

expDir = '/projects/RRF13'
analysisDir = join(expDir, 'TDLS_classify')

# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

# loop over subjects
for s in subjs:
    rawScanDir = join(expDir, 'Scans', s)

    # build the output dir for this subject if necessary
    outputDir = join(analysisDir, 'data', s)
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    # get a list of all scans in this dir
    rawScans = os.listdir(rawScanDir)

    # look for, and then convert, specific scans
    scanRuns = ['MPRAGE', 'Run1', 'Run2', 'Run3', 'Run4', 'TDSL1', 'TDSL2']
    for run in scanRuns:

        # try to find this run for this subj
        scanFile = glob.glob(join(rawScanDir, '*{}*.PAR'.format(run)))

        if not scanFile:
            print('Could not find {} run for subj {}'.format(run, s))
        else:
            # build the output name for the converted file
            output_fname = join(outputDir,'{}_{}'.format(s, run))

            # convert the file
            convertFile(scanFile[0], output_fname)
