# -*- coding: utf-8 -*-
"""
:DESCRIPTION:Functions to process Satlantic SUNA version 2 log data files
study

:REQUIRES:  numpy, statsmodels, pandas

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
import datetime
import glob
import os
import numpy as np
import numpy.ma as ma
import pandas as pd
import statsmodels.robust.scale as smc
# =============================================================================
# METHODS
# =============================================================================


def get_header(version=2):
    """This function assigns the SUNA file header based on suna version"""
    if version == 1:
        header = ['INSTRUMENT', 'TIMEFIELD', 'NITRATE_UM', 'NITRATE_MG',
                  'ERROR', 'T_LAMP', 'T_SPEC', 'LAMP_TIME', 'HUMIDITY',
                  'VOLT_12', 'VOLT_REG', 'VOLT_MAIN', 'SPEC_AVG',
                  'DARK_AVG', 'CHECK SUM']
        for i in range(1, 227):  # write the channel header
            col = "CHANNEL(" + str(i) + ")"
            header.insert(13+i, col)
    elif version == 2:
        header = ['Header and Serial Number', 'Date year and day-of-year',
                  'Time, hours of day', 'Nitrate concentration [uM]',
                  'Nitrogen in nitrate [mg/L]', 'Absorbance at 254 nm',
                  'Absorbance at 350 nm', 'Bromide trace [mg/L]',
                  'Spectrum average', 'Dark value used for fit',
                  'Integration time factor', 'Internal temperature [C]',
                  'Spectrometer temperature [C]', 'Lamp temperature [C]',
                  'Cumulative lamp on-time [s]', 'Relative Humidity [%]',
                  'Main Voltage [V]', 'Lamp Voltage [V]',
                  'Internal Voltage [V]',
                  'Main current [mA]', 'Fit Aux 1', 'Fit Aux 2', 'Fit Base 1',
                  'Fit Base 2', 'Fit RMSE', 'CTD Time [seconds since 1970]',
                  'CTD Salinity [PSU]', 'CTD Temperature [C]',
                  'CTD Pressure [dBar]', 'Check Sum']
        for i in range(1, 257):  # write the channel header
            col = "Spectrum channel " + str(i)
            header.insert(10 + i, col)
    return header


def custom_mad_func(array_like, criteria=2.5, **kwargs):
    """This function performs a mad calculation on array of data
    Returns the median of MAD data"""
    if kwargs:
        criteria = kwargs['criteria']
        ul = kwargs['ul']
        ll = kwargs['ll']
    else:
        ul = 58
        ll = 0.001
    # prescreen burst data for outliers
    array_like = ma.compressed(ma.masked_outside(array_like, ll, ul))
    MAD = smc.mad(array_like)
    k = (MAD*criteria)
    M = np.nanmedian(array_like)
    high = M + k
    low = M - k
    b = ma.masked_outside(array_like, high, low)
    c = ma.compressed(b)
    return np.nanmedian(c)


#def read_log_file(textfile, kind='daily', utc_offset=-8):
#    """Read SUNA v2 daily log file and return a dataframe"""
#    if kind is 'daily':
#        header = get_header(version=2)
#        dcol = header[1]
#        tcol = header[2]
#        # read in csvfile to a dataframe
#        df = pd.read_csv(textfile, header=None, skiprows=14)
#        # ditch frame header column, we crete our own
#        df.drop(df.columns[0], axis=1, inplace=True)
#        df.columns = header[1:]
#        # remove rows with nonsensical date year and doy
#        df = df[df[dcol] != 0]
#        # remove rows with nonsensical hod
#        df = df[(df[tcol] < 24) & (df[tcol] > 0)]
#        df.index = df.apply(lambda row: date_time(row[dcol],
#                                                  row[tcol]), axis=1)
#        df.index = pd.DatetimeIndex(df.index) + pd.DateOffset(hours=utc_offset)
#        return df


def rd_sunav2_logfile(textfile, utc_offset=-8):
    """Read internally logged SUNA v2 file and return a dataframe or array"""
    try:
        header = get_header(version=2)
        dcol = header[1]
        tcol = header[2]
        # read in csvfile to a dataframe, skipping bad lines
        df = pd.read_csv(textfile, header=None, skiprows=14,
                         error_bad_lines=False)
        # ditch frame header column
        df.drop(df.columns[0], axis=1, inplace=True)
        print "Processing file:", textfile[-12:], "please wait..."
        df.columns = header[1:]
        # remove rows with nonsensical date year and doy
        df = df[df[dcol] != 0]
        # remove rows with nonsensical hod
        df = df[(df[tcol] < 24) & (df[tcol] > 0)]
        df.index = df.apply(lambda row: date_time(row[dcol],
                                                  row[tcol]), axis=1)
        df.index = pd.DatetimeIndex(df.index) + pd.DateOffset(hours=utc_offset)
        return df
    except:
        print "Could not process file:", textfile[-12:], "skipping..."


def list_files(path, fmatch):
    files = []
    for name in glob.glob(os.path.join(path, fmatch)):
        if os.path.isfile(os.path.join(path, name)):
            files.append(name)
    return files


def date_time(dates, times):
    """this function converts the date and time columsn of a suna data frame
    to a python date time object"""
    #TODO/HACK: setting date to Jan 1 2000 when date is 0
    if dates != 0:
        date = date_convertor(dates)
    else:
        date = datetime.datetime(2000, 1, 1)
    time = time_convertor(times)
    dt = datetime.datetime(date.year, date.month, date.day,
                           time.hour, time.minute, time.second)
    return dt


def date_convertor(dates):
    """converts the year and julian day to MM-DD-YYYY"""
    date = str(int(dates))  # redundant
    day = int(date[-3:]) - 1
    year = int(date[:4])
    date = datetime.datetime(year, 1, 1,) + datetime.timedelta(day)
    return date


def time_convertor(time_hours):
    """converts the decimal hour to a HH:MM:SS format"""
    time_minutes = time_hours * 60
    time_seconds = time_minutes * 60
    hours_part = np.floor(time_hours)
    minutes_part = np.floor(time_minutes % 60)
    seconds_part = np.floor(time_seconds % 60)
    time_out = datetime.time(int(hours_part), int(minutes_part),
                             int(seconds_part))
    return time_out
