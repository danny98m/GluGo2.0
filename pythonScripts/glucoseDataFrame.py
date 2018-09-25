# glucoseDataFrame.py
# sets up glucose info dataframe for analysis
# TODO add the other columns rn it just does the actual glucose values
import pandas as pd
import os
import sys
sys.path.append("..")
from pythonScripts.jsonToCsv import convertToCsv

def createDataframe():
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

	#print(data)
	pathBaseName = os.path.basename(pathToCsv)
	pathBaseName = "OUTPUT_" + pathBaseName
	pathBaseName = os.path.join(os.path.dirname(pathToCsv), pathBaseName)
	data.to_csv(pathBaseName)				# return dataframe as a csv

def main():
	createDataframe()

if __name__ == '__main__':
	main()