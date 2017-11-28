"""
Make individual, single-col, regressors for every trial
"""

import os
from os.path import join

import pandas as pd
import numpy as np

dataDir = '../../data'

nVols = 500     # number of volumes per run

def mk_trialRegressors(subj):
    """
    Make trial regressors for this subject
    """

    # make output dir
    outputDir = join(dataDir, subj, 'timingFiles', 'trialRegressors')
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    # load this subjects trial onsets file
    trialOnsets = pd.read_table(join(dataDir, subj, (subj + '_trialOnsets.txt')),
                    sep='\t')

    # grab the trialOnsets column only
    onsets = trialOnsets.TrialOnset

    # loop over all trialOnsets
    for i,thisOnset in enumerate(onsets):

        trialNum = i+1     # so trial numbers start at 1

        # make a list of all of the OTHER onsets than the current one
        allOtherOnsets = [x for x in onsets if x != thisOnset]

        ### Make the regressor this this onset
        # create an empty regressor
        trialRegressor = np.zeros(nVols)

        # convert this onset to nearest volume index
        onsetIdx = int(np.round(thisOnset/1000))

        # set this vol to 1 in the regressor
        trialRegressor[onsetIdx] = 1

        # write the regressor
        outputFile = join(outputDir, 'trial_{:02}.txt'.format(trialNum))
        np.savetxt(outputFile, trialRegressor, fmt='%1.0u')

        ### Make the regressor for all OTHER onsets
        nuisRegressor = np.zeros(nVols)

        # loop over each of the OTHER onsets, add each to the nuisance regressor
        for nuisOnset in allOtherOnsets:
            idx = int(np.round(nuisOnset/1000))
            nuisRegressor[idx] = 1

        # write the nuisance regressor
        outputFile = join(outputDir, 'allBut_trial{:02}.txt'.format(trialNum))
        np.savetxt(outputFile, nuisRegressor, fmt='%1.0u')

# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

for s in subjs:
    mk_trialRegressors(s)
    print('subject {} trial regressors complete...'.format(s))
