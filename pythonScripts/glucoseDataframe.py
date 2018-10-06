# glucoseDataFrame.py
# sets up glucose info dataframe for analysis
# TODO add the other columns rn it just does the actual glucose values
import pandas as pd
import numpy as np
import os
import sys
sys.path.append("..")
from pythonScripts.jsonToCsv import convertToCsv

from datetime import date
from dateutil.parser import parse

def createDataframe():
	# get correct path to csv file
	pathToCsv = convertToCsv()
	currentFile = os.path.basename(pathToCsv)
	print(f"Currently Reading File: {currentFile}")

	# this is the column in the csv we want to look at
	gluValues = ["value"]
	
	#----------Create data frame-------------------
	data = pd.read_csv(pathToCsv) #get all data from csv
	data = data[pd.notnull(data["value"])] # remove values that are NaN
	#----------------------------------------------

	#----------Get data columns--------------------
	glu = data.loc[:,'value']
	timestamp = data.loc[:,'time']
	#----------------------------------------------

	#--------Do conversion across entire dataset---------------
	# conversion mmol/L to mg/dL
	conversionFactor = 18.01559
	glu = glu.mul(conversionFactor)
	#----------------------------------------------------------

	#--------Save month, day, weekday, hour, minutes---------------
	index = timestamp.index

	monthList = []
	dayList = []
	weekdayList = []
	hourList = []
	minutesList = []

	timeStr = timestamp.astype(str).values.tolist()
	for i in timeStr:
		#for months
		month = parse(i).month
		monthList.append(month)
		#for days
		day = parse(i).day
		dayList.append(day)
		#for weekdays
		weekday = parse(i).weekday()
		weekdayList.append(weekday)
		#for hours
		hour = parse(i).hour
		hourList.append(hour)
		#for minutes
		minute = parse(i).minute
		minutesList.append(minute)


	#pd.DataFrame('month',monthList)
	monthdf = pd.DataFrame(np.array(monthList),index=index)
	daydf = pd.DataFrame(np.array(dayList),index=index)
	weekdaydf = pd.DataFrame(np.array(weekdayList),index=index)
	hourdf = pd.DataFrame(np.array(hourList),index=index)
	minutesdf = pd.DataFrame(np.array(minutesList),index=index)
	#--------------------------------------------------------------

	#-------Dicts----------
	#basal rates (unit/hour)
	basal = {
		"00:00" : .625,
		"02:30" : .650,
		"04:00" : .800,
		"08:00" : .725,
		"12:00" : .700,
		"14:00" : .250,
		"19:00" : .650
	}

	#insulin sensitivity (mg/dL/unit)
	sensitivity = {
		"00:00" : 60,
		"06:00" : 70,
		"09:00" : 60,
		"12:00" : 60,
		"15:00" : 60
	}

	#carb ratio (grams/unit)
	carbRatio = {
		"00:00" : 10,
		"06:00" : 5,
		"11:30" : 5.5,
		"14:00" : 6,
		"18:00" : 7,
		"21:00" : 9
	}
	#----------------------

	#--------Concatenate all of the dataframes into one dataframe----------------------------
	final = pd.concat([timestamp,glu,monthdf,daydf,weekdaydf,hourdf,minutesdf],axis=1,ignore_index=True) #concatenate the dataframe together
	#----------------------------------------------------------------------------------------

	#print(data)
	pathBaseName = os.path.basename(pathToCsv)
	pathBaseName = "OUTPUT_" + pathBaseName
	pathBaseName = os.path.join(os.path.dirname(pathToCsv), pathBaseName)
	header = ["TimeStamp", "Glucose (ml/dL)", "Month", "Day","Weekday", "Hour","Minutes"]
	final.to_csv(pathBaseName,header=header)		# return dataframes as a csv

def main():
	createDataframe()

if __name__ == '__main__':
	main()