import pandas as pd
import os
import os.path
import sys

def convert():
    #------Setup Proper Portable File Path------------
    os.chdir("..")                                              # Go back in directory
    jsonPath = os.path.join("jsonData", "test_kates_data.json") # Set up directory
    absoluteJsonPath =  os.path.abspath(jsonPath)               # Create absolute path
    print(f"Changing directory to {absoluteJsonPath}")

    # Checking if path exists
    if (os.path.exists(absoluteJsonPath) != True):
        print(f"Path {absoluteJsonPath} does not exist")
        sys.exit()                                              # Quit program if not found

    csvPath = os.path.join("csvData")                           # Add csv path
    df = pd.read_json(absoluteJsonPath)                         # Read json file
    df.to_csv(os.path.join(csvPath, 'test_kates_data.csv'))     # Convert

def main():
    # should later allow convert to take file argument to make this portable
    convert()


if __name__ == "__main__":
    main()