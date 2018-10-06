# jsonToCsv.py
# Takes json file and converts it to csv
# TODO: make convert work with any file passed (either as an argument or through input)

import pandas as pd
import os
import os.path
import sys

def convertToCsv():
    #------Setup Proper Portable JSON File Path-----------------
    os.chdir("..")                                                      # Go back in directory
    files = []                                                          # Create empty list

    # TODO: can use this to convert just every json file in directory
    # Add files from jsonData to list
    for (dirpath, dirnames, filenames) in os.walk("jsonData"):
        files.extend(filenames)

    # List all json files in directory
    print("---------------------------------")
    print("JSON files in current directory..")
    for file in files:
        print(file)

    desiredConvertFile = input("\nEnter JSON File For Conversion: ")
    jsonPath = os.path.join("jsonData", desiredConvertFile)             # Set up directory
    absoluteJsonPath =  os.path.abspath(jsonPath)                       # Create absolute path
    print(f"Changing directory to {absoluteJsonPath}")
    #-----------------------------------------------------------

    # Checking if path exists......
    if (os.path.exists(absoluteJsonPath) != True):
        print(f"Path {absoluteJsonPath} does not exist")
        sys.exit()                                                      # Quit program if not found

    # If you're here the path exists.. congrats
    #--------------CSV Path Setup-------------------------------
    csvPath = os.path.join("csvData", "csvInData")                                   # Add csv path
    absoluteCsvPath = os.path.abspath(csvPath)
    #-----------------------------------------------------------

    #-------------Convert JSON to CSV---------------------------
    newFileName = desiredConvertFile.split(".json")
    newFileName = newFileName[0]                                        # Eventually make this non mutated
    newFileName += ".csv"
    df = pd.read_json(absoluteJsonPath)                                 # Read json file
    df.to_csv(os.path.join(absoluteCsvPath, newFileName))               # Convert
    #-----------------------------------------------------------
    destinationPath = os.path.abspath(os.path.join(absoluteCsvPath, newFileName))
    print(f"\nCSV file created in {destinationPath}\n")

    return destinationPath


def main():
    # should later allow convert to take file argument to make this portable
    convertToCsv()

if __name__ == "__main__":
    main()