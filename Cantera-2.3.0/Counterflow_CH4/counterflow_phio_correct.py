"""
Zhen Lu 2018/05/06

correct the file name of the phio cases

"""

import glob
import os
from counterflow_file import *

#
phio = [0.04,0.1,0.2,0.4,0.6]

file_exts = ['.dat', '.xml', '.cema']

folder_params = {}
folder_params['phif'] = float('inf')
folder_params['phio'] = None

for phi in phio:
    folder_params['phio'] = phi
    folder_name = params2name(folder_params)
    os.chdir(folder_name)

    for file_ext in file_exts:
        for file_name in glob.glob('*{}'.format(file_ext)):
            params = name2params(file_name)
            params['phio'] = phi
            file_name_new = params2name(params)

            os.rename(file_name, file_name_new)

    os.chdir('..')
