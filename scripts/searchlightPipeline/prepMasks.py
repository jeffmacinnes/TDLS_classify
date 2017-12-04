"""
Prep visual area masks.

- threshold the probabilistic masks
- binarize
- merge L & R
"""
import os
from os.path import join

maskDir = '../../data/MNI_masks'
thresh = 50       # probability to threshold probabilistic atlas at


for ROI in ['V1', 'V2', 'V3', 'V4']:
    for hemi in ['L', 'R']:

        ### create thresholded & binarized version of the orig mask
        # path to original mask
        origMask = join(maskDir, '{}_{}.nii.gz'.format(ROI, hemi))
        outputName = join(maskDir, '{}_thr{}_{}'.format(ROI, thresh, hemi))

        cmd_str = ' '.join(['fslmaths', origMask,
                        '-thr', str(thresh),
                        '-bin', outputName])
        os.system(cmd_str)

    ### Combine the threshed & binarized hemisphere masks into a single masks
    L_mask = join(maskDir, '{}_thr{}_L.nii.gz'.format(ROI, thresh))
    R_mask = join(maskDir, '{}_thr{}_R.nii.gz'.format(ROI, thresh))
    cmd_str = ' '.join(['fslmaths', L_mask,
                        '-add', R_mask,
                        '-bin',
                        join(maskDir, '{}_mask'.format(ROI))])
    os.system(cmd_str)


    ### Clean up the intermediate files
    os.remove(L_mask)
    os.remove(R_mask)
