# glucoseDataFrame.py
# sets up glucose info dataframe for analysis
import sys
sys.path.append("..") # proper file path for importing local modules

import pandas as pd
import numpy as np
import os
from pythonScripts.jsonToCsv import convertToCsv
from datetime import date
from dateutil.parser import parse

#-------CONSTANTS-------------
CONVERSION_FACTOR = 18.01559
#-----------------------------

def createDataframe():
	# get correct path to csv file
	pathToCsv = convertToCsv()
	currentFile = os.path.basename(pathToCsv)
	print(f"Currently Reading File: {currentFile}")

	# this is the column in the csv we want to look at
	gluValues = ["value"]
	#----------Create data frame-------------------
	glucLevelData = pd.read_csv(pathToCsv) #get all data from csv
	glucLevelData = glucLevelData[pd.notnull(glucLevelData["value"])] # remove values that are NaN
	#----------------------------------------------

	#----------Get data columns--------------------
	glu = glucLevelData.loc[:,'value']
	timestamp = glucLevelData.loc[:,'time']
	#----------------------------------------------

	#--------Do conversion across entire dataset---------------
	# conversion mmol/L to mg/dL
	#----------------------------------------------------------
	glu = glu.mul(CONVERSION_FACTOR)
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
	#pathToBolus = 'csvData/csvInData/Kate_CareLink_Export.csv'
	#bolusData = pd.read_csv(pathToBolus)

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

	#=======NASTY CODE FOR CARB AND BOLUS OUTPUT============================
	pathToCareLink = os.path.join(os.getcwd(), "csvData", "csvInData")
	bolus_carbCsv = pd.read_csv(os.path.join(pathToCareLink, 'Kate_CareLink_Export_test.csv'))

	bolus = bolus_carbCsv.loc[:,'Bolus Volume Delivered (U)']
	date = bolus_carbCsv.loc[:, 'Date']
	time = bolus_carbCsv.loc[:, 'Time']
	carb = bolus_carbCsv.loc[:, 'BWZ Carb Input (grams)']
	header = ['Date', 'Time', 'Bolus (U)', 'Carb Input (grams)']
	bolus_carbData = pd.concat([date,time,bolus,carb],axis=1, ignore_index=True)
	bolus_carbData = bolus_carbData.dropna(subset=[2, 3], how='all')

	pathToOutCsvBC = os.path.join(os.getcwd(), "csvData", "csvOutData")
	pathToOutCsvBC = os.path.join(pathToOutCsvBC, "bolus_carb_output.csv")
	bolus_carbData.to_csv(pathToOutCsvBC, header=header)
	#=========================================================================

	#--------Concatenate all of the dataframes into one dataframe----------------------------
	final = pd.concat([timestamp,glu,monthdf,daydf,weekdaydf,hourdf,minutesdf],axis=1,ignore_index=True) #concatenate the dataframe together
	#----------------------------------------------------------------------------------------
	#print(final)
	
	pathBaseName = os.path.basename(pathToCsv)
	outputFileName = "OUTPUT_" + pathBaseName
	pathToOutCsv = os.path.join(os.getcwd(), "csvData", "csvOutData")
	outputFilePath = os.path.join(pathToOutCsv, outputFileName)
	header = ["TimeStamp", "Glucose (ml/dL)", "Month", "Day","Weekday", "Hour","Minutes"]
	final.to_csv(outputFilePath,header=header)		# return dataframes as a csv
	
def main():
	createDataframe()

if __name__ == '__main__':
	main()
