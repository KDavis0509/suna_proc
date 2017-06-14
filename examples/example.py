# -*- coding: utf-8 -*-
"""
:DESCRIPTION:internally logged daily suna file processor
This example script processes SUNA version 2 full_ascii log data file located in a
directory

:REQUIRES: suna_proc

:TODO:

:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.2

"""
# =============================================================================
# IMPORT STATEMENTS
# =============================================================================
import os
import matplotlib.pyplot as plt 
from suna_process import process, get_tz_name
# =============================================================================
# MAIN FUNCTION
# =============================================================================


def main(file_direc, fmatch, suna_version, interval,
         UTC_tz_offset, datetime_name, plot=True):
    low_limit = 0.1
    high_limit = 58
    # set the outfile name based on the name of the file directory
    no3_mad_raw = process(file_direc, fmatch, suna_version, interval,
                          UTC_tz_offset, datetime_name)
    # filter out NO3 conc data when sensor in air (typically, NO3 < 0.1 mg/L),
    # there is an error (NO3 = -1), or concentration exceeds concentration
    # limit
    no3_mad = no3_mad_raw[(no3_mad_raw > low_limit) & (no3_mad_raw < high_limit)]
    # write mad processed nitrate concentration output to csv file
    no3_mad.to_csv(os.path.join(file_direc, 'SUNA_NO3_mad.csv'))

    # plot the raw and mad processed nitrate concentration timeseries data
    if plot:
        plt.figure()
        no3_mad_raw.plot(marker='*', label='raw', legend=True)
        ax2 = no3_mad.plot(marker='o', label='mad_screened', legend=True)
        ax2.set_ylabel('NO$_3$ (mg/L-N)')
        plt.show()

# %%
if __name__ == "__main__":
    # ============================BEGIN USER VARIABLES=========================
    # Place files in 'data' folder
    cwd = os.getcwd()
    file_direc = os.path.join(cwd, 'data')
    suna_version = 2
    # define sampling interval
    interval = 15  # in minutes
    # define timezone offset relative to UTC, in hours
    UTC_tz_offset = -5
    # name datetime index based on time zone
    datetime_name = get_tz_name(UTC_tz_offset)
#    datetime_name = "Datetime (EST)"
    # ==============================END USER VARIABLES=========================
    fmatch = 'D2*.csv'  # match and process all daily csv files
    # call main routine to process and plot data
    main(file_direc, fmatch, suna_version, interval,
         UTC_tz_offset, datetime_name)
