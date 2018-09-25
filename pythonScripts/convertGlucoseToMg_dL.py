# convertGlucoseToMg_dL.py
# Converts the glucose values from mmol/L to mg/dL
import pandas as pd
import os
import sys
sys.path.append("..")
from pythonScripts.jsonToCsv import convertToCsv

def convertGlucValues():
	colNames = ["value"]
	#os.chdir("..")
	#print(os.getcwd())
	pathToCsv = convertToCsv()
	data = pd.read_csv(pathToCsv, names=colNames)
	#print(pathToCsv)




def main():
	convertGlucValues()

if __name__ == '__main__':
	main()