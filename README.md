# usb_doc_extractor
A document extractor for USB drives
This program will poll the windows api returning a list of removable drives, it will crawl through the directories and files in the drive and filter them by extension. The remaining files will be copied to a directory in the user directory, the name of the directory is generated from the volume information of the drive.
