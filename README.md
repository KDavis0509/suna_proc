# suna_proc : a python package to process Satlantic SUNA data 

suna_proc is a python package that reads SUNA data (log files) into a pandas timeseries dataframe.
Burst data is grouped by time, processed for outlier detection using the median absolute deviation, 
converted to a pandas dataframe and saved to a csv file.

See http://satlantic.com/suna for more information on the Satlantic SUNA v2.

See examples for package usage

Requirements:
--------------

### Required packages: ###

* datetime
* glob
* matplotlib
* numpy
* pandas
* statsmodels

Example: Process a directory of daily log files and save as a pandas dataframe
-------------------------------------------------------------------------------
:::python

	import os
	import matplotlib.pyplot as plt
	from suna_proc import process

	def main(file_direc, fmatch, suna_version, interval,
			 UTC_tz_offset, datetime_name):
		no3_mad_raw = process(file_direc, fmatch, suna_version, interval,
							  UTC_tz_offset, datetime_name)
		# filter out nitrate conc data when sensor in air (typically, NO3 < 0.1 mg/L),
		# there is an error (NO3 = -1), or concentration exceeds concentration
		# limit
		no3_mad = no3_mad_raw[(no3_mad_raw > 0.1) & (no3_mad_raw < 58)]
		# write mad proced nitrata concentration output to csv file
		no3_mad.to_csv(os.path.join(file_direc, (out_name + '_SUNA_NO3_mad.csv')))

		# plot the raw and mad processed nitrate concentration time series data
		plt.figure()
		no3_mad_raw.plot(marker='*', label='raw', legend=True)
		ax2 = no3_mad.plot(marker='o', label='mad_screened', legend=True)
		ax2.set_ylabel('NO$_3$ (mg/L-N)')
		plt.show()


	if __name__ == "__main__":
		# ============================BEGIN USER VARIABLES=========================
		# DEFINE FILE CONTAINING DIRECTORY
		file_direc = r'C:\Users\saraceno\Documents\Code\Python\repos\suna_proc\examples\data'
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
		#call main routine to process and plot data
		main(file_direc, fmatch, suna_version, interval,
			 UTC_tz_offset, datetime_name)

Installation:
------------

Install suna_proc from the command line by following these steps:

    $ git clone https://github.com/OneGneissGuy/suna_proc.git
    $ cd suna_process
    $ python setup.py install
	
OR

Copy the [source code](https://github.com/OneGneissGuy/suna_proc/tree/master/suna_process) directly

Disclaimer:
----------

This software is preliminary or provisional and is subject to revision. It is being provided to meet the need for timely
best science. The software has not received final approval by the U.S. Geological Survey (USGS). No warranty, expressed
or implied, is made by the USGS or the U.S. Government as to the functionality of the software and related material nor
shall the fact of release constitute any such warranty. The software is provided on the condition that neither the USGS
nor the U.S. Government shall be held liable for any damages resulting from the authorized or unauthorized use of the
software.

The USGS provides no warranty, expressed or implied, as to the correctness of the furnished software or the suitability
for any purpose. The software has been tested, but as with any complex software, there could be undetected errors. Users
who find errors are requested to report them to the USGS.

References to non-USGS products, trade names, and (or) services are provided for information purposes only and do not
constitute endorsement or warranty, express or implied, by the USGS, U.S. Department of Interior, or U.S. Government, as
to their suitability, content, usefulness, functioning, completeness, or accuracy.

Although this program has been used by the USGS, no warranty, expressed or implied, is made by the USGS or the United
States Government as to the accuracy and functioning of the program and related program material nor shall the fact of
distribution constitute any such warranty, and no responsibility is assumed by the USGS in connection therewith.

This software is provided "AS IS."


Author(s):
------
John Franco Saraceno <saraceno@usgs.gov>

More information:
-----------------
* Python: https://www.python.org/
* pytest: http://pytest.org/latest/
* Sphinx: http://sphinx-doc.org/
* public domain: https://en.wikipedia.org/wiki/Public_domain
* CC0 1.0: http://creativecommons.org/publicdomain/zero/1.0/
* U.S. Geological Survey: https://www.usgs.gov/
* USGS: https://www.usgs.gov/
* U.S. Geological Survey (USGS): https://www.usgs.gov/
* United States Department of Interior: https://www.doi.gov/
* official USGS copyright policy: http://www.usgs.gov/visual-id/credit_usgs.html#copyright/
* U.S. Geological Survey (USGS) Software User Rights Notice: http://water.usgs.gov/software/help/notice/
* Python's download page: https://www.python.org/downloads/
* git: https://git-scm.com/
* Distutils: https://docs.python.org/3/library/distutils.html
* Installing Python Modules: https://docs.python.org/3.5/install/
* How Installation Works: https://docs.python.org/3.5/install/#how-installation-works
