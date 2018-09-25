# convertGlucoseToMg_dL.py
# Converts the glucose values from mmol/L to mg/dL
import pandas as pd
import os
import sys
sys.path.append("..")
from pythonScripts.jsonToCsv import convertToCsv

def convertGlucValues():
	# get correct path to csv file
	pathToCsv = convertToCsv()

	# this is the column in the csv we want to look at
	colNames = ["value"]
	
	#----------Create data frame-------------------
	data = pd.read_csv(pathToCsv, usecols=colNames)
	data = data[pd.notnull(data["value"])] # remove values that are NaN
	#----------------------------------------------

	#--------Do conversion across entire dataset---------------
	# conversion mmol/L to mg/dL
	conversionFactor = 18
	data = data.mul(conversionFactor)
	#----------------------------------------------------------

	# for now im just printing the data i guess
	print(data)

def main():
	convertGlucValues()

if __name__ == '__main__':
	main()