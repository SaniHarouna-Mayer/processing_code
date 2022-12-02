import numpy as np
import os
from glob import glob
import matplotlib.pyplot as plt

def load_data(fname):
    x0, x1 = np.loadtxt(fname).T
    return x0, x1

def save_data(fname, x0, x1, header=''):
    np.savetxt(fname, np.vstack((x0, x1,)).T, header=header, comments='#')
    return

##########
parent_dir = "/Users/admin/data/21_bt_2110_processed/"
data_dir = "cu3n_insitu_comm_140_max_1"

fnames = glob(os.path.join(parent_dir, data_dir, "*.chi"))
m = 30 # numer of datapoints to merge. array of size x will be averaged to an array of size x//m

avgdata_dir = os.path.join(parent_dir, data_dir) + "-avgby" + str(m)
if not os.path.isdir(avgdata_dir):
    os.mkdir(avgdata_dir)

for fname in fnames:
    x0, x1 = load_data(fname)
    l_i = len(x1)
    num_res = l_i % m
    l_f = int(np.ceil(l_i / m))
    if num_res != 0:
        x1_res_avg = x1[-1]
        x2_res_avg = np.mean(x2[-num_res:])
        for i in range(m - num_res):
            x1 = np.append(x1, x1_res_avg)
            x2 = np.append(x2, x2_res_avg)
    x0 = np.arange(l_f)
    x1 = np.mean(np.resize(x1, (l_f, m)), axis=1)
    x2 = np.mean(np.resize(x2, (l_f, m)), axis=1)
    save_data(os.path.join(dir_name, fname[:-4] + "_rdps.txt"), x0, x1)

