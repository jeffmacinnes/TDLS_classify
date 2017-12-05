"""
Script to retrieve the searchlight results (i.e. voxel accuraccies)
within a given mask. This operates on an individual subject basis
"""
import os
from os.path import join

from nilearn.input_data import NiftiMasker
import numpy as np
import json

dataDir = '../../data'
sl_radius = 5.0


def getSearchlightResults(classProb, subj, mask):
    """
    return the voxel accuracies from individual subject whole
    brain searchlight results for the classProb specified. Voxel
    results will be masked to only include voxels falling
    within the given mask
    """
    subjDir = join(dataDir, subj)
    sl_file = join(subjDir, 'searchlights', '{}_r{:.1f}_{}.nii.gz'.format(subj, sl_radius, classProb))
    mask_file = join(subjDir, 'masks', '{}_mask.nii.gz'.format(mask))

    # build a masker to load the sl data with the specified mask
    masker = NiftiMasker(mask_img=mask_file)

    # load the data with the masker
    sl_results = masker.fit_transform(sl_file)

    # convert to 1D
    sl_results = np.squeeze(sl_results)

    # remove any voxels that are equal to 0
    sl_results = sl_results[sl_results != 0]

    # convert to integer percent
    sl_results = [int(x*100) for x in sl_results]

    # Return a list of all voxel percentages
    return sl_results


classProbs = ['Category', 'Modality', 'Stimulus',
                'categoryWords', 'categoryPics',
                'stimulusWords', 'stimulusPics']
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']
masks = ['V1', 'V2', 'V3', 'V4']

allResults = {}
for c in classProbs:
    thisClassProb = {}      # dict to store all subjs results for this class prob
    for s in subjs:
        thisSubj = {}       # dict to store all masks results for this subj
        for m in masks:
            # get a list of voxel values (i.e. accuracies) for this
            # specific classProb/Subj/Mask combo
            results = getSearchlightResults(c,s,m)

            # write these results to the dict
            thisSubj[m] = results

            print('{} {} {} done'.format(c, s, m))

        # write all of mask results for this subj to the thisClassProb dict
        thisClassProb[s] = thisSubj

    # write all of the subjects results for this classProb to the alllResults dict
    allResults[c] = thisClassProb

outputFile = '../../analysis/sl_byVisArea/sl_allResults.json'

with open(outputFile, 'w') as fp:
    json.dump(allResults, fp, separators=(',', ':'), sort_keys=True, indent=4)
