"""
Cluster extent thresholding for whole brain searchlight images.

Find all of the clusters with a minumum extent of X voxels (where X is set below).
Write the output as a cluster mask img where every cluster is labeled according
to its index location. In addition, write out the full cluster table to disk.
"""
from __future__ import print_function

import os
from os.path import join
import subprocess

import numpy as np

clusterExtent = 4    # minimum number of voxels that must be in each cluster
slRadius = 5.0

dataDir = '../../data'

def mkClusters(subj, classProb):
    """
    find clusters for the searchlight image for this subj/classProb
    """
    subj_slDir = join(dataDir, subj, 'searchlights')
    subj_clusterDir = join(subj_slDir, 'clusters')
    if not os.path.isdir(subj_clusterDir):
        os.makedirs(subj_clusterDir)

    # setup paths
    sl_img = join(subj_slDir, '{}_r{:.1f}_{}.nii.gz'.format(subj, slRadius, classProb))
    clusterIdx_img = join(subj_clusterDir, '{}_{}_minExt{}.nii.gz'.format(subj, classProb, clusterExtent))
    cluster_fname = join(subj_clusterDir, '{}_{}_minExt{}.txt'.format(subj, classProb, clusterExtent))

    # figure out the accuracy ranges across the voxels in this searchlight
    accRange = subprocess.getoutput('fslstats {} -R'.format(sl_img))
    maxAcc = accRange.split(' ')[1]

    # set threshold based on a proportion of the max accuracy
    thresh = .6 * float(maxAcc)
    print(thresh)

    # setup command
    cmd_str = ' '.join(['cluster',
                        '-i', sl_img,
                        '-t', '{:.1f}'.format(thresh),
                        '--minextent={}'.format(clusterExtent),
                        '-o', clusterIdx_img,
                        '>', cluster_fname])
    print(cmd_str)
    os.system(cmd_str)

# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

classProbs = ['Modality', 'Category', 'Stimulus',
                'categoryPics', 'categoryWords',
                'stimulusPics', 'stimulusWords']

subjs = ['13034']
#classProbs = ['Modality']

for s in subjs:
    for c in classProbs:
        mkClusters(s,c)
