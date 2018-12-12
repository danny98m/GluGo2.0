"""
glucoseDataFrame.py

Creates a dataframe of glucose related statistics
in diabetics for predictive analysis.
"""
import sys
import os
import math
from datetime import *
from dateutil.parser import parse
import pandas as pd
import numpy as np

sys.path.append("..") # proper file path for importing local modules
from pythonScripts.jsonToCsv import convertToCsv

#-------CONSTANTS-------------
CONVERSION_FACTOR = 18.01559
#-------Dicts----------
    #basal rates (unit/hour)
BASAL = {
    "0" : .625,
    "2" : .650,     #if hour equals 2, then also minute = 30 cause (2:30)
    "4" : .800,
    "8" : .725,
    "12" : .700,
    "14" : .250,
    "19" : .650
}

#insulin sensitivity (mg/dL/unit)
SENSITIVITY = {
    "0" : 60,
    "6" : 70,
    "9" : 60,
    "12" : 60,
    "15" : 60
}

#carb ratio (grams/unit)
CARB_RATIO = {
    "0" : 10,
    "6" : 5,
    "11" : 5.5,     #if hour equals 11, then also minute = 30 cause (11:30)
    "14" : 6,
    "18" : 7,
    "21" : 9
}
#----------------------
#-----------------------------

def convert_glucose(glucose_levels):
    """Do conversion across entire dataset
    conversion mmol/L to mg/dL"""

    value_row = glucose_levels.loc[:, 'value']

    convert_row = value_row.mul(CONVERSION_FACTOR)
    round_conversion = convert_row.round(2)

    return round_conversion

def divide_timestamp(time_row):
    """Seperates timestamp into individual
    months, days, weekdays, hours, and minutes"""
    month_list = []
    day_list = []
    weekday_list = []
    hour_list = []
    minutes_list = []

    time_str = time_row.astype(str).values.tolist()
    for i in time_str:
        #for months
        month = parse(i).month
        month_list.append(month)
        #for days
        day = parse(i).day
        day_list.append(day)
        #for weekdays
        weekday = parse(i).weekday()
        weekday_list.append(weekday)
        #for hours
        hour = parse(i).hour
        hour_list.append(hour)
        #for minutes
        minute = parse(i).minute
        minutes_list.append(minute)

    return month_list, day_list, weekday_list, hour_list, minutes_list

