"""
Preprocess the func data in prep for downstream analyses.
    - High pass Filter
    - motion correction
    - registration/normalization
"""
import os
from os.path import join
import sys

feat_template_dir = 'feat_templates'
data_dir = '../data'

def build_preproc_job(subj):
    """
    Modify the preprocessing template to fit this subject's data
    and save the copy. 
    Return the path to the modified feat .fsf file
    """

    subj_data_dir = join(data_dir, subj)

    # path to feat template
    template_path = join(feat_template_dir, 'preprocessing.fsf')

    #inputs


    # open the template file in 'read' mode, extract all text
    with open(template_path, 'r') as template_file:
        text = template_file.read()

    # make substitutions
    text = text.replace('SUB_', output_var)







# create list of subjects to iterate over
subjs = ['13034', '13035', '13036',
        '13038', '13039', '13040']

# loop over subjects
for s in subjs:
    processSubjRawBehave(s)
