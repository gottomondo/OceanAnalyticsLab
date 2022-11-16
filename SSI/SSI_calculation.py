#!/usr/bin/env python

import netCDF4 as nc
import numpy as np
#import ipywidgets as widgets

#Input
from SSI.SSI_iparameters import InputParametersSSI
from input.iparameters import InputParameters
from input import working_domain as wd
from log.logmng import LogMng


import math as math
import calendar
import urllib.parse
import re
import numba
from numba import jit
import xarray as xr
import matplotlib.pyplot as plt

from cartopy import config
import cartopy.crs as ccrs

from calendar import monthrange
from os.path import  isfile 
from netCDF4 import Dataset, num2date
from datetime import date, timedelta, datetime


# functions
def diff_month(d1, d2):
    return (d1.year - d2.year) * 12 + d1.month - d2.month + 1

def clean_filename(name):
        forbidden_chars = ' "*\\/\'|?:<>'
        filename = ''.join([x if x not in forbidden_chars else '_' for x in name])
        if len(filename) >= 176:
            filename = filename[:170] + '...'
        return filename 


# Iterate over every hour of the day and calculate the daily SSI index for each lat/lon grid cell and add the daily SSI to the timestep (period)
@jit()
def calcSSIDayStep(SSIdaily, SSIoutput, SSImax, SSIrate, SSIndays, windspeedPerDay, SSIperc, SSIwindspeed_perc, SSIwindspeed_thres, startlat, startlong, dayidx, step, deltaperiodlat ,deltaperiodlong):
    for hourofdayidx in range(24):
        for latidx in range(deltaperiodlat):
            for longidx in range(deltaperiodlong):
                #if np.isnan(windspeedPerDay[hourofdayidx,startlat+latidx, startlong+longidx]) :
                    #continue
                if SSIperc == 'ssi_percentile':
                    SSIdaily[dayidx][latidx][longidx] +=  max(0, windspeedPerDay[hourofdayidx,startlat+latidx, startlong+longidx] / SSIwindspeed_perc[latidx, longidx] - 1) ** 3                
                elif SSIperc == 'ssi_percentile_min':
                    SSIdaily[dayidx][latidx][longidx] +=  max(0, windspeedPerDay[hourofdayidx,startlat+latidx, startlong+longidx] / max(SSIwindspeed_perc[latidx, longidx], SSIwindspeed_thres) - 1) ** 3                                   
                else:
                    SSIdaily[dayidx][latidx][longidx] +=  max(0, windspeedPerDay[hourofdayidx,startlat+latidx, startlong+longidx] / SSIwindspeed_thres - 1) ** 3                
                    
    #Add day to timestep               
    for latidx in range(deltaperiodlat):
        for longidx in range(deltaperiodlong):                
            SSIoutput[step][latidx][longidx] += SSIdaily[dayidx][latidx][longidx]
            if SSIdaily[dayidx][latidx][longidx] > 0 :
                SSIndays[step][latidx][longidx] += 1
            if SSImax[step][latidx][longidx] < SSIdaily[dayidx][latidx][longidx] :
                SSImax[step][latidx][longidx] = SSIdaily[dayidx][latidx][longidx]
            if SSIndays[step][latidx][longidx] > 0 :
                SSIrate[step][latidx][longidx] = SSIoutput[step][latidx][longidx] / SSIndays[step][latidx][longidx]


# Iterate over each lat/lon grid cell tot calculate the Area numbers of a timestep
@jit()

def calcSSIAreaStep(SSIAreaoutput, SSIAreamax, SSIArearate, SSIAreandays,SSIoutput, SSImax, SSIrate, SSIndays, step, deltaperiodlat ,deltaperiodlong):         
    for latidx in range(deltaperiodlat):
        for longidx in range(deltaperiodlong):                
            SSIAreaoutput[step] += SSIoutput[step][latidx][longidx]
            if SSIAreandays[step] < SSIndays[step][latidx][longidx] :
                SSIAreandays[step] = SSIndays[step][latidx][longidx]
            if SSIAreamax[step] < SSImax[step][latidx][longidx] :
                SSIAreamax[step] = SSImax[step][latidx][longidx]
            if SSIAreandays[step] > 0 :
                SSIArearate[step]= SSIAreaoutput[step] / SSIAreandays[step]
    


