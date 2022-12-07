import pyFAI
import fabio
import os
from glob import glob

def integrate_ims_in_dir(path, dtype_im=".tif", dtype_int=".dat"):
    """
    Azimuthally integrate all images in directory <path> with ending <dtype_im>
    to patterns of ending <dtype_int> if not already integrated.
    :param 'str' path: path to directory where to apply the azimuthal integration
    :param 'str' dtype_im: data type/filename ending of image file
    :param 'str' dtype_int: data type/filename ending of pattern file
    """
    dirs = []
    for dir in glob("/Volumes/LARSABI/P07-2022-1202/sanisanisanisani/*/"):
        dirs.append(dir)
    fnames_ims = []
    for fnames_ims_indir in dirs:
        for fname in glob(os.path.join(fnames_ims_indir, "*" + dtype_im)):
            fnames_ims.append(fname)
    # print(fnames_ims)
    # fnames_ims = glob(os.path.join(path, "*" + dtype_im))
    for fname_im in fnames_ims:
        im = fabio.open(fname_im).data
        fname_int = fname_im[:-len(dtype_im)] + dtype_int
        fname_int = os.path.join(path, os.path.basename(fname_int))
        if os.path.isfile(fname_int):
            print(f"already integrated: {fname_im}")
            continue
        else:
            ai.integrate1d(data=im,
                           npt=1000,
                           filename=fname_int,
                           mask=mask,
                           polarization_factor=0.95,
                           unit="q_A^-1")
            print(f"integrate: {fname_im}")

if __name__ == "__main__":
    # define directories, filenames and initiate pyFAI object for azimuthal integration
    path = "/Volumes/LARSABI/P07-2022-1202/sanisanisanisani"
    fname_poni = "/Volumes/LARSABI/P07-2022-1202/sanisanisanisani/dd_cap6_kcap.poni"
    fname_mask = "/Volumes/LARSABI/P07-2022-1202/sanisanisanisani/sh_cu3pdn_insitu_bkg_1_00001-00mean_120_files-mask.edf" # empty string/None/False if no mask available
    ai = pyFAI.load(fname_poni)
    mask = fabio.open(fname_mask).data if fname_mask else None

    # integrate all images in directory if not already integrated
    integrate_ims_in_dir(path)
