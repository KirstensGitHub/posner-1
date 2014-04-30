from psychopy import gui, misc
from os import path
import pandas as pd
import scipy
from scipy import stats
import matplotlib.pyplot as plt

#filenames = gui.fileOpenDlg(".",allowed="*.psydat") # the "." argument means 'start in the current directory'
#print filenames
#
# let's export a csv file from the psydat file
#for thisFileName in filenames:
#    thisPath, thisFullName = path.split(thisFileName)
#    thisFullPath, thisExt = path.splitext(thisFileName)
#    fileNoExt, fileExt = path.splitext(thisFileName)
#    newName = fileNoExt+"NEW.csv"
#    dat = misc.fromFile(thisFileName)
#    dat.saveAsWideText(newName)
#    print 'saved', newName
   
filenamesPd = gui.fileOpenDlg(allowed="*.csv") 

for thisFilenamePd in filenamesPd:
    print thisFilenamePd
    thisDat = pd.read_csv(thisFilenamePd) # it's a data frame like in R, or an array like in numpy
    # filter out the bad data
    filtered = thisDat[thisDat["corr"]==1] # only include correct values
    filtered = filtered[filtered["rt"]<=1.0] # remove RTs larger than 1s 
    conflict = filtered[filtered["description"] == 'conflict'] # conflicting cue data
    congruent = filtered[filtered["description"] != 'conflict'] # congruent cue data
    
    #get mean/std.dev
    meanConfl = scipy.mean(conflict["rt"])
    sdConfl = scipy.std(conflict["rt"], ddof=1) # ddof=1 means /sqrt(N-1)
    meanCongr = scipy.mean(congruent["rt"])
    sdCongr = scipy.std(congruent["rt"], ddof=1)
    print "Conflict = %.3f (sd=%.3f)" %(meanConfl, sdConfl)
    print "Congruent = %.3f (sd=%.3f)" %(meanCongr, sdCongr) 
   
    # checking significance
    t, p = stats.ttest_ind(conflict["rt"], congruent["rt"])
    print "Independent samples t-test: t=%.3f, p=%.4f" % (t,p)
   
    # lets plot the data
    fig, ax = plt.subplots(1)
    ax.bar([1,2], [meanConfl, meanCongr], yerr=[sdConfl, sdCongr])
    plt.show() 