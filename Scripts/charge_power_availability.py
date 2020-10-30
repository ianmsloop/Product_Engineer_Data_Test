import pandas as pd
import numpy as np
import sys
import os
from matplotlib import pyplot as plt

project_dir = os.getcwd().split('Scripts')[0]
sys.path.append(project_dir) # add Product_Engineer_Data_Test to path

'''PROJECT NOTES
Variable Naming:
PWF = PW_FullPackEnergyAvailable
PWE = PW_EnergyRemaining
PWA = PW_AvailableChargePower
QI = Quality Index (0-100%) measure of how much of much data is available in a month
CPA = charge power availability

Conversions:
30s = 30000ms
60s = 60000ms
300,000 ms = 5min

Description:
There is much missing data for the batteries during certain months, as well as gaps in between sections
of the present data. To quantify the confidence in CPA, I have defined a QI to accompany it. This is the
% time that data was sampled during all of the possible 5min sampling periods in a month.

Sampling rate is constant for all data streams (5 mins) though there are gaps in the data, but PW_EnergyRemaining 
and PW_AvailableChargePower are offset by 30s and 60s from PW_FullPackEnergyAvailable, respectively
'''

def days_in_month(month):
    """Determine number of days in a month based on month number
        :arg month (int): month of the year 1-12

    :returns days (int): number of days (28,29,30,31)
    TODO: add leap year functionality, not currently needed since we are dealing with data in months 8-12
    """
    if month < 8:
        if month%2 == 1:
            return 31
        else:
            return 30
    else:
        if month%2 == 1:
            return 30
        else:
            return 31


# Set up results dataframe, columns are month numbers, index are different metrics
monthly_avg_cpa = pd.DataFrame(columns=['8','9','10','11','12'], index=['battery_1_CPA_w_full','battery_1_CPA',
                                                                    'battery_2_CPA','battery_3_CPA','battery_4_CPA',
                                                                    'battery_5_CPA', 'battery_1_QI','battery_2_QI',
                                                                    'battery_3_QI','battery_4_QI','battery_5_QI'])
# loop through and read from 001.csv to 005.csv
for i in range(1, 6):
    filename = '00' + str(i) + '.csv'
    battery_data = pd.read_csv(project_dir + 'Data test\\TEFA-interview-data-set\\' + filename)
    battery_data.index = pd.to_datetime(battery_data['timestamp'], unit='ms')

    # Split data into each metric
    FullPackEnergyAvailable = battery_data.iloc[np.where(battery_data['signal_name'] == 'PW_FullPackEnergyAvailable')]
    EnergyRemaining = battery_data.iloc[np.where(battery_data['signal_name'] == 'PW_EnergyRemaining')]
    AvailableChargePower = battery_data.iloc[np.where(battery_data['signal_name'] == 'PW_AvailableChargePower')]

    # Interpolate and adjust timestamps to all match those of FullPackEnergyAvailable
    EnergyRemaining.loc[:,'signal_value'] = np.interp(EnergyRemaining.loc[:,'timestamp'].values - 30000,
                                                      EnergyRemaining.loc[:,'timestamp'].values,
                                                      EnergyRemaining.loc[:,'signal_value'].values)
    EnergyRemaining.loc[:,'timestamp'] = EnergyRemaining.loc[:,'timestamp'].values - 30000
    EnergyRemaining.index = pd.to_datetime(EnergyRemaining.loc[:,'timestamp'], unit='ms')
    AvailableChargePower.loc[:,'signal_value'] = np.interp(AvailableChargePower.loc[:,'timestamp'].values - 60000,
                                                           AvailableChargePower.loc[:,'timestamp'].values,
                                                           AvailableChargePower.loc[:,'signal_value'].values)
    AvailableChargePower.loc[:,'timestamp'] = AvailableChargePower.loc[:,'timestamp'].values - 60000
    AvailableChargePower.index = pd.to_datetime(AvailableChargePower.loc[:,'timestamp'], unit='ms')

    for month in monthly_avg_cpa.columns:
        # Grab data for the current month
        PWF = FullPackEnergyAvailable.iloc[np.where(np.array(FullPackEnergyAvailable.index.month) == int(month))[0]].sort_index()
        PWE = EnergyRemaining.iloc[np.where(np.array(EnergyRemaining.index.month) == int(month))[0]].sort_index()
        PWA = AvailableChargePower.iloc[np.where(np.array(AvailableChargePower.index.month) == int(month))[0]].sort_index()

        # calculate % time battery 1 is available, including full battery
        if i == 1:
            available_w_full_battery = PWA.iloc[np.where(PWA['signal_value'] >= 3300)[0]]
            monthly_avg_cpa.loc['battery_1_CPA_w_full'][month] = len(available_w_full_battery)/len(PWA['signal_value'])*100

        # calculate % time battery 1 is available, excluding when battery is > 90 % charged
        excluding_full_battery = PWA.iloc[np.where(PWE['signal_value'] / PWF['signal_value'] <= 0.9)[0]]
        cpa_battery_data = excluding_full_battery.iloc[np.where(excluding_full_battery['signal_value'] >= 3300)[0]]
        if len(excluding_full_battery) == 0: # Data not present for some months
            monthly_avg_cpa.loc['battery_' + str(i) + '_CPA'][month] = 0
            monthly_avg_cpa.loc['battery_' + str(i) + '_QI'][month] = 0
        else:
            monthly_avg_cpa.loc['battery_' + str(i) + '_CPA'][month] = len(cpa_battery_data) / len(excluding_full_battery)*100
            # convert days to # of 5min intervals, then to % completeness
            monthly_avg_cpa.loc['battery_' + str(i) + '_QI'][month] = len(PWA) / (days_in_month(int(month))*1440/5)*100
