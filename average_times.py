import numpy as np
import os
from glob import glob
import matplotlib.pyplot as plt

def load_data(fname):
    x0, x1= np.loadtxt(fname).T
    return x0, x1

def save_data(fname, x0, x1, header=''):
    np.savetxt(fname, np.vstack((x0, x1)).T, header=header, comments='#')
    return

##########
parent_dir = "/Users/admin/data/21_bt_2110_processed/"
data_dir = "cu3n_insitu_comm_140_max_1"
# data_dir = "bg_bnnh2_insitu_syn_140_max_2"

dtype = ".chi"
fnames = glob(os.path.join(parent_dir, data_dir, "*" + dtype))
fnames.sort()

merge_num = 10
merge_sum = len(fnames) // merge_num

avgdata_dir = os.path.join(parent_dir, data_dir) + "-avgby" + str(merge_num)
if not os.path.isdir(avgdata_dir):
    os.mkdir(avgdata_dir)

for i_sum in range(merge_sum):
    x1s_notavg = []
    for i_num in range(merge_num):
        i = i_sum * merge_num + i_num
        x0, x1 = load_data(fnames[i])
        x1s_notavg.append(x1)
    x1_avg = np.mean(x1s_notavg, axis=0)
    save_name = os.path.join(avgdata_dir, os.path.basename(fnames[i_sum * merge_num]))
    save_name = save_name[:-len(dtype)] + "-avgby" + str(merge_num) + dtype
    save_data(save_name, x0, x1_avg)
# if len(fnames) % merge_num != 0:
#     x1s_notavg = []
#     i = merge_sum * merge_num
#     while i < len(fnames):
#         x0, x1 = load_data(fnames[i])
#         x1s_notavg.append(x1)
#         i += 1
#     x1_avg = np.mean(x1s_notavg, axis=0)
#     save_name = os.path.join(avgdata_dir, os.path.basename(fnames[i_sum * merge_num]))
#     save_name = save_name[:-len(dtype)] + "-avgby" + len(fnames) % merge_num + dtype
#     save_data(save_name, x0, x1_avg)

