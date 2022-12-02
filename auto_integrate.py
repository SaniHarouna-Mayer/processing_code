import pyFAI
import fabio
import os
from time import sleep
from glob import glob
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

def integrate_ims_in_dir(path, dtype_im=".tif", dtype_int=".dat"):
    """
    Azimuthally integrate all images in directory <path> with ending <dtype_im>
    to patterns of ending <dtype_int> if not already integrated.
    :param 'str' path: path to directory where to apply the azimuthal integration
    :param 'str' dtype_im: data type/filename ending of image file
    :param 'str' dtype_int: data type/filename ending of pattern file
    """
    fnames_ims = glob(os.path.join(path, "*" + dtype_im))
    for fname_im in fnames_ims:
        im = fabio.open(fname_im).data
        fname_int = fname_im[:-len(dtype_im)] + dtype_int
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


patterns = ["*"]
ignore_patterns = None
ignore_directories = True
case_sensitive = True
go_recursively = False
my_event_handler = PatternMatchingEventHandler(patterns,
                                               ignore_patterns,
                                               ignore_directories,
                                               case_sensitive)
def integrate_on_created(event, dtype_im=".tif", dtype_int=".dat"):
    """
    Azimuthally integrate all created images in directory <path>
    with ending <dtype_im> to patterns of ending <dtype_int>.
    :param 'watchdog.events.FileCreatedEvent' event: watchdog object to check for created files
    :param 'str' dtype_im: data type/filename ending of image file
    :param 'str' dtype_int: data type/filename ending of pattern file
    """
    if event.src_path[-len(dtype_im):] == dtype_im:
        im = fabio.open(event.src_path).data
        ai.integrate1d(data=im,
                       npt=1000,
                       filename=event.src_path[:-len(dtype_im)] + dtype_int,
                       mask=mask,
                       polarization_factor=0.95,
                       unit="q_A^-1")
        print(f"integrate: {event.src_path}")
my_event_handler.on_created = integrate_on_created

if __name__ == "__main__":
    # define directories, filenames and initiate pyFAI object for azimuthal integration
    path = "/Users/admin/data/20_Pt_tf/watchdog_test"
    fname_poni = "/Users/admin/data/20_Pt_tf/alaci/poni_avg_phiscan.poni"
    fname_mask = "/Users/admin/data/20_Pt_tf/alaci/mask_20200413.edf" # empty string/None/False if no mask available
    ai = pyFAI.load(fname_poni)
    mask = fabio.open(fname_mask).data if fname_mask else None

    # integrate all images in directory if not already integrated
    integrate_ims_in_dir(path)

    # launch watchdog which integrates all new created images
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