# Save Data to a .csv
monthly_avg_cpa.to_csv(project_dir + 'Plots\Results.csv')

# plot results for Exercise 1
fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
ax1.set_title('Average Charge Power Availability for Battery 1 including Full Battery')
ax1.set_ylabel('% Time Available')
ax1.bar(monthly_avg_cpa.columns, monthly_avg_cpa.loc['battery_1_CPA_w_full'])
ax1.grid(True)
ax1.set_yticks(np.arange(0,110,10))
ax1.set_yticklabels(np.arange(0,110,10))
ax2.set_title('Quality Index based on Completeness of Data')
ax2.set_xlabel('Month Number')
ax2.set_ylabel('% Complete Dataset')
ax2.bar(monthly_avg_cpa.columns, monthly_avg_cpa.loc['battery_1_QI'])
ax2.grid(True)
ax2.set_yticks(np.arange(0,110,10))
ax2.set_yticklabels(np.arange(0,110,10))
fig.savefig(project_dir + 'Plots\\Battery1CPAwFullBattery.jpg')

# plot results for Exercise 2
fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
ax1.set_title('Average Charge Power Availability for Battery 1 excluding Full Battery')
ax1.set_ylabel('% Time Available')
ax1.bar(monthly_avg_cpa.columns, monthly_avg_cpa.loc['battery_1_CPA'])
ax1.grid(True)
ax1.set_yticks(np.arange(0,110,10))
ax1.set_yticklabels(np.arange(0,110,10))
ax2.set_title('Quality Index based on Completeness of Data')
ax2.set_xlabel('Month Number')
ax2.set_ylabel('% Complete Dataset')
ax2.bar(monthly_avg_cpa.columns, monthly_avg_cpa.loc['battery_1_QI'])
ax2.grid(True)
ax2.set_yticks(np.arange(0,110,10))
ax2.set_yticklabels(np.arange(0,110,10))
fig.savefig(project_dir + 'Plots\\Battery1CPA.jpg')

# plot results for Exercise 3
fig, (ax1, ax2) = plt.subplots(2,1, sharex=True)
ax1.set_title('Charge Power Availability for Batteries 1-5 excluding Full Battery')
ax1.set_ylabel('% Time Available')
x = np.arange(len(monthly_avg_cpa.columns))
spacing = 0.1
width = 0.1
ax1.bar(x, monthly_avg_cpa.loc['battery_1_CPA'], color='g', width=width)
ax1.bar(x + spacing, monthly_avg_cpa.loc['battery_2_CPA'], color='b', width=width)
ax1.bar(x + spacing*2, monthly_avg_cpa.loc['battery_3_CPA'], color='y', width=width)
ax1.bar(x + spacing*3, monthly_avg_cpa.loc['battery_4_CPA'], color='k', width=width)
ax1.bar(x + spacing*4, monthly_avg_cpa.loc['battery_5_CPA'], color='r', width=width)
ax1.grid(True)
ax1.set_yticks(np.arange(0,110,10))
ax1.set_yticklabels(np.arange(0,110,10))
ax2.set_title('Quality Index based on Completeness of Data')
ax2.set_xlabel('Month Number')
ax2.set_ylabel('% Complete Dataset')
ax2.bar(x, monthly_avg_cpa.loc['battery_1_QI'], color='g', width=width)
ax2.bar(x + spacing, monthly_avg_cpa.loc['battery_2_QI'], color='b', width=width)
ax2.bar(x + spacing*2, monthly_avg_cpa.loc['battery_3_QI'], color='y', width=width)
ax2.bar(x + spacing*3, monthly_avg_cpa.loc['battery_4_QI'], color='k', width=width)
ax2.bar(x + spacing*4, monthly_avg_cpa.loc['battery_5_QI'], color='r', width=width)
ax2.grid(True)
ax2.legend(['Battery 1','Battery 2','Battery 3','Battery 4','Battery 5'], loc='best')
ax2.set_yticks(np.arange(0,110,10))
ax2.set_yticklabels(np.arange(0,110,10))
ax2.set_xticks(np.arange(0,len(monthly_avg_cpa.columns)))
ax2.set_xticklabels(monthly_avg_cpa.columns)
fig.savefig(project_dir + 'Plots\\Battery1thru5CPA.jpg')


