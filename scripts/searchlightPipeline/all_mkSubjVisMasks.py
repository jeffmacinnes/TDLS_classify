"""
Take the MNI visual area masks (V1, V2, etc..) and transform them
down to subject functional space for each subject using the
standard2example_func.mat transformation matrix found in each
subject's preprocessing folder
"""

import os
from os.path import join


dataDir = '../../data'
#visAreas = ['V1', 'V2', 'V3', 'V4']
areas = ['V1', 'V2', 'V3', 'V4', 'PMC', 'PPA']

def makeSubjMasks(subj):
    """
    convert all of the vis masks for this subject
    """
    subjDir = join(dataDir, subj)
    outputDir = join(subjDir, 'masks')
    if not os.path.isdir(outputDir):
        os.makedirs(outputDir)

    refVol = join(subjDir, 'preprocessed.feat/mean_func.nii.gz')
    xfm_mat = join(subjDir, 'preprocessed.feat/reg/standard2example_func.mat')

    # loop over all masks
    for v in areas:
        inputMask = join(dataDir, 'MNI_masks', '{}_mask.nii.gz'.format(v))
        outputVol = join(outputDir, '{}_mask'.format(v))
        outputVolpath = outputVol + '.nii.gz'
        print(v, outputVolpath)

        if os.path.isfile(outputVolpath):
            pass
        else: 
            # run the command to apply the transformation
            cmd_str = ' '.join(['flirt',
                                '-in', inputMask,
                                '-ref', refVol,
                                '-applyxfm', '-init', xfm_mat,
                                '-out', outputVol])
            os.system(cmd_str)

            # binarize the output image
            cmd_str = ' '.join(['fslmaths', outputVol,
                            '-bin', outputVol])
            os.system(cmd_str)

            print('made {} mask for subj {}'.format(v, subj))


subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']
for s in subjs:
    makeSubjMasks(s)
