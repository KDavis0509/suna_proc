# -*- coding: utf-8 -*-
"""
:DESCRIPTION:NAWQA IWS nitate file processor
This script processes SUNA version 2 full_ascii log data file located in a
directory

:REQUIRES: matplotlib, os, suna_proc

:TODO:

:AUTHOR: John Franco Saraceno
:ORGANIZATION: U.S. Geological Survey, United States Department of Interior
:CONTACT: saraceno@usgs.gov
:VERSION: 0.1
Wed Aug 10 14:45:07 2016
"""
# =============================================================================
# IMPORT STATEMENTS
# =============================================================================
import os
import matplotlib.pyplot as plt
from suna_proc import process
# =============================================================================
# MAIN FUNCTION
# =============================================================================


def main(file_direc, fmatch, suna_version, interval,
         UTC_tz_offset, datetime_name):
    # set the ouTfile name based on the name of the file directory
    no3_mad_raw = process(file_direc, fmatch, suna_version, interval,
                          UTC_tz_offset, datetime_name)
    # filter out NO3 conc data when sensor in air (typically, NO3 < 0.1 mg/L),
    # there is an error (NO3 = -1), or concentration exceeds concentration
    # limit
    no3_mad = no3_mad_raw[(no3_mad_raw > 0.1) & (no3_mad_raw < 58)]
    # write mad proced nitrata concentration output to csv file
    no3_mad.to_csv(os.path.join(file_direc, (out_name + '_SUNA_NO3_mad.csv')))

    # plot the raw and mad processed nitrate concentration timeseries data
    plt.figure()
    no3_mad_raw.plot(marker='*', label='raw', legend=True)
    ax2 = no3_mad.plot(marker='o', label='mad_screened', legend=True)
    ax2.set_ylabel('NO$_3$ (mg/L-N)')
    plt.show()

# %%
if __name__ == "__main__":
    # ============================BEGIN USER VARIABLES=========================
    # DEFINE FILE CONTAINING DIRECTORY
    file_direc = r'C:\Users\saraceno\Documents\Code\Python\repos\suna_proc\examples\example_data'
    fmatch = 'D*.csv'  # match and process all daily log files
    out_name = file_direc.split(os.sep)[-1]
    suna_version = 2
    # define sampling interval
    interval = 30  # in minutes
    # define timezone offset relative to UTC, in hours
    UTC_tz_offset = -5
    # name datetime index based on time zone
    datetime_name = "Datetime (EST)"
    # ==============================END USER VARIABLES=========================
    # call main routine to process and plot data
    main(file_direc, fmatch, suna_version, interval,
         UTC_tz_offset, datetime_name)
