# glucoseDataFrame.py
# sets up glucose info dataframe for analysis
import sys
sys.path.append("..") # proper file path for importing local modules

import pandas as pd
import numpy as np
import os
import math
from datetime import *
from pythonScripts.jsonToCsv import convertToCsv
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
	glucLevelData = glucLevelData[pd.notnull(glucLevelData["value"])] # remove rows that are NaN for value
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
	indexy = timestamp.index # save the index from this dataframe as variable index

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

	#convert the lists to dataframes while ensuring the index corresponds to the other dataframes
	monthdf = pd.DataFrame(np.array(monthList),index=indexy)
	daydf = pd.DataFrame(np.array(dayList),index=indexy)
	weekdaydf = pd.DataFrame(np.array(weekdayList),index=indexy)
	hourdf = pd.DataFrame(np.array(hourList),index=indexy)
	minutesdf = pd.DataFrame(np.array(minutesList),index=indexy)
	#--------------------------------------------------------------

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
	bolus_carbCsv = pd.read_csv(os.path.join(pathToCareLink, 'Kate_CareLink_Export.csv'),skiprows=6)

	bolus = bolus_carbCsv.loc[:,'Bolus Volume Delivered (U)']
	date = bolus_carbCsv.loc[:, 'Date']
	time = bolus_carbCsv.loc[:, 'Time']
	carb = bolus_carbCsv.loc[:, 'BWZ Carb Input (grams)']
	bolus_carbData = pd.concat([date,time,bolus,carb],axis=1, ignore_index=True)
	bolus_carbData = bolus_carbData.dropna(subset=[2, 3], how='all') #remove column if NaN value in both columns 2&3
	bolus_carbData = bolus_carbData.drop(bolus_carbData.index[len(bolus_carbData)-1]) #get rid of last header row
	bolus_carbData.columns = ["Date", "Time", "Bolus (U)", "Carb Input (grams)"]
	#-------------------------------------------------------------------------

	#--------Save month, day, weekday, hour, minutes---------------

	monthListB = []
	dayListB = []
	weekdayListB = []
	hourListB = []
	minutesListB = []

	date = bolus_carbData.loc[:, 'Date']
	time = bolus_carbData.loc[:, 'Time']

	indexBolus = date.index # save the index from this dataframe as variable index

	dayStr = date.astype(str).values.tolist()
	timeStrB = time.astype(str).values.tolist()
	for j in timeStrB:
		timeWhole = datetime.strptime(j, '%H:%M:%S')
		#for months
		hourListB.append(timeWhole.hour)
		#for days
		minutesListB.append(timeWhole.minute)
	for k in dayStr:
		dateWhole = datetime.strptime(k, '%Y/%m/%d')
		#for hours
		monthListB.append(dateWhole.month)
		#for minutes
		dayListB.append(dateWhole.day)

	#convert the lists to dataframes while ensuring the index corresponds to the other dataframes
	monthdfBolus = pd.DataFrame(np.array(monthListB),index=indexBolus)
	daydfBolus = pd.DataFrame(np.array(dayListB),index=indexBolus)
	hourdfBolus = pd.DataFrame(np.array(hourListB),index=indexBolus)
	minutesdfBolus = pd.DataFrame(np.array(minutesListB),index=indexBolus)

	#concatenate all of these
	bolus_carbFinal = pd.concat([bolus_carbData,monthdfBolus,daydfBolus,hourdfBolus,minutesdfBolus],axis=1, ignore_index=True)
	bolus_carbFinal.columns = ["Date", "Time", "Bolus (U)", "Carb Input (grams)", "Month", "Day", "Hour","Minutes"]
	
	#--------------------------------------------------------------

	#--------Concatenate all of the dataframes into one dataframe----------------------------
	final = pd.concat([timestamp,glu,monthdf,daydf,weekdaydf,hourdf,minutesdf],axis=1,ignore_index=True) #concatenate the dataframe together
	#give columns names
	final.columns = ["TimeStamp", "Glucose (mg/dL)", "Month", "Day","Weekday", "Hour","Minutes"]
	#----------------------------------------------------------------------------------------
	
	
	#MERGE MEDTRONIC DATA WITH DEXCOM
	#----------------------------------------------------------------------------------------
	#make dataframe of NaN filled bolus and carb columns with indexes matching tidepool
	bolusCarbdf = pd.DataFrame(np.nan, index=indexy, columns=["Bolus (U)", "Carb Input (grams)"])

	#match up the bolus insulin & carb intake from one csv
	for indexMed, rowMed in bolus_carbFinal.iterrows(): #go through Medtronic Data
		minsMed = getattr(rowMed, "Minutes")
		hrsMed = getattr(rowMed, "Hour")
		dayMed = getattr(rowMed, "Day")
		monthMed = getattr(rowMed, "Month")
		bolusMed = getattr(rowMed, "Bolus (U)")
		
		carbMed = getattr(rowMed, "Carb Input (grams)")
		curSmalls = -1
		gotOne = False
		for indexTide, rowTide in final.iterrows():		#go through Tidepool Data
			minsTide = getattr(rowTide, "Minutes")
			hrsTide = getattr(rowTide, "Hour")
			dayTide = getattr(rowTide, "Day")
			monthTide = getattr(rowTide, "Month")
			#find closest time in Tidepool data to Medtronic data
			if monthTide == monthMed and dayTide == dayMed and hrsTide == hrsMed:
				difTime = minsMed - minsTide #time difference of medtronic time minux tidepool time
				if (difTime) <= 5:
					curSmalls = indexTide
				if gotOne:
					break #get out of this inner loop as we found the time we wanted for this data
				if (difTime) <= 5:
					gotOne = True
		
		#add bolus & carb info to bolusCarbdf
		if curSmalls != -1:
			if not math.isnan(float(carbMed)):
				bolusCarbdf.loc[curSmalls, 'Carb Input (grams)'] = carbMed
			if not math.isnan(float(bolusMed)):
				bolusCarbdf.loc[curSmalls, 'Bolus (U)'] = bolusMed
			
	#--------Concatenate all of the bolusCarbdf dataframe with final dataframe----------------------------
	almostFinal = pd.concat([timestamp,glu,monthdf,daydf,weekdaydf,hourdf,minutesdf,bolusCarbdf],axis=1,ignore_index=True) #concatenate the dataframes together
	#give columns names
	almostFinal.columns = ["TimeStamp", "Glucose (mg/dL)", "Month", "Day","Weekday", "Hour","Minutes","Bolus (U)", "Carb Input (grams)"]
	#----------------------------------------------------------------------------------------


	#----------------------------------------------------------------------------------------
	#create initial csv OUTPUT
	pathBaseName = os.path.basename(pathToCsv)
	outputFileName = "OUTPUT_" + pathBaseName
	pathToOutCsv = os.path.join(os.getcwd(), "csvData", "csvOutData")
	outputFilePath = os.path.join(pathToOutCsv, outputFileName)
	almostFinal.to_csv(outputFilePath)		# return dataframes as a csv
	#----------------------------------------------------------------------------------------

	#----------------------------------------------------------------------------------------
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
	#----------------------------------------------------------------------------------------

	
	#--------Concatenate the new dataframes into final dataframe----------------------------
	realFinal = pd.concat([timestamp,glu,basaldf,insulindf,carbdf,monthdf,daydf,weekdaydf,hourdf,minutesdf,bolusCarbdf],axis=1,ignore_index=True) #concatenate the dataframe together
	#----------------------------------------------------------------------------------------

	#create final csv OUTPUT (rewrites the earlier csv file)
	header = ["TimeStamp", "Glucose (mg/dL)", "Basal Insulin (U/hr)","Insulin Sensitivity (mg/dL/U)","Carb Ratio (g/U)", "Month", "Day","Weekday", "Hour","Minutes","Bolus (U)", "Carb Input (grams)"]
	realFinal.to_csv(outputFilePath,header=header)		# return dataframes as a csv
	
	
def main():
	createDataframe()

if __name__ == '__main__':
	main()
