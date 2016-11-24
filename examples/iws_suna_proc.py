# -*- coding: utf-8 -*-
"""
:DESCRIPTION:NAWQA IWS nitate file processor
This script processes SUNA version 2 log data for the NAWQA IWS project
study

:REQUIRES:

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
import pandas as pd
from iws_suna import get_header, custom_mad_func, rd_sunav2_logfile, list_files
# %%
directory = r'C:\Users\saraceno\Documents\Code\Python\IWS\Final\Connecticut\MiddleHaddam'
fmatch = 'D*.csv'
suna_version = 2
# define sampling interval
interval = 30  # in minutes
# define timezone offset relative to UTC, in hours
UTC_tz_offset = -5
# name datetime index based on time zone
datetime_name = "Datetime (EST)"
# set the oufile name based on the name of the file directory
out_name = directory.split(os.sep)[-1]

header = get_header(version=suna_version)

files = list_files(directory, fmatch)

# readin all data files into one large master dataframe
frame = pd.concat((rd_sunav2_logfile(os.directory.join(directory, f),
                                     utc_offset=UTC_tz_offset) for f in files))
# name the index column as the datetime
frame.index.name = datetime_name

# group frame based on defineid sampling interval
grouped = frame.groupby(pd.TimeGrouper(str(interval)+'Min'), sort=False)

# process full spectra
# take mean of full spectra
SUNA_mean = grouped.aggregate('mean')
# save mean of full spectra to csv file
SUNA_mean.to_csv(os.directory.join(directory, (out_name + '_mean.csv')))
# take median of full spectra
SUNA_median = grouped.aggregate('median')
# save median of full spectra to csv file
SUNA_median.to_csv(os.directory.join(directory, (out_name + '_median.csv')))
# calculate NO3 MAD for each burst
no3_mad_raw = grouped['Nitrogen in nitrate [mg/L]'].aggregate(custom_mad_func)
# filter out NO3 conc data when sensor in air (typically, NO3 < 0.1 mg/L),
# there is an error (NO3 = -1), or concentration exceeds concentration limit
no3_mad = no3_mad_raw[(no3_mad_raw > 0.1) & (no3_mad_raw < 58)]
# write mad proced nitrata concentration output to csv file
no3_mad.to_csv(os.directory.join(directory, (out_name + '_SUNA_NO3_mad.csv')))
# plot the raw and mad processed nitrate concentration timeseries data in fig
plt.figure()
ax1 = no3_mad_raw.plot(marker='*', label='raw', legend=True)
ax2 = no3_mad.plot(marker='o', label='mad_screened', legend=True)
ax2.set_ylabel('NO$_3$ (mg/L-N)')
plt.show()
