"""
Read the raw, exported behavioral files from ePrime. Grab the relevent bits
and write new formated behavioral files for each subject
"""
# python2/3 compatibility
from __future__ import print_function

import os
import sys
from os.path import join

import numpy as np
import pandas as pd

dataDir = '../data'
rawBehaveDir = join(dataDir, 'rawBehavioral')

def processSubjRawBehave(subj):
    """
    Open this subject's raw behavioral file, extract the
    relevant bits, and write a new file in their data dir
    """
    # read in the raw data file
    df = pd.read_table(join(rawBehaveDir, 'TDSL_2_0_{}.txt'.format(subj)),
                        encoding='utf-16',
                        header=1)

    # reduce the dataframe to the rows for the ToolDwelling blocks only
    TD_df = df[(df['Procedure[Block]'] == 'TDBlockWordProc')
                | (df['Procedure[Block]'] == 'TDBlockPictureProc')]

    # get the trial onsets. These come from different columns depending on the
    # task block
    word_onsets = TD_df['ToolDwellingWord.OnsetTime'].dropna()
    pic_onsets = TD_df['ToolDwellingPic.OnsetTime'].dropna()

    # word block always came before pic block. Concatenate onsets accordingly
    onsets = pd.concat([word_onsets, pic_onsets], ignore_index=True)

    # correct the onset times to sync with the scan vols time.
    # The first trial always occurred 2000ms after the start of the scan
    correctedOnsets = onsets - onsets.iloc[0] + 2000

    # reduce the dataframe to the relevant columns only, reset index
    TD_df = TD_df[['Category', 'Stimulus', 'Modality']].reset_index(drop=True)

    # The 'Modality' column will have NaNs for non-Picture rows. Correct this
    TD_df.Modality.fillna('Word', inplace=True)

    # Add the correctedOnsets to this reduced dataframe
    TD_df.loc[:, 'TrialOnset'] = correctedOnsets.values.astype(int)

    # Reorder the columns for cleanliness
    TD_df = TD_df[['TrialOnset', 'Modality', 'Category', 'Stimulus']]

    # Save the output
    outputFile = join(dataDir, subj, '{}_trialOnsets.txt'.format(subj))
    TD_df.to_csv(outputFile, index=False, sep='\t')

    print('Finished subject {}'.format(subj))


# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

# loop over subjects
for s in subjs:
    processSubjRawBehave(s)
