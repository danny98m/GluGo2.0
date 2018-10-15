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
	#----------------------------------------------------------

	#--------Save month, day, weekday, hour, minutes---------------
	indexy = timestamp.index #save the index from this dataframe as variable index

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
	#convert the lists to dataframes while ensuring the index corresponds to the other dataframes
	monthdf = pd.DataFrame(np.array(monthList),index=indexy)
	daydf = pd.DataFrame(np.array(dayList),index=indexy)
	weekdaydf = pd.DataFrame(np.array(weekdayList),index=indexy)
	hourdf = pd.DataFrame(np.array(hourList),index=indexy)
	minutesdf = pd.DataFrame(np.array(minutesList),index=indexy)
	#--------------------------------------------------------------
	#pathToBolus = 'csvData/csvInData/Kate_CareLink_Export.csv'
	#bolusData = pd.read_csv(pathToBolus)

	#-------Dicts----------
	#basal rates (unit/hour)
	basal = {
		"0" : .625,
		"2" : .650,		#if hour equals 2, then also minute = 30 cause (2:30)
		"4" : .800,
		"8" : .725,
		"12" : .700,
		"14" : .250,
		"19" : .650
	}

	#insulin sensitivity (mg/dL/unit)
	sensitivity = {
		"0" : 60,
		"6" : 70,
		"9" : 60,
		"12" : 60,
		"15" : 60
	}

	#carb ratio (grams/unit)
	carbRatio = {
		"0" : 10,
		"6" : 5,
		"11" : 5.5,		#if hour equals 11, then also minute = 30 cause (11:30)
		"14" : 6,
		"18" : 7,
		"21" : 9
	}
	#----------------------

	#---------NASTY CODE FOR CARB AND BOLUS OUTPUT---------------------------
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
	#-------------------------------------------------------------------------

	#--------Concatenate all of the dataframes into one dataframe----------------------------
	final = pd.concat([timestamp,glu,monthdf,daydf,weekdaydf,hourdf,minutesdf],axis=1,ignore_index=True) #concatenate the dataframe together
	#----------------------------------------------------------------------------------------
	
	#create initial csv OUTPUT
	pathBaseName = os.path.basename(pathToCsv)
	outputFileName = "OUTPUT_" + pathBaseName
	pathToOutCsv = os.path.join(os.getcwd(), "csvData", "csvOutData")
	outputFilePath = os.path.join(pathToOutCsv, outputFileName)
	header = ["TimeStamp", "Glucose (ml/dL)", "Month", "Day","Weekday", "Hour","Minutes"]
	final.to_csv(outputFilePath,header=header)		# return dataframes as a csv

	basalSensRatioData = pd.read_csv(outputFilePath)

	basalList = []
	insulinSensList = []
	carbRatioList = []

	for index, row in basalSensRatioData.iterrows():
		#for basal list
		if row['Hour'] >= 0 and row['Hour'] < 3:
			if row['Hour'] == 2 and row['Minutes'] < 30:
				basalList.append(basal["0"])
			elif row['Hour'] == 2 and row['Minutes'] >= 30:
				basalList.append(basal["2"])
			else:
				basalList.append(basal["0"])
		elif row['Hour'] >= 3 and row['Hour'] < 4:
			basalList.append(basal["2"])
		elif row['Hour'] >= 4 and row['Hour'] < 8:
			basalList.append(basal["4"])
		elif row['Hour'] >= 8 and row['Hour'] < 12:
			basalList.append(basal["8"])
		elif row['Hour'] >= 12 and row['Hour'] < 14:
			basalList.append(basal["12"])
		elif row['Hour'] >= 14 and row['Hour'] < 19:
			basalList.append(basal["14"])
		elif row['Hour'] >= 19 and row['Hour'] < 24:
			basalList.append(basal["19"])

		#for insulin sensitivity list
		if row['Hour'] >= 0 and row['Hour'] < 6:
			insulinSensList.append(sensitivity["0"])
		elif row['Hour'] >= 6 and row['Hour'] < 9:
			insulinSensList.append(sensitivity["6"])
		elif row['Hour'] >= 9 and row['Hour'] < 12:
			insulinSensList.append(sensitivity["9"])
		elif row['Hour'] >= 12 and row['Hour'] < 15:
			insulinSensList.append(sensitivity["12"])
		elif row['Hour'] >= 15 and row['Hour'] < 24:
			insulinSensList.append(sensitivity["15"])

		#for carb ratio list 
		if row['Hour'] >= 0 and row['Hour'] < 6:
			carbRatioList.append(carbRatio["0"])
		elif row['Hour'] >= 6 and row['Hour'] < 12:
			if row['Hour'] == 11 and row['Minutes'] < 30:
				carbRatioList.append(carbRatio["6"])
			elif row['Hour'] == 11 and row['Minutes'] >= 30:
				carbRatioList.append(carbRatio["11"])
			else:
				carbRatioList.append(carbRatio["6"])
		elif row['Hour'] >= 12 and row['Hour'] < 14:
			carbRatioList.append(carbRatio["11"])
		elif row['Hour'] >= 14 and row['Hour'] < 18:
			carbRatioList.append(carbRatio["14"])
		elif row['Hour'] >= 18 and row['Hour'] < 21:
			carbRatioList.append(carbRatio["18"])
		elif row['Hour'] >= 21 and row['Hour'] < 24:
			carbRatioList.append(carbRatio["21"])

	#create dataframes from lists
	basaldf = pd.DataFrame(np.array(basalList),index=indexy) #like above set index to index
	insulindf = pd.DataFrame(np.array(insulinSensList),index=indexy) #like above set index to index
	carbdf = pd.DataFrame(np.array(carbRatioList),index=indexy) #like above set index to index
	

	
	#--------Concatenate the new dataframes into final dataframe----------------------------
	realFinal = pd.concat([timestamp,glu,basaldf,insulindf,carbdf,monthdf,daydf,weekdaydf,hourdf,minutesdf],axis=1,ignore_index=True) #concatenate the dataframe together
	#----------------------------------------------------------------------------------------

	#create final csv OUTPUT (rewrites the earlier csv file)
	header = ["TimeStamp", "Glucose (ml/dL)", "Basal Insulin (U/hr)","Insulin Sensitivity (mg/dL/U)","Carb Ratio (g/U)", "Month", "Day","Weekday", "Hour","Minutes"]
	realFinal.to_csv(outputFilePath,header=header)		# return dataframes as a csv
	
	
def main():
	createDataframe()

if __name__ == '__main__':
	main()
