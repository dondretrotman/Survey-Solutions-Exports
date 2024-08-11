# Title: LFS data downloader
# Description: This uses the Survey Solutions API to generate a Data package, download and extract it
# Version: 5.2
# Date: 2024-08-09
# Author: Dondre Trotman
# Notes: This script assumes that you have 7zip installed and set as a path (so that it can be called withtout stating the path)
#        It also assumes that you have the SSAW, pandas and openpyxl modules installed. Run the following in a command prompt if they are is not: pip install SSAW pandas openpyxl
#        the pydantic module should be version 1.9.0 (pip install --force-reinstall "pydantic==1.9.0")
#        It also requires a directory named "Weekly Updates" to export the completed files to.
#        Run "runpy.bat" to run the script (not included)
#Changelog: 
#1.0 - Initial release. Grabs the data and extracts it
#2.0 - Prints all output to file as well as the screen, including 7zip
#3.0 - Modified for LFS
#4.0 - Made it export a finished, dated txt file with all data
#4.1 - Changed questionnaire status to "ALL", Changed filename variables to accomodate different questionnaire statuses
#5.0 - Exports to MSExcel worksheet
#5.1 - Changed it to work locally on the server
#5.2 - Changed to Version 18 of the questionnaire

import ssaw, os, winsound, sys, fileinput, time, json
import pandas as pd
from ssaw import ExportApi
from ssaw.models import ExportJob
from datetime import datetime, date
from shutil import move
from tempfile import NamedTemporaryFile

#enable logging to both screen and textfile
class Logger(object):
    def __init__(self):
        self. terminal = sys.stdout
        self.log = open("ssawlog.txt", "a")
        
    def write(self, message):
#        self.terminal.write(message)
        self.log.write(message)
        
    def flush(self):
        pass

sys.stdout = Logger()

#assign api info. I think this obfuscates the username\password    
with open('api.json', 'r') as apifile: 
    data = json.load(apifile) 
client = ssaw.Client(url=data['url'], api_user=data['api_user'], api_password=data['api_password'], workspace=data['workspace'])

# generate the job first (True) or just download (False)? True is required to ensure that the latest data is downloaded. False is useful if redownloading recently downloaded data.
generate = False
# Type of export. Possible values are Tabular, STATA, SPSS, Binary, DDI, Paradata
etype = "Tabular"
# Questionnaire status. Possible values are  All, SupervisorAssigned, InterviewerAssigned, Completed, RejectedBySupervisor, ApprovedBySupervisor, RejectedByHeadquarters, ApprovedByHeadquarters
istatus = "ALL"
starttime = datetime.now()
today = str(date.today())
szip = r'start 7z x -aoa -o* '
homedir = data['homedir']
file18 = homedir+'\CLFSS_18_Tabular_'+istatus+'('+today+')\CLFSS_PERSONS.tab'
temp_path = 'temp'
filelist = [file18]
finalfile = 'Weekly Updates\\'+today+'.txt'
finalexcel = 'Weekly Updates\\CLFSS '+today+'.xlsx'
numlines = 0
quesid = data['questionnaire_identity']

argscawi1 = {
    "questionnaire_identity": quesid,
    "export_type": etype,
    "interview_status": istatus
}

# without export_path parameter file will be saved
# in the current working directory

print("Data download started at ", starttime)
print('Be patient! Some files can take a while to download')

#Labourforce v18
print('Getting LFS data V18 in tab format...')
# there is no ready export, start a new job
if generate == True:
    job = ExportJob(**argscawi1)
    job = ExportApi(client, workspace=data['workspace']).start(job, wait=True, show_progress=True)
print("Downloading...")
response = ExportApi(client, workspace=data['workspace']).get(**argscawi1, show_progress=True)
os.rename('CLFSS_18_Tabular_'+istatus+'.zip', 'CLFSS_18_Tabular_'+istatus+'('+today+').zip')
print('Done!\n')
os.system(szip+r'CLFSS_18_Tabular_'+istatus+'('+today+').zip"')

#wait 5 seconds to make sure that the file is unzipped
print("Waiting for 5 seconds to make sure we're fully unzipped\n")
time.sleep(5)

#remove the headers for version 15. Leave this in just in case I have to deal with multiple files again
#print("Formatting files...")
#with open(file15, 'r', encoding='utf-8') as f_in:
#    with NamedTemporaryFile(mode='w', delete=False) as f_out:
#        temp_path = f_out.name
#        next(f_in)
#        for line in f_in:
#            f_out.write(line)
#os.remove(file15)
#move(temp_path,file15)
#print('Done!\n')

#Concatenate the files
print('Concatenating files...')
with open(finalfile,'w') as final, fileinput.input(filelist) as fin:
    for line in fin:
        final.write(line)
        numlines = numlines + 1
print('Done!\n')

print(str(numlines)+' lines written!')
#read the csv (as tab delimited, header at row 0, use python engine)
df = pd.read_csv(finalfile, sep="\t", header=0, engine="python")
print("Exporting to Excel...")
#export to excel (with a header, using openpyxl, don't insert a row index)
df.to_excel(finalexcel, sheet_name='Sheet1', header=True, engine='openpyxl', index=False)
print('Final file has been stored in: '+ homedir + '\\' + finalexcel)

endtime = datetime.now()
print("Script ended at ", endtime)
print("runtime is ", endtime-starttime)
print("-------------------------------------------------------------------------------\n\n")
#winsound.Beep(500,100)

