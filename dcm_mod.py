"""
Created on Tue Aug  3 11:15:21 2020

@author: tryexc
"""
import shutil
import time
import os
from os import listdir

############################################################
# Set path to Dicom-Dir
p = ''
# Set new DICOM Tags
Pname = '' # PatientName
PbDay = '' # PatientID
Pid = '' # PatientBirthDate
StudDes = '' # StudyDescription
d = '' # output directory
errorlog = '.../copyErrorLog.txt' # set path to error logfile
############################################################
def list_files(directory, extension):
    return (f for f in listdir(directory) if f.endswith('.' + extension))


for patDir in os.listdir(p):
    for seqDir in os.listdir(p+'/'+patDir):
        files = list_files( p+'/'+patDir + '/' + seqDir, "dcm")
        src = p+'/'+patDir + '/' + seqDir 
        dst = d + Pname + '/' + seqDir # modify structure if needed
        shutil.copytree(src, dst,False,lambda x,y:[r for r in y if os.path.isfile(x+os.sep+r)])
        time.sleep(3)
       
        for f in files:
            dataset = pydicom.dcmread(p+'/'+patDir + '/' + seqDir + '/' + f)
            try:
                           
                dataset.data_element('PatientName').value = Pname
                dataset.data_element('PatientID').value = Pid
                dataset.data_element('PatientBirthDate').value = PbDay
                dataset.data_element('StudyDescription').value = StudDes
                dataset.data_element('PerformingPhysicianName').value = '' # removed here
                

                dataset.save_as(dst + '/' + f)
                print('Save: '+dst + '/' + f)
                
            except Exception as e:
                print(e)
                log_file = open(errorlog, 'a')
                log_file.write(src + '\n')
                log_file.close()
print('remove orig. data....')
#shutil.rmtree(p) #  if needed!
print('done....')