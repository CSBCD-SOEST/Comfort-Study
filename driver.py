import NISignalExpressUtility
import os
import time
import datetime
#import shutil
import csv
#from GrundfosUtility import convert_output
from DataFiles import __data__
from ConvertedCSVs import __converted__
from ReshapedCSVs import __reshaped__
from CalibratedCSVs import __calibrated__
from Output import __output__
from NISignalExpressUtility import separatefiles
#from NISignalExpressUtility import network_share_auth
data_location = os.path.dirname(os.path.abspath(__data__.__file__)) #DataFile
converted_location = os.path.dirname(os.path.abspath(__converted__.__file__))
reshaped_location = os.path.dirname(os.path.abspath(__reshaped__.__file__))
calibrated_location = os.path.dirname(os.path.abspath(__calibrated__.__file__))
output_location = os.path.dirname(os.path.abspath(__output__.__file__))
archive_location = os.path.join(os.path.dirname(__file__), 'archive')

print "data: ", data_location
print "converted: ", converted_location
print "reshaped: ", reshaped_location
print "calibrated: ", calibrated_location
print "output: ", output_location

pattern = '%d.%m.%Y %H:%M:%S'


#if in archive, ignore it
#if not in archive, add it to archive and process it


while 1:
    #check that file was created an hour ago
    now = datetime.datetime.now().strftime(pattern)
    current_epoch = int(time.mktime(time.strptime(now, pattern)))
    
    data_folders_locations = [] 
    #get folders in DataFiles folder
    for folder_name in os.listdir(data_location):
        if ".py" not in folder_name:
            archived = False
            with open('archive.csv', 'rb') as archivefile:
                archivereader = csv.reader(archivefile)
                for archiveditem in archivereader:
                    try:
                        if folder_name == archiveditem[0]:
                            archived = True
                    except:
                        print "Error: Blank archive file"
            if not archived:
                try:
#                    print os.listdir(os.path.join(data_location, folder_name))[0]
                    tdms_path = os.path.join(data_location, folder_name, os.listdir(os.path.join(data_location, folder_name))[0])
#                    print tdms_path                    
                    create_time = os.path.getctime(tdms_path)
#                    print create_time
                    
                #create_time = os.path.getctime(os.path.abspath(folder_name))
                #create_time = os.stat(os.path.abspath(folder_name)).st_mtime
                    if current_epoch - 600 > create_time:
                        with open('archive.csv', 'a') as archivefile:
                            archivewriter = csv.writer(archivefile)
                            archivewriter.writerow([folder_name])
                        NIExtract = NISignalExpressUtility.NISignalExpressUtility(\
                            os.path.join(data_location, folder_name), converted_location,\
                            reshaped_location, calibrated_location)
                        print "Extracted " + folder_name
                        NIExtract.convert_to_csv()
                        print "Converted " + folder_name
                        NIExtract.reshape_csv()
                        print "Reshaped " + folder_name
                        NIExtract.calibrate_output()
                        print "Calibrated " + folder_name
                except Exception as e:
#                    print e
                    print "File " + folder_name + " not ready for processing"
    #move into ADASEED folder
    #can be configured for different output folders
    separatefiles()
    #clear temporary files
    for files in os.listdir(converted_location):
        if ".csv" in files:
            os.remove(os.path.join(converted_location, files))   
            
    for files in os.listdir(reshaped_location):
        if ".csv" in files:
            os.remove(os.path.join(reshaped_location, files))  

    for files in os.listdir(calibrated_location):
        if ".csv" in files:
            os.remove(os.path.join(calibrated_location, files)) 
    #sleep for 10 minutes
    time.sleep(600)
