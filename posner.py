from psychopy import visual, core, event, data, gui, logging

#initialise experiment-wide objects
win = visual.Window([1024,768], fullscr=False, units='pix')
globalClock = core.Clock()
respClock = core.Clock()

#initialise experiment information
info = {} #a dictionary
#present dialog to collect info
info['participant'] = ''
dlg = gui.DlgFromDict(info)
if not dlg.OK:
    core.quit()
    
#add additional info after the dialog has gone
info['fixFrames'] = 30 #0.5s at 60Hz
info['cueFrames'] = 12 #200ms at 60Hz
info['probeFrames'] = 12
info['dateStr'] = data.getDateStr() #will create str of current date/time

#set up logging
#create a clock to synchronise with our experiment
globalClock = core.Clock()
logging.setDefaultClock(globalClock)
logging.console.setLevel(logging.WARNING)#set the console to receive warnings and errors
    
#create the base filename for our data files
filename = "data/{participant}_{dateStr}".format(**info)

DEBUG = False # set debug
if DEBUG:
    fullscr = False
    logging.console.setLevel(logging.INFO)
else:
    fullscr = True
    logging.console.setLevel(logging.WARNING)

# initialise stimuli
fixation = visual.Circle(win, size = 5,
    lineColor = 'white', fillColor = 'lightGrey')
probe = visual.ImageStim(win, size = 80, # 'size' is 3xSD for gauss,
    pos = [300, 0], #we'll change this later
    image = None, mask = 'gauss',
    color = 'green')
cue = visual.ShapeStim(win, 
    vertices = [[-30,-20], [-30,20], [30,0]],
    lineColor = 'red', fillColor = 'salmon')
textStim = visual.TextStim(win)

conditions = data.importConditions('conditions.csv') #import conditions from file

# Messages
instructPractice = 'This is just a practice, no data will be saved.'
instructExp = 'We\'re doing the experiment for real now. \n\nData will be saved in %s' % '/'+filename+'.csv'
instructThanks = 'Thank you -- this was an example of the Posner paradigm.'

# Create a function to show text
def showText(input, acceptedKeys=None):
    """Presents text and waits for accepted keys"""
    
    # Set and display text
    textStim.setText(input)
    textStim.draw()
    win.flip()
    
    # Wait for response and return it
    response = event.waitKeys(keyList=acceptedKeys)
    if response[0] == 'q':
        logging.warning('Script manually interrupted by keypress')
        core.quit()
    return response

def runBlock(nReps=1, saveFile= True):
    """Runs a block of trials
    nReps is the number of repetitions of every trialList
    saveFile(bool) is whether to save data or logfiles"""
    
    #set up the trials/experiment
    trials = data.TrialHandler(trialList=conditions, nReps=nReps) #create trial handler (loop)

    if saveFile:
        #create logging file
        logDat = logging.LogFile(filename+".log",
            filemode='w', #set to 'a' to append instead of overwriting
            level=logging.EXP)#errors, data events and warnings sent to this logfile
            
        #add trials to the experiment handler to store data
        thisExp = data.ExperimentHandler(
                name='Posner', version='1.0', #not needed, just handy
                extraInfo = info, #the info we created earlier
                dataFileName = filename, # using our string with data/name_date
                )
        thisExp.addLoop(trials) #there could be other loops (like practice loop)

    #loop through trials
    for thisTrial in trials:
        # set up this trial
        resp = None
        rt = None
        probe.setPos( [thisTrial['probeX'], 0] )
        cue.setOri( thisTrial['cueOri'] )
        
        #fixation period
        fixation.setAutoDraw(True)
        for frameN in range(info['fixFrames']):
            win.flip()
            
        #present cue
        cue.setAutoDraw(True)
        for frameN in range(info['cueFrames']):
            win.flip()
        cue.setAutoDraw(False)
        
        #present probe
        probe.setAutoDraw(True)
        win.callOnFlip(respClock.reset) #can use callOnFlip() to reset the clock
        event.clearEvents()
        for frameN in range(info['probeFrames']):
            win.flip()
            keys = event.getKeys(keyList = ['left', 'right', 'escape'])
            if len(keys)>0:
                resp = keys [0] #take the first keypress as the response
                rt = respClock.getTime()
                break #out of the probe-drawing loop
        probe.setAutoDraw(False)
        fixation.setAutoDraw(False)
        
        #clear screen
        win.flip()
        
        #wait for response if we didn't already have one
        if resp is None:
            keys = event.waitKeys(keyList = ['left','right','escape'])
            resp = keys[0] #take first response
            rt = respClock.getTime()
        
        #check if the response was correct
        if thisTrial['probeX']>0 and resp=='right':
            corr = 1
        elif thisTrial['probeX']<0 and resp=='left':
            corr = 1
        elif resp=='escape':
            trials.finished = True
        else:
            corr = 0
            
        #store the response and RT
        trials.addData('resp', resp)
        trials.addData('rt', rt)
        trials.addData('corr', corr)
        
        if saveFile:
            thisExp.nextEntry()

#practice trials
showText(instructPractice)
runBlock(nReps=1, saveFile=False) #comment to not run practice trials

#real data collection
showText(instructExp)
runBlock(nReps=2, saveFile=True)

#show a debriefing screen
showText(instructThanks)