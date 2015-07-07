import NISignalExpressUtility
import os
import time
import datetime
import shutil
import csv
from GrundfosUtility import convert_output
from DataFiles import __data__
from ConvertedCSVs import __converted__
from ReshapedCSVs import __reshaped__
from CalibratedCSVs import __calibrated__
from Output import __output__
from NISignalExpressUtility import separatefiles
from NISignalExpressUtility import network_share_auth
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
    separatefiles()
    for files in os.listdir(converted_location):
        if ".csv" in files:
            os.remove(os.path.join(converted_location, files))   
            
    for files in os.listdir(reshaped_location):
        if ".csv" in files:
            os.remove(os.path.join(reshaped_location, files))  

    for files in os.listdir(calibrated_location):
        if ".csv" in files:
            os.remove(os.path.join(calibrated_location, files))    
    time.sleep(600)
                    
                    
'''      
            archived = False
            with open('archive.csv','rb') as archivefile:
                #print "archive file opened"
                archivereader = csv.reader(archivefile)
                #print "here"
                
                for archiveditem in archivereader:
                    #print folder_name
                    print archiveditem
                    if folder_name is archiveditem:
                        
                    #if item has not yet been archived
                        archived = True
            #print archived
            if not archived:
                #print "not archived"
                with open('archive.csv', 'wb') as archivefile:
                    #add item to archived list
                    archivewriter = csv.writer(archivefile)
                    archivewriter.writerow(list(folder_name))
                #for data_folders in data_folders_locations:
                create_time = os.path.getctime(os.path.abspath(data_folders_locations))
                if current_epoch - 3600 > create_time:
                    NIExtract = NISignalExpressUtility.NISignalExpressUtility(\
                        data_folders_locations, converted_location,\
                        reshaped_location, calibrated_location)
                    NIExtract.convert_to_csv()
                    NIExtract.reshape_csv()
                    NIExtract.calibrate_output()
                            
                                #archive converted files
                                #shutil.move(os.path.abspath(data_folders), archive_location)
        separatefiles()
''' 
  


#    flowDir = os.path.join(os.path.dirname(os.path.abspath(__file__)),  "ADASEED", "CalibratedFlow")
#    print "flowdir" 
#    print flowDir
#    flowFiles = os.listdir(flowDir)
#    tempDir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ADASEED", "CalibratedTemperature")
#    tempFilesDir = os.listdir(os.path.join(os.path.dirname(__file__), "CalibratedTemperature"))
    #serverFlowDir = "P:\1.Projects\1.17.RadiantPanels\CalibratedFlow"
    #serverTempDir = "P:\1.Projects\1.17.RadiantPanels\CalibratedTemperature"
    
'''
    with network_share_auth(r"\\CSBCD\smb-share", "steve", ""):
        for fileName in flowFiles:
            if ".csv" in fileName:         
                flowFilePath = os.path.join(flowDir, fileName)
                print "flow file path"
                print flowFilePath
                shutil.copyfile(os.path.abspath(flowFilePath), r"P:\1.Projects\1.17.RadiantPanels\CalibratedFlow")
        for fileName in tempFilesDir:
            if ".csv" in fileName:
                tempFilePath = os.path.join(tempDir, fileName)
                shutil.copyfile(tempFilePath, r"P:\1.Projects\1.17.RadiantPanels\CalibratedTemperature")
'''
    #time.sleep(3600)

#Enable only if the the collected data is from Grundfos VFS 1-20 sensor
#convert_output(calibrated_location, output_location)