# ### SSI source data
# Next, an overview over available source data is presented.
# This comprises currently a data file that contains downloaded hourly Copernicus C3S ERA5 reanalysis data (10 m wind data above sea) for Mediterranean Sea area (0.5x0.5 deg) over the periode 1 January 1979 till 31 December 2020  (NetCDF format). 
# 
# The available source data might be extended to cover larger areas (North Sea etc.) using several data files with downloaded data or via a direct API call to C3S using WEkEO
# 

# In[2]:

def calculateSSI(input_parameters: InputParametersSSI, json_log: LogMng):

    
    # source  data (ERA5 hourly wind speeds and wind percentiles
    print("===SSI METHOD STARTED===\n")
    json_log.phase_start("Calculate SSI")
    #inputfile = 'indir/C3S_ERA5_Medsea_1979_2020_allmonths_alldays.nc'
    inputfile = "indir/" + (input_parameters.get_data_source()).replace("_STHUB", "_WIND.nc")
    
    try:
        dsInput = Dataset(inputfile)
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)

    try: 
        dsInput.isopen()  #  make sure dataset is not alread open.
    except: pass
  

    #pvaluesfile = 'indir/C3S_ERA5_Medsea_1979_2020_windspeed_P90959899.nc'
    pvaluesfile = "indir/" + (input_parameters.get_data_source()).replace("_STHUB", "_WIND_P90959899.nc")
    
    try:
        dsPVals = Dataset(pvaluesfile)
    except Exception as e: 
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)

    try: 
        dsPValsInput.isopen()  #  make sure dataset is not alread open.
    except: pass
    
    # Get a reference to the NetCDF windspeed and time variable
    windspeedVariable=dsInput['wind']
    # Get a reference to the  windspeed percentile variables
    windspeed_Pvals=dsPVals['windspeed_P90959899']

    #input time and area information
    timeVariable=dsInput['time']
    latitude=dsInput['latitude'][:]
    longitude=dsInput['longitude'][:]

    # Keep the shape of the array in variables
    nrhours = windspeedVariable.shape[0]
    nrlats  = windspeedVariable.shape[1]
    nrlongs = windspeedVariable.shape[2]

    # Calculate the number of days from the shape
    nrdays  = int(nrhours/24)

    #determine time extent
    # timeVariable.units contains "hours since yyyy-mm-dd hh:MM:ss"
    mindate_tmp = re.split(" ", timeVariable.units )
    #mindate = date.fromisoformat(mindate_tmp[2])
    mindate = datetime.strptime(mindate_tmp[2], "%Y-%m-%d")
    maxdate=mindate + timedelta(days=nrdays)

    #determine latitude extent
    minlatdeg = latitude[nrlats-1]
    maxlatdeg = latitude[0]

    #determine longitude extent
    minlongdeg = longitude[0]
    maxlongdeg = longitude[nrlongs-1]

    #print("Data Source files: %s with %s" % (inputfile, pvaluesfile))
    #print("Source data TIME PERIOD: from %s till %s" % (mindate, maxdate))
    #print("Source data AREA BBOX; latitude %3.1f till %3.1f and longitude %3.1f till %3.1f" % (minlatdeg, maxlatdeg, minlongdeg, maxlongdeg))

    
    # Default windspeed threshold (fixed) for the SSI indicator
    windspeed_threshold_value=input_parameters.get_threshold_value()

    # Default windspeed percentile  for the SSI indicator
    windspeed_threshold_percentile=input_parameters.get_threshold_perc()

    #Get the specified title to create the outputfile and remove blanks
    #outputfile= clean_filename(outputfile)
    #outputfile= input_parameters.get_title() + "_output.nc"
    outputfile= "SSIoutput.nc"
    

    #Validate and process StartDate and EndDate
    #startdate = date.fromisoformat(input_parameters.get_start_time())
    startdate = datetime.strptime(input_parameters.get_start_time(), "%Y-%m-%d")
   
    #enddate = date.fromisoformat(input_parameters.get_end_time())
    enddate = datetime.strptime(input_parameters.get_end_time(), "%Y-%m-%d")
    

    print("SUMMARY OF SSI CALCULATION PARAMETERS (INPUT):" )

    #Validate and process StepUnit and StepSize
    unitoptions=[('None', 1), ('Days', 2), ('Months', 3), ('Years', 4)]
    allowed_stepunits = {'None':1, 'Days':2, 'Months':3, 'Years':4}
    stepunit=allowed_stepunits[input_parameters.get_time_stepunit()]
    stepsize=input_parameters.get_time_stepsize()
    if stepunit == 3:
        startdate = startdate.replace(day=1,)
        _, daysmonth = calendar.monthrange(enddate.year, enddate.month)
        enddate = enddate.replace(day=daysmonth)
        print ("\tStart:", startdate.strftime('%Y-%m'))
        print ("\tEnd(including):", enddate.strftime('%Y-%m'))
    elif stepunit == 4:
        startdate = startdate.replace(month=1, day=1)
        enddate = enddate.replace(month=12, day=31)
        print ("\tStart:", startdate.strftime('%Y'))
        print ("\tEnd(including):", enddate.strftime('%Y'))
    else:
        print ("\tStart:", startdate)
        print ("\tEnd(including):", enddate)

    try:
        if startdate < mindate:
            raise Exception("Start date %s outside input TIME RANGE: %s till %s" % (startdate.strftime("%Y-%m-%d"), mindate.strftime("%Y-%m-%d"), maxdate.strftime("%Y-%m-%d")))
        if enddate > maxdate:
            raise Exception("End date %s outside input TIME RANGE: %s till %s" % (enddate.strftime("%Y-%m-%d"), mindate.strftime("%Y-%m-%d"), maxdate.strftime("%Y-%m-%d")))                
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    
        
        
    #determine time interval
    deltastart = startdate-mindate
    deltastartday=deltastart.days
    deltaperiod = enddate-startdate
    #include enddate +1
    #deltaperiodday=deltaperiod.days + 1
    deltaperiodday=deltaperiod.days
    deltaendday=deltastartday+deltaperiodday
        
    
    if stepunit==1:
        stepsize=1
    if stepunit >1:
        print ("\tStepsize:", stepsize, unitoptions[stepunit-1][0])
    else:
        print ("\tStepsize:", unitoptions[stepunit-1][0])

    #no step
    if stepunit == 1: # no serie
        nrsteps=1
        steprange=deltaperiodday
    elif stepunit == 2: # days
        nrsteps=math.ceil(deltaperiodday/stepsize)
        steprange=stepsize
    elif stepunit == 3: #month
        nrmonths = diff_month(enddate, startdate)
        nrsteps=math.ceil(nrmonths/stepsize)
    #    if nrsteps == nrmonths/stepsize :
    #        nrsteps +=1
    elif stepunit == 4: #years
        nrsteps=math.ceil((enddate.year - startdate.year)/stepsize)
        if nrsteps == (enddate.year - startdate.year)/stepsize :
            nrsteps +=1

    print("\tNumber of steps (maps) = ", nrsteps)

    
    stepdeg=0.5
    
    #Validate and process Latitude and Longitude ranges
    startlongdeg = wd.get_horizontal_domain(input_parameters.get_working_domain())[0][0]
    endlongdeg = wd.get_horizontal_domain(input_parameters.get_working_domain())[0][2]
    startlatdeg= wd.get_horizontal_domain(input_parameters.get_working_domain())[0][1]
    endlatdeg = wd.get_horizontal_domain(input_parameters.get_working_domain())[0][3]

    try:
        if startlongdeg < minlongdeg:
            raise Exception("Start longitude %3.1f outside input long. RANGE: %3.1f till %3.1f" % (startlongdeg, minlongdeg, maxlongdeg))
        if endlongdeg > maxlongdeg:
            raise Exception("End longitude %s outside input long. RANGE: %3.1f till %3.1f" % (endlongdeg, minlongdeg, maxlongdeg))                
        if startlatdeg < minlatdeg:
            raise Exception("Start latitude %s outside input lat. RANGE: %3.1f till %3.1f" % (startlatdeg, minlatdeg, maxlatdeg))                
        if endlatdeg > maxlatdeg:
            raise Exception("End latitude %s outside input lat. RANGE: %3.1f till %3.1f" % (endlatdeg, minlatdeg, maxlatdeg))                
    except Exception as e:
        error_code = 2
        json_log.handle_exc(traceback.format_exc(), str(e), error_code)
        exit(error_code)    
                             
    print("\tLatitude range:" ,startlatdeg, endlatdeg)
    print("\tLongitude range:", startlongdeg, endlongdeg)
    #print("Source data AREA BBOX; latitude %3.1f till %3.1f and longitude %3.1f till %3.1f" % (minlatdeg, maxlatdeg, minlongdeg, maxlongdeg))
    
    #Latitude range
    #startlat = int((startlatdeg - minlatdeg)/stepdeg)
    startlat = int((maxlatdeg - endlatdeg)/stepdeg)
    #endlat = int((endlatdeg - minlatdeg)/stepdeg) +1
    #endlat = int((endlatdeg - minlatdeg)/stepdeg)
    endlat = int((maxlatdeg - startlatdeg)/stepdeg)
    deltaperiodlat=endlat-startlat

    #Longitude range
    startlong = int((startlongdeg - minlongdeg)/stepdeg)
    #endlong = int((endlongdeg - minlongdeg)/stepdeg) +1
    endlong = int((endlongdeg - minlongdeg)/stepdeg)
    deltaperiodlong=endlong-startlong

    #Validate and process windspeed threshold
    windthreshold_perc= input_parameters.get_output_type()
    
    # Default windspeed threshold (fixed) for the SSI indicator
    windspeed_threshold_value=input_parameters.get_threshold_value()

    # Default windspeed percentile  for the SSI indicator
    windspeed_threshold_percentile=input_parameters.get_threshold_perc()


    if windthreshold_perc=='ssi_percentile':
        print("\tWindspeed threshold percentile:", windspeed_threshold_percentile )
    elif windthreshold_perc=='ssi_percentile_min':
        print("\tWindspeed threshold percentile %s with mininum value %3.1f"% (windspeed_threshold_percentile,windspeed_threshold_value))
    else:
        print("\tWindspeed threshold -fixed- (m/s):", windspeed_threshold_value)
    print("\n")
    #
    #create SSI calulation arrays (tmp and output)
    #
    SSIdaily=np.zeros((deltaperiodday, deltaperiodlat, deltaperiodlong), dtype=np.float32)
    SSIoutput=np.zeros((nrsteps, deltaperiodlat, deltaperiodlong), dtype=np.float32)
    SSImax=np.zeros((nrsteps, deltaperiodlat, deltaperiodlong), dtype=np.float32)
    SSIndays=np.zeros((nrsteps, deltaperiodlat, deltaperiodlong), dtype=np.int32)
    SSIrate=np.zeros((nrsteps, deltaperiodlat, deltaperiodlong), dtype=np.float32)
    SSIwindspeed_perc=np.zeros((deltaperiodlat, deltaperiodlong), dtype=np.float32)
    SSIAreaoutput=np.zeros((nrsteps), dtype=np.float32)
    SSIAreamax=np.zeros((nrsteps), dtype=np.float32)
    SSIAreandays=np.zeros((nrsteps), dtype=np.int32)
    SSIArearate=np.zeros((nrsteps), dtype=np.float32)

    timeperiod=np.zeros(nrsteps)
    timestepsize=np.zeros(nrsteps+1)
    latitude_range=np.zeros(deltaperiodlat)
    longitude_range=np.zeros(deltaperiodlong)

    #Initialize
    timeperiod[0]=timeVariable[deltastartday*24]

    outputlatidx=0
    for latidx in range(deltaperiodlat):
        latitude_range[outputlatidx]=latitude[startlat+latidx]
        outputlatidx += 1

    outputlongidx = 0
    for longidx in range(deltaperiodlong):
        longitude_range[outputlongidx] = longitude[startlong+longidx]
        outputlongidx += 1

    if windthreshold_perc=='ssi_percentile' or windthreshold_perc=='ssi_percentile_min':
        for latidx in range(deltaperiodlat):
            for longidx in range(deltaperiodlong):
                if windspeed_threshold_percentile == 'P90':
                    SSIwindspeed_perc[latidx][longidx]= windspeed_Pvals[0][startlat+latidx][startlong+longidx]
                elif windspeed_threshold_percentile == 'P95':
                    SSIwindspeed_perc[latidx][longidx]= windspeed_Pvals[1][startlat+latidx][startlong+longidx]
                elif windspeed_threshold_percentile == 'P98':
                    SSIwindspeed_perc[latidx][longidx]= windspeed_Pvals[2][startlat+latidx][startlong+longidx]
                else:
                    SSIwindspeed_perc[latidx][longidx]= windspeed_Pvals[3][startlat+latidx][startlong+longidx]

    startidx=deltastartday
    endidx=deltastartday
    step=0
    currentstartdate = startdate
    currentenddate = startdate

    #
    #Calculate SSI for the selected timeperiod and area
    #
    print("CALCULATION started")
    while endidx < deltaendday:
        if stepunit == 1: # no serie
            endidx=deltaendday
            stepsizedays=0
        elif stepunit == 2: # days
            startidx = endidx
            stepsizedays=stepsize
            endidx += stepsizedays
        elif stepunit == 3: #month
            startidx = endidx
            currentstartdate = currentenddate
            if (currentenddate.month + stepsize) > 12 :
                currentenddate = currentenddate.replace(year=(currentenddate.year + 1))
                currentenddate = currentenddate.replace(month=(currentenddate.month + stepsize -12))
            else:
                currentenddate = currentenddate.replace(month=(currentenddate.month + stepsize))
            currentdelta = currentenddate - currentstartdate
            stepsizedays = currentdelta.days
            endidx += stepsizedays
        elif stepunit == 4: #years
            startidx = endidx
            currentstartdate = currentenddate
            currentenddate = currentenddate.replace(year=(currentenddate.year + stepsize))
            currentdelta = currentenddate - currentstartdate
            stepsizedays = currentdelta.days
            endidx += stepsizedays

        if endidx > deltaendday:
            endidx = deltaendday

        timeperiod[step]=timeVariable[startidx*24]

        for dayidx in range(startidx, endidx):   
            startHourIndex = (dayidx * 24)
            endHourIndex = startHourIndex+24
            newdayidx = step*(endidx - startidx) + (dayidx - startidx)

            # Load the data from the NetCDF variable for this specific day (24 hours)
            windspeedPerDay = windspeedVariable[startHourIndex:endHourIndex][:][:]

            # Calculate day and add to timestep
            calcSSIDayStep(SSIdaily, SSIoutput, SSImax, SSIrate, SSIndays, windspeedPerDay, windthreshold_perc, SSIwindspeed_perc, windspeed_threshold_value, startlat, startlong, newdayidx, step, deltaperiodlat ,deltaperiodlong)

        #Calculate area totals of a timestep
        calcSSIAreaStep(SSIAreaoutput, SSIAreamax, SSIArearate, SSIAreandays,SSIoutput, SSImax, SSIrate, SSIndays, step, deltaperiodlat ,deltaperiodlong)

        #Next step
        print('.', end='', flush=True)
        step += 1
        timestepsize[step] = timestepsize[step-1] + stepsizedays

    print("\nCALCULATION finished\n")
    json_log.phase_done("Calculate SSI")

    json_log.phase_start("Save SSI output data")
    # ### Save calculated SSI grid data and timeseries in output file
    #
    #create outputfile
    #
    dsOutput = Dataset(outputfile,mode='w',format='NETCDF4')
    dsOutput.title='SSI calculated data'
    dsOutput.subtitle="SSI calculated data"

    # copy global attributes all at once via dictionary
    dsOutput.setncatts(dsInput.__dict__)

    # copy dimensions
    lat_dim = dsOutput.createDimension('lat', deltaperiodlat)     # latitude axis
    lon_dim = dsOutput.createDimension('lon', deltaperiodlong)    # longitude axis
    time_dim = dsOutput.createDimension('time', nrsteps)   # time axis
    #for name, dimension in dsInput.dimensions.items():
    #        dsOutput.createDimension(
    #            name, (len(dimension) if not dimension.isunlimited() else None))

    toexclude = ['time', 'wind','latitude', 'longitude']
    # copy all file data except for the excluded
    for name, variable in dsInput.variables.items():
        if name not in toexclude:
            x = dsOutput.createVariable(name, variable.datatype, variable.dimensions)
            # copy variable attributes all at once via dictionary
            dsOutput[name].setncatts(dsInput[name].__dict__)
            dsOutput[name][:] = dsInput[name][:]

    x = dsOutput.createVariable('time', np.int32, ('time',))
    dsOutput['time'].setncatts(dsInput['time'].__dict__)
    dsOutput['time'].standard_name='time'
    dsOutput['time'][:] = timeperiod

    y = dsOutput.createVariable('lat',np.float32,('lat',))
    dsOutput['lat'].setncatts(dsInput['latitude'].__dict__)
    dsOutput['lat'].standard_name='latitude'
    dsOutput['lat'][:] = latitude_range

    z = dsOutput.createVariable('lon',np.float32,('lon',))
    dsOutput['lon'].setncatts(dsInput['longitude'].__dict__)
    dsOutput['lon'].standard_name='longitude'
    dsOutput['lon'][:] = longitude_range

    # Define SSI arrays to hold the grid data
    SSItotal = dsOutput.createVariable('SSItotal',np.float32,('time','lat','lon')) # note: unlimited dimension is leftmost
    SSItotal.standard_name = 'SSI_total' # this is a CF standard name
    SSItotal[:,:,:] = SSIoutput   # Appends data along unlimited dimension

    SSImaximum = dsOutput.createVariable('SSImax',np.float32,('time','lat','lon')) # note: unlimited dimension is leftmost
    SSImaximum.standard_name = 'SSI_max' # this is a CF standard name
    SSImaximum[:,:,:] = SSImax  # Appends data along unlimited dimension

    SSInrdays = dsOutput.createVariable('SSInrdays',np.int32,('time','lat','lon')) # note: unlimited dimension is leftmost
    SSInrdays.standard_name = 'SSI_nrdays' # this is a CF standard name
    SSInrdays[:,:,:] = SSIndays  # Appends data along unlimited dimension

    SSIavgrate = dsOutput.createVariable('SSIrate',np.float32,('time','lat','lon')) # note: unlimited dimension is leftmost
    SSIavgrate.standard_name = 'SSI_rate' # this is a CF standard name
    SSIavgrate[:,:,:] = SSIrate  # Appends data along unlimited dimension

    # Define SSI arrays to hold the grid data
    SSIAreatotal = dsOutput.createVariable('SSIAreatotal',np.float32,('time')) # note: unlimited dimension is leftmost
    SSIAreatotal.standard_name = 'SSIArea_total' # this is a CF standard name
    SSIAreatotal[:] = SSIAreaoutput  # Appends data along unlimited dimension

    SSIAreamaximum = dsOutput.createVariable('SSIAreamax',np.float32,('time')) # note: unlimited dimension is leftmost
    SSIAreamaximum.standard_name = 'SSIArea_max' # this is a CF standard name
    SSIAreamaximum[:] = SSIAreamax  # Appends data along unlimited dimension

    SSIAreanrdays = dsOutput.createVariable('SSIAreanrdays',np.int32,('time')) # note: unlimited dimension is leftmost
    SSIAreanrdays.standard_name = 'SSIArea_nrdays' # this is a CF standard name
    SSIAreanrdays[:] = SSIAreandays  # Appends data along unlimited dimension

    SSIAreaavgrate = dsOutput.createVariable('SSIArearate',np.float32,('time')) # note: unlimited dimension is leftmost
    SSIAreaavgrate.standard_name = 'SSIArea_rate' # this is a CF standard name
    SSIAreaavgrate[:] = SSIArearate  # Appends data along unlimited dimension

    print("OUTPUT:")
    print("Calculated SSI grid data %s and time series data store in %s" % (SSItotal.shape, outputfile))

    dsInput.close()
    dsOutput.close()

    #
    # ## SSI plots (maps (disabled) and time series)
    #

    nc = xr.open_dataset(outputfile)

    #SSItotalselected = 0
    SSItotalselected = 1
    SSImaxselected = SSInrdaysselected =  SSIrateselected = 0
    
    #SSItotalselected = SSItotalselection.value
    #SSImaxselected = SSImaxselection.value
    #SSInrdaysselected = SSInrdaysselection.value
    #SSIrateselected = SSIrateselection.value
    
    #plotlimit = plotmaps = 0
    plotlimit = 50
    plotmaps = 1
    plotseries = 1
    
    #plotlimit = Plotlimitation.value - 1
    #plotmaps = Plottypemaps.value
    #plotseries = Plottypeseries.value

    nrmaps = SSItotalselected + SSImaxselected + SSInrdaysselected + SSIrateselected

    #if nrmaps == 1:
    #    plt.rcParams['figure.figsize'] = 15, 8.
    #elif nrmaps == 2:
    #    plt.rcParams['figure.figsize'] = 15, 12.
    #elif nrmaps == 3:
    #    plt.rcParams['figure.figsize'] = 15, 16.
    #else:
    #    plt.rcParams['figure.figsize'] = 15, 20.
    
    xx=15
    nrmaps=nrsteps+1
    if nrmaps > plotlimit:
        nrmaps=plotlimit+1
    xx= 15
    yy= 4*nrmaps
    plt.rcParams['figure.figsize'] = xx, yy
    plt.rcParams['axes.facecolor']='white'
    plt.rcParams['savefig.facecolor']='white'
    plt.rcParams['figure.subplot.hspace'] = 0.5
    mapindex=0


    if plotmaps:
        for ii in range(nrsteps):

            #Compose figure title
            if stepunit == 4:
                titlestartdate = startdate + timedelta(days=timestepsize[ii])
                titlename= "Year %s" % (titlestartdate.strftime('%Y'))
                if stepsize > 1:
                    titleenddate = startdate + timedelta(days=(timestepsize[ii+1]-1))
                    titlename = titlename + " - %s" % (titleenddate.strftime('%Y'))
            elif stepunit == 3:
                titlestartdate = startdate + timedelta(days=timestepsize[ii])
                titlename= "Month %s" % (titlestartdate.strftime('%Y-%m'))
                if stepsize > 1:
                    titleenddate = startdate + timedelta(days=(timestepsize[ii+1]-1))
                    titlename = titlename + " - %s" % (titleenddate.strftime('%Y-%m'))
            elif stepunit == 2:
                titlestartdate = startdate + timedelta(days=timestepsize[ii])
                titlename= "Day %s" % (titlestartdate)
                if stepsize > 1:
                    titleenddate = startdate + timedelta(days=(timestepsize[ii+1]-1))
                    titlename = titlename + "% - %s" % (titleenddate)
            else:
                titlestartdate = startdate
                titleenddate = enddate
                titlename = "Period %s - %s" % (titlestartdate, titleenddate)

            filetitlename = titlename
            if windthreshold_perc =='ssi_percentile':
                titlename = titlename + "(threshold %s percentile)" % (windspeed_threshold_percentile)
            elif windthreshold_perc =='ssi_percentile_min':
                titlename = titlename + " (threshold %s percentile with min. %3.1f m/s )" % (windspeed_threshold_percentile, windspeed_threshold_value)
            else:
                titlename = titlename + " (threshold fixed %3.1f m/s)" % (windspeed_threshold_value)

            #mapindex=0

            if SSItotalselected:
                mapindex += 1
                ax=plt.subplot(nrmaps,1,mapindex,projection=ccrs.PlateCarree())
                da =nc.SSItotal.isel(time=ii)
                da.plot.pcolormesh("lon", "lat", ax=ax, cmap=plt.cm.Reds, cbar_kwargs=dict(orientation='vertical', shrink=0.5))
                ax.set_title(titlename)
                ax.coastlines()
                ax.gridlines(draw_labels=True)

            if SSImaxselected:
                mapindex += 1
                ax = plt.subplot(nrmaps,1,mapindex,projection=ccrs.PlateCarree())
                da=nc.SSImax.isel(time=ii)
                da.plot.pcolormesh("lon", "lat", ax=ax, cmap=plt.cm.Reds, cbar_kwargs=dict(orientation='vertical', shrink=0.5))
                ax.set_title(titlename)
                ax.coastlines()
                ax.gridlines(draw_labels=True)

            if SSInrdaysselected:
                mapindex += 1
                ax = plt.subplot(nrmaps,1,mapindex,projection=ccrs.PlateCarree())
                da=nc.SSInrdays.isel(time=ii)
                da.plot.pcolormesh("lon", "lat", ax=ax, cmap=plt.cm.Reds, cbar_kwargs=dict(orientation='vertical', shrink=0.5))
                ax.set_title(titlename)
                ax.coastlines()
                ax.gridlines(draw_labels=True)

            if SSIrateselected:
                mapindex += 1
                ax = plt.subplot(4,1,4,projection=ccrs.PlateCarree())
                da=nc.SSIrate.isel(time=ii)
                da.plot.pcolormesh("lon", "lat", ax=ax, cmap=plt.cm.Reds, cbar_kwargs=dict(orientation='vertical', shrink=0.5))
                ax.set_title(titlename)
                ax.coastlines()
                ax.gridlines(draw_labels=True)

            #plt.tight_layout()
            #filetitlename = filetitlename.replace(' ', '_')
            #plt.savefig("%s_map_%s.png" % (outputfile, filetitlename), format='png')
            #plt.show()
            #plt.close()

            
            if ii == plotlimit :
                ii=nrsteps
                break
        
        plt.tight_layout()
        plt.savefig("SSImaps.png", format='png')
        #plt.show()
        plt.close()
        print("SSI map plots created: SSImaps.png")
        

    if plotseries and nrsteps > 1 :
        plt.rcParams['figure.figsize'] = 15, 20.
        fig, axes = plt.subplots(nrows=4)
        nc.SSIAreatotal.plot(ax=axes[0], color="red", marker="o")
        nc.SSIAreamax.plot(ax=axes[1], color="red", marker="o")
        nc.SSIAreanrdays.plot(ax=axes[2], color="red", marker="o")
        nc.SSIArearate.plot(ax=axes[3], color="red", marker="o")
        
        plt.tight_layout()
        #timeseriesplot = outputfile.replace("_output.nc", "") + "_area_timeseries.png"
        #plt.savefig(timeseriesplot, format='png')
        plt.savefig("SSItimeseries.png", format='png')
        #plt.show()
        plt.close()

        #print("SSI area time series plot created: %s" % timeseriesplot)
        print("SSI area time series plots created: SSItimeseries.png")
    
    json_log.phase_done("Save SSI output data")
    
    print("\n\n===SSI METHOD COMPLETED===")


