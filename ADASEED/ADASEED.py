#!/usr/bin/env python
'''
This script is designed to gather data and input them into a PostgreSQL
database.

9/18/2014: Modified to be re-purposed for Kuykenall data collection. Only 
           Hoboware will be used in this project. EGauge components will be
           disabled from the script.
           
           Outputs for this script will be modified to talk to the server API.
           It will push all reshaped data files up into the server, where
           another script will handle shifting the data into the database.
'''
import datetime
import time
from Hobowarebin import HobowareUtility
import os
import xmlrpclib

__author__ = "Christian A. Damo"
__copyright__ = "Copyright 2014 School of Architecture, University of Hawaii at Manoa"
__credits__ = ["Christian A. Damo", "Reed Shinsato"]
__version__ = "0.01"
__maintainer__ = "Eileen Peppard"
__email__ = "epeppard@hawaii.edu"
__status__ = "Prototype"

key = ""

def push_temperature():
    temp_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CalibratedTemperature")
    server = xmlrpclib.ServerProxy("")	
	#if there ARE files to process, then for each file do the following
    for files in os.listdir(temp_dir):
        with open(os.path.join(temp_dir, files), "rb") as handle:
            binary_data = xmlrpclib.Binary(handle.read())
        server.radiantpaneltemperature_push(binary_data, os.path.split(files)[1], key)
        os.remove(os.path.join(temp_dir, files))
    
def push_flow():
    flow_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "CalibratedFlow")
    server = xmlrpclib.ServerProxy("")	
	#if there ARE files to process, then for each file do the following
    for files in os.listdir(flow_dir):
        with open(os.path.join(flow_dir, files), "rb") as handle:
            binary_data = xmlrpclib.Binary(handle.read())
        server.radiantpanelflow_push(binary_data, os.path.split(files)[1], key)
        os.remove(os.path.join(flow_dir, files))

def process_hobo_files():
    	'''
	given:  nothing
	return: nothing, but carries out the entire processing of the hobo files
	        when they are saved to the ADASEED>hobo folder. Reshapes the raw 
             file to a csv, then edits the output by reshaping to eshape and
             finally inserting it into the database.
    	'''
     
     #connect to the API
	server = xmlrpclib.ServerProxy("")
	#get the files in the ADASEED>hobo directory
	hobo_files = hobo.get_hobo_files()
	#if there's no files to process, tell the user there isn't any and end the function
	if len(hobo_files) == 0:
		print "At "+str(datetime.datetime.now())+" there were no data collected from the Hobo Network\n"
		return 0
	#if there ARE files to process, then for each file do the following
	for hobo_file in hobo_files:
		#inform the user you're processing a particular file
		print 'processing '+hobo_file
		#extract the data from the raw hobo shaped file
		output_filename = hobo.extract_data(hobo_file)
		#edit the file to do something, look at the HoboUtility comments
		output_filename = hobo.edit_output(output_filename)
		#once the file is in an eshape go ahead and push it up to the server
		with open(output_filename, "rb") as handle:
			binary_data = xmlrpclib.Binary(handle.read())
		server.kuykendall_push(binary_data, os.path.split(output_filename)[1]\
                                 , key)
		#delete all the hobo meta files
		hobo.clean_folder()

try:
	#display greeting
	print ''
	print '                  *****    Welcome to the    *****'
	print '"Automatic Data Acquisition System for Energy and Environmental Data"'
	print '                             (ADASEED)\n'

	#instance Classes
	hobo = HobowareUtility.HobowareUtility()

	#check for directories used by this script
	if not os.path.exists('hobo'):
     	#generate the hobo folder if it doesnt exist
		os.makedirs('hobo')
  
	if not os.path.exists('extracted'):
		os.makedirs('extracted')
  
	if not os.path.exists('edited'):
		os.makedirs('edited')
      
	if not os.path.exists('archive\hobo'):
     	#generate the archieve folder if it doesn't exist
		os.makedirs('archive\hobo')

	#wait for the user so that they can make sure everything is in working order
	raw_input('Press Enter to start "ADASEED"...')
	
	#get time now and store as 'from' time for use in the "except" block.
	old_time = datetime.datetime.now()
	from_str = str(old_time)[:-9]+'00'

	#let the user know that we're starting the session
	print 'Your session has started at '+from_str
	print 'Hit control-c to end session'

	#start looping
	while 1:
		#wait every 2 hours
		time.sleep(600)

		push_temperature()
		push_flow()


except KeyboardInterrupt:
	#this block of code basically carries out the same sequence of commands
	#in the while loop above
	#let the user know wer're finishing up
	print 'Ending the "Automatic Data Acquisition System for Energy and Environmental Data"\n'
	#process any hobo files
	push_temperature()

	push_flow()
	#let the user manually end the program so that they can read
	#any outputs that were created.
	raw_input('Press Enter to quit "ADASEED"...')
		
	
