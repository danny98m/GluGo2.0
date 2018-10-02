'''
====================================
Programmer: Yun Zhang
====================================
Summary:
This python script reads output file of glucose level predication and split the data
to two different files: 1) predication made based on the first mode and 2) predication
made based on the second mode. The two output files will include: time, predict glucose
level, actual level, and carb intake (if based on mode 1)

INPUT:
glucose prediction csv file

OUTPUT:
two csv files

CAUTION:
Please arrange the glucose predication csv file in CHRONOLOGICAL order and delete 
any carb intake that were entered as "0".
'''
import csv
import datetime

#------------------ GLOBAL CONSTANTS --------------------------
MODE_1_TIME_RANGE = 15300

#------------------ DEFINE VARIABLES --------------------------
mode_1 = []
mode_2 = []
time = []
timestamp = []
predict_value = []
actual_value = []
carb_intake = []
carbIntakeTime = 0

print ("Please make sure data in input CSV file is listed in chronological order.")
input ("Press any key to continue...")

# read the glucose prediction result file and append each row in different lists 
with open ("gluPredict.csv", mode='r') as fd:
    reader = csv.reader(fd)
    for row in reader:
        # string time
        time.append(row[0])
        
        # convert to timestamp and store
        convertDate = datetime.datetime.strptime(row[0], '%m/%d/%y %H:%M').timestamp()
        timestamp.append(convertDate)
        
        # glucose predication value
        predict_value.append(row[1])
        
        # actual glucose value 
        actual_value.append(row[2])
        
        # carb intake 
        if (len(row[3]) > 0 and row[3] != 0):
            carb_intake.append(row[3])
        else:
            carb_intake.append(0)

# determine which mode has been used 
for index in range(0, len(time)):
    
    # determine carb intake timestamp
    if (carb_intake[index] != 0):
        mode_1.append([time[index], predict_value[index], actual_value[index], carb_intake[index]])
        carbIntakeTime = timestamp[index]
        
    # determine glucose level predicted using mode 1 and store
    if ((timestamp[index] - carbIntakeTime) <= MODE_1_TIME_RANGE):
        mode_1.append([time[index], predict_value[index], actual_value[index]])
        
    # append data predicted using mode 2
    else:
        mode_2.append([time[index], predict_value[index], actual_value[index]])
  
# write to two separate csv files   
with open("mode1_result.csv", 'w') as output:
    writer = csv.DictWriter(output, ['Date', 'Predict Value', 'Actual Value','Carb Intake'])
    writer.writeheader()      
    writer = csv.writer(output)
    writer.writerows(mode_1)
  
with open("mode2_result.csv", 'w') as output:
    writer = csv.DictWriter(output, ['Date', 'Predict Value', 'Actual Value'])
    writer.writeheader()                      
    writer = csv.writer(output)
    writer.writerows(mode_2)      
        
        
print ("\n\nDone.\n")