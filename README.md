# Comfort-Study
This script was put together and modified to automate the NI Express DAQ collection process. For this experiement, we are using two NI USB-6341 connected to Grundfos temperature/flow sensors. NI Express projects have been set to convert the incoming voltages to their corresponding units of F and L/min. Logs are generated every 10 minutes and the collection script will only process the logs to a CSV file if they are older than 10 minutes. A secondary script will take the CSV and push them into our officeserver where another script will insert the data into a PostgreSQL table.