def create_dataframe():
    """Creates dataframe for glucose analysis"""

    #---get correct path to csv input file-----------
    path_to_input_csv = convertToCsv()
    current_file = os.path.basename(path_to_input_csv)
    print(f"Currently Reading File: {current_file}")
    care_link_file = input("\nEnter Medtronic File: ")
    #------------------------------------------------

    #----------Create data frame-------------------
    #get all data from csv
    gluc_level_data = pd.read_csv(path_to_input_csv)
    # remove rows that are NaN for value
    gluc_level_data = gluc_level_data[pd.notnull(gluc_level_data["value"])]
    #----------------------------------------------

    #---------------conversion mmol/L to mg/dL-----------------
    glu = convert_glucose(gluc_level_data)
    #----------------------------------------------------------

    #--------Save month, day, weekday, hour, minutes---------------
    timestamp = gluc_level_data.loc[:, 'time']
    saved_index = timestamp.index # save the index from this dataframe as variable index

    month_list, day_list, weekday_list, hour_list, minutes_list = divide_timestamp(timestamp)

    #convert the lists to dataframes while ensuring the index corresponds to the other dataframes
    monthdf = pd.DataFrame(np.array(month_list), index=saved_index)
    daydf = pd.DataFrame(np.array(day_list), index=saved_index)
    weekdaydf = pd.DataFrame(np.array(weekday_list), index=saved_index)
    hourdf = pd.DataFrame(np.array(hour_list), index=saved_index)
    minutesdf = pd.DataFrame(np.array(minutes_list), index=saved_index)
    #--------------------------------------------------------------

    #---------BOLUS OUTPUT---------------------------
    path_to_care_link = os.path.join(os.getcwd(), "csvData", "csvInData")
    bolus_carb_csv = pd.read_csv(os.path.join(path_to_care_link, care_link_file), skiprows=6)

    bolus = bolus_carb_csv.loc[:, 'Bolus Volume Delivered (U)']
    date = bolus_carb_csv.loc[:, 'Date']
    time = bolus_carb_csv.loc[:, 'Time']
    carb = bolus_carb_csv.loc[:, 'BWZ Carb Input (grams)']
    bolus_carb_data = pd.concat([date, time, bolus, carb], axis=1, ignore_index=True)

    #remove column if NaN value in both columns 2&3
    bolus_carb_data = bolus_carb_data.dropna(subset=[2, 3], how='all')
    #get rid of last header row
    bolus_carb_data = bolus_carb_data.drop(bolus_carb_data.index[len(bolus_carb_data)-1])
    bolus_carb_data.columns = ["Date", "Time", "Bolus (U)", "Carb Input (grams)"]
    #-------------------------------------------------------------------------

    #--------Save month, day, weekday, hour, minutes---------------

    month_list_b = []
    day_list_b = []
    hour_list_b = []
    minutes_list_b = []

    date = bolus_carb_data.loc[:, 'Date']
    time = bolus_carb_data.loc[:, 'Time']

    index_bolus = date.index # save the index from this dataframe as variable index

    day_str = date.astype(str).values.tolist()
    time_str_b = time.astype(str).values.tolist()
    for j in time_str_b:
        time_whole = datetime.strptime(j, '%H:%M:%S')
        #for months
        hour_list_b.append(time_whole.hour)
        #for days
        minutes_list_b.append(time_whole.minute)
    for k in day_str:
        date_whole = datetime.strptime(k, '%Y/%m/%d')
        #for hours
        month_list_b.append(date_whole.month)
        #for minutes
        day_list_b.append(date_whole.day)

    #convert the lists to dataframes while ensuring the index corresponds to the other dataframes
    monthdf_bolus = pd.DataFrame(np.array(month_list_b), index=index_bolus)
    daydf_bolus = pd.DataFrame(np.array(day_list_b), index=index_bolus)
    hourdf_bolus = pd.DataFrame(np.array(hour_list_b), index=index_bolus)
    minutesdf_bolus = pd.DataFrame(np.array(minutes_list_b), index=index_bolus)

    #concatenate all of these
    bolus_carb_final = pd.concat([bolus_carb_data, monthdf_bolus, daydf_bolus, hourdf_bolus, minutesdf_bolus], axis=1, ignore_index=True)
    bolus_carb_final.columns = ["Date", "Time", "Bolus (U)", "Carb Input (grams)", "Month", "Day", "Hour", "Minutes"]

    #--------------------------------------------------------------

    #--------Concatenate all of the dataframes into one dataframe----------------------------
    final = pd.concat([timestamp, glu, monthdf, daydf, weekdaydf, hourdf, minutesdf], axis=1, ignore_index=True) #concatenate the dataframe together
    #give columns names
    final.columns = ["TimeStamp", "Glucose (mg/dL)", "Month", "Day", "Weekday", "Hour", "Minutes"]
    #----------------------------------------------------------------------------------------

    #MERGE MEDTRONIC DATA WITH DEXCOM
    #----------------------------------------------------------------------------------------
    #make dataframe of NaN filled bolus and carb columns with indexes matching tidepool
    bolus_carbdf = pd.DataFrame(np.nan, index=saved_index, columns=["Bolus (U)", "Carb Input (grams)"])

    #match up the bolus insulin & carb intake from one csv
    for index_med, row_med in bolus_carb_final.iterrows(): #go through Medtronic Data
        mins_med = getattr(row_med, "Minutes")
        hrs_med = getattr(row_med, "Hour")
        day_med = getattr(row_med, "Day")
        month_med = getattr(row_med, "Month")
        bolus_med = getattr(row_med, "Bolus (U)")
        carb_med = getattr(row_med, "Carb Input (grams)")
        cur_smalls = -1
        got_one = False

        for index_tide, row_tide in final.iterrows():     #go through Tidepool Data
            mins_tide = getattr(row_tide, "Minutes")
            hrs_tide = getattr(row_tide, "Hour")
            day_tide = getattr(row_tide, "Day")
            month_tide = getattr(row_tide, "Month")
            #find closest time in Tidepool data to Medtronic data
            if month_tide == month_med and day_tide == day_med and hrs_tide == hrs_med:
                #time difference of medtronic time minux tidepool time
                dif_time = mins_med - mins_tide
                if (dif_time) <= 5:
                    cur_smalls = index_tide
                if got_one:
                    break #get out of this inner loop as we found the time we wanted for this data
                if (dif_time) <= 5:
                    got_one = True

        #add bolus & carb info to bolusCarbdf
        if cur_smalls != -1:
            if not math.isnan(float(carb_med)):
                bolus_carbdf.loc[cur_smalls, 'Carb Input (grams)'] = carb_med
            if not math.isnan(float(bolus_med)):
                bolus_carbdf.loc[cur_smalls, 'Bolus (U)'] = bolus_med
  
    #--------Concatenate all of the bolusCarbdf dataframe with final dataframe---------------
    #concatenate the dataframes together
    almost_final = pd.concat([timestamp, glu, monthdf, daydf, weekdaydf, hourdf,
                              minutesdf, bolus_carbdf], axis=1, ignore_index=True)

    #give columns names
    almost_final.columns = ["TimeStamp", "Glucose (mg/dL)", "Month",
                            "Day", "Weekday", "Hour", "Minutes", "Bolus (U)", 
                            "Carb Input (grams)"]
    #----------------------------------------------------------------------------------------


    #----------------------------------------------------------------------------------------
    #create initial csv OUTPUT
    path_base_name = os.path.basename(path_to_input_csv)
    output_file_name = "OUTPUT_" + path_base_name
    path_to_out_csv = os.path.join(os.getcwd(), "csvData", "csvOutData")
    output_file_path = os.path.join(path_to_out_csv, output_file_name)
    almost_final.to_csv(output_file_path)      # return dataframes as a csv
    #----------------------------------------------------------------------------------------

    #----------------------------------------------------------------------------------------
    basal_sens_ratio_data = pd.read_csv(output_file_path)

    basal_list = []
    insulin_sens_list = []
    carb_ratio_list = []

    for index, row in basal_sens_ratio_data.iterrows():
        #for basal list
        if row['Hour'] >= 0 and row['Hour'] < 3:
            if row['Hour'] == 2 and row['Minutes'] < 30:
                basal_list.append(BASAL["0"])
            elif row['Hour'] == 2 and row['Minutes'] >= 30:
                basal_list.append(BASAL["2"])
            else:
                basal_list.append(BASAL["0"])
        elif row['Hour'] >= 3 and row['Hour'] < 4:
            basal_list.append(BASAL["2"])
        elif row['Hour'] >= 4 and row['Hour'] < 8:
            basal_list.append(BASAL["4"])
        elif row['Hour'] >= 8 and row['Hour'] < 12:
            basal_list.append(BASAL["8"])
        elif row['Hour'] >= 12 and row['Hour'] < 14:
            basal_list.append(BASAL["12"])
        elif row['Hour'] >= 14 and row['Hour'] < 19:
            basal_list.append(BASAL["14"])
        elif row['Hour'] >= 19 and row['Hour'] < 24:
            basal_list.append(BASAL["19"])

        #for insulin sensitivity list
        if row['Hour'] >= 0 and row['Hour'] < 6:
            insulin_sens_list.append(SENSITIVITY["0"])
        elif row['Hour'] >= 6 and row['Hour'] < 9:
            insulin_sens_list.append(SENSITIVITY["6"])
        elif row['Hour'] >= 9 and row['Hour'] < 12:
            insulin_sens_list.append(SENSITIVITY["9"])
        elif row['Hour'] >= 12 and row['Hour'] < 15:
            insulin_sens_list.append(SENSITIVITY["12"])
        elif row['Hour'] >= 15 and row['Hour'] < 24:
            insulin_sens_list.append(SENSITIVITY["15"])

        #for carb ratio list
        if row['Hour'] >= 0 and row['Hour'] < 6:
            carb_ratio_list.append(CARB_RATIO["0"])
        elif row['Hour'] >= 6 and row['Hour'] < 12:
            if row['Hour'] == 11 and row['Minutes'] < 30:
                carb_ratio_list.append(CARB_RATIO["6"])
            elif row['Hour'] == 11 and row['Minutes'] >= 30:
                carb_ratio_list.append(CARB_RATIO["11"])
            else:
                carb_ratio_list.append(CARB_RATIO["6"])
        elif row['Hour'] >= 12 and row['Hour'] < 14:
            carb_ratio_list.append(CARB_RATIO["11"])
        elif row['Hour'] >= 14 and row['Hour'] < 18:
            carb_ratio_list.append(CARB_RATIO["14"])
        elif row['Hour'] >= 18 and row['Hour'] < 21:
            carb_ratio_list.append(CARB_RATIO["18"])
        elif row['Hour'] >= 21 and row['Hour'] < 24:
            carb_ratio_list.append(CARB_RATIO["21"])

    #create dataframes from lists
    basaldf = pd.DataFrame(np.array(basal_list), index=saved_index) #like above set index to index
    insulindf = pd.DataFrame(np.array(insulin_sens_list), index=saved_index) #like above set index to index
    carbdf = pd.DataFrame(np.array(carb_ratio_list), index=saved_index) #like above set index to index
    #----------------------------------------------------------------------------------------

    
    #--------Concatenate the new dataframes into final dataframe----------------------------
    real_final = pd.concat([timestamp, glu, basaldf, insulindf, carbdf, monthdf, daydf, weekdaydf, hourdf, minutesdf, bolus_carbdf], axis=1, ignore_index=True) #concatenate the dataframe together
    #----------------------------------------------------------------------------------------

    #give columns names
    real_final.columns = ["TimeStamp", "Glucose (mg/dL)", "Basal Insulin (U/hr)", 
    "Insulin Sensitivity (mg/dL/U)","Carb Ratio (g/U)", "Month", "Day", 
    "Weekday", "Hour", "Minutes", "Bolus (U)", "Carb Input (grams)"]

    last_time = ""
    for index, row in real_final.iterrows():
        if row['TimeStamp'] == last_time:
            real_final = real_final.drop(index, axis=0)
        last_time = row['TimeStamp']
    '''
    #create final csv OUTPUT (rewrites the earlier csv file)
    header = ["TimeStamp", "Glucose (mg/dL)", "Basal Insulin (U/hr)","Insulin Sensitivity (mg/dL/U)","Carb Ratio (g/U)", "Month", "Day","Weekday", "Hour","Minutes","Bolus (U)", "Carb Input (grams)"]
    '''
    real_final = real_final.reindex(index=real_final.index[::-1])
    real_final.to_csv(output_file_path)        # return dataframes as a csv


def main():
    """main"""

    create_dataframe()

if __name__ == '__main__':
    main()
