import csv
import datetime
import pandas as pd

#------------------ GLOBAL CONSTANTS --------------------------
TIME_INTERVAL = 5

#------------------ DEFINE VARIABLES --------------------------
time = []
slope = []
glucose = []
month = []
day = []
weekday = []
hour = []
minutes = []
slopeIncrease = []
slopeDecrease = []

currentSlope = 0
currentMinute = 0

print ("Please make sure data in input CSV file is listed in chronological order.")
input ("Press any key to continue...")

# read the dataset and grab slope, glucose level, month, weekday, hour, and minutes to lists
df = pd.read_csv('OUTPUT_data_download_Kate_access.csv')
slope = df["Slope"].tolist()
glucose = df["Glucose (ml/dL)"].tolist()
month = df["Month"].tolist()
day = df["Day"].tolist()
weekday = df["Weekday"].tolist()
hour = df["Hour"].tolist()
minutes = df["Minutes"].tolist()

# check for abnormal increasing/decreasing trend
for index in range (0, len(slope)):
    previousSlope = currentSlope
    currentSlope = slope[index]
    previousMinute = currentMinute
    currentMinute = minutes[index]
    if (currentSlope >= previousSlope and glucose[index] >= 230 and abs(currentMinute-previousMinute) > TIME_INTERVAL):
        slopeIncrease.append([glucose[index],month[index],day[index],weekday[index],hour[index],minutes[index]])
    elif (currentSlope <= previousSlope and glucose[index] <= 70 and abs(currentMinute-previousMinute) > TIME_INTERVAL):
        slopeDecrease.append([glucose[index],month[index],day[index],weekday[index],hour[index],minutes[index]])
        
# write to two separate csv files   
with open("trendIncrease.csv", 'w') as output:
    writer = csv.DictWriter(output, ['Glucose','Month','Day','Weekday','Hour','Minutes'])
    writer.writeheader()      
    writer = csv.writer(output)
    writer.writerows(slopeIncrease)
          
with open("trendDecrease.csv", 'w') as output:
    writer = csv.DictWriter(output, ['Glucose','Month','Day','Weekday','Hour','Minutes'])
    writer.writeheader()                      
    writer = csv.writer(output)
    writer.writerows(slopeDecrease)      
                
                
print ("\n\nDone.\n")
    
    
        