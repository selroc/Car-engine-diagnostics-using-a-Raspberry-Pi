"""@package utilities
"""
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
import time
import cpi2adc #analogue to digital converter library
import csv
import numpy as np
from peakfind import detect_peaks, plot#peakfind library

read0=cpi2adc.readchannel0 #define read chanel


def valuesBefore():
    """Calculates the average of the battery before ignition

    Returns
    -------
    avgBefore : float
        the average of the battery before ignition
    """
    
    valuesBefore = []

    t_end = time.time() + 10
    while time.time() < t_end :#]read channel 0
        V=read0()
        V=V/0.155
        V= round (V,3)

        valuesBefore.append(V)

    avgBefore = np.mean(valuesBefore)

    print ("the battery measurement before ignition sequence has finished")

    with open('csv/Before.csv', 'w') as file:
            writer = csv.writer(file, delimiter = '\t', lineterminator = '\n',)
            for x in range(0, len(valuesBefore)):
                row = valuesBefore[x]
                writer.writerow([row])
    return avgBefore

def valuesIgnittion(mpd):
    """Measures the data from the battery and calculates the average for each cylinder plots
        the signal graph, the average graph and the percentage graph.
    Parameters
    ----------
    mpd : int
        minimum peak distance. used in the pead detect function

    Returns
    -------
    avgCylPeak1 : float
        the average of cylinder 1 peaks
    avgCylPeak2 : float
        the average of cylinder 2 peaks
    avgCylPeak3 : float
        the average of cylinder 3 peaks
    avgCylPeak4 : float
        the average of cylinder 4 peaks
    avgCyl1 : float
        the average of cylinder 1 troughs
    avgCyl2 : float
        the average of cylinder 2 toughs
    avgCyl3 : float
        the average of cylinder 3 troughs
    avgCyl4 : float
        the average of cylinder 4 troughs
    """
    
    x =[]

    t_end = time.time() + 3
    while time.time() < t_end :#read from channel 0 for specified amount of time
        V=read0()
        V=V/0.155
        V= round (V,3)
        x.append(V)
    
    print ("the battery measurement during ignition sequence has finished")

    #writing the values to file for future reference
    with open('csv/Battery.csv', 'w') as file:
            writer = csv.writer(file, delimiter = '\t', lineterminator = '\n',)
            for i in range(0, len(x)):
                row = x[i]
                writer.writerow([row])

    #finding peaks and troughs indexes
    peaks = detect_peaks(x,mpd = mpd,show=True) #returns list of indexes of peaks in values list
    troughs =detect_peaks(x,mpd = mpd,valley = True, show=True) #returns list of indexes of troughs in values list

    ind = np.unique(np.hstack((peaks, troughs))) #concatinate the peaks and troughs arrays as one

    x = np.atleast_1d(x).astype('float64')#make values list as array so it is compatible with plot function

    plot(x, ind) #plot the voltage wave and mark both peaks and troughs

    #find peaks and troughs values and plot overall drop 
    #and percentage of efficiency graphs
    peakValues, troughValues, avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4 =calculateavg(x,peaks,troughs)

    print('peaks')
    print(peakValues)
    print('troughs')
    print(troughValues)


    return avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4
    ##################end of cranking stage##########

def valuesAfter(avgBefore, avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4):
    """Reads the battery voltage after ignition, calculates the average and plots the average for each 
        cylinder and the average of battery before and after ignition

    Parameters
    ----------
    avgBefore: float
        the average of the battery before ignition
    avgCylPeak1 : float
        the average of cylinder 1 peaks
    avgCylPeak2 : float
        the average of cylinder 2 peaks
    avgCylPeak3 : float
        the average of cylinder 3 peaks
    avgCylPeak4 : float
        the average of cylinder 4 peaks
    avgCyl1 : float
        the average of cylinder 1 troughs
    avgCyl2 : float
        the average of cylinder 2 toughs
    avgCyl3 : float
        the average of cylinder 3 troughs
    avgCyl4 : float
        the average of cylinder 4 troughs
    """

    valuesAfter = []

    t_end = time.time() + 10
    while time.time() < t_end :#]read channel 0
        V=read0()
        V=V/0.155
        V= round (V,3)

        valuesAfter.append(V)

    avgAfter = np.mean(valuesAfter)

    print ("the battery measurement after ignition sequence has finished")

    plotavgall(avgAfter, avgBefore,avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4)

    with open('csv/After.csv', 'w') as file:
            writer = csv.writer(file, delimiter = '\t', lineterminator = '\n',)
            for x in range(0, len(valuesAfter)):
                row = valuesAfter[x]
                writer.writerow([row])

def readcsv(filename):
    """Reads a csv file for local testing

    Parameters
    ----------
    filename : csv file
        a csv file with the signal data

    Returns
    -------
    a : list
        list of values in csv
    """
    import csv
    file = open(filename, "rU")
    reader = csv.reader(file, delimiter=";")

    a = []

    for row in reader:
        for y in row:
            a.append(float(y))
    
    file.close()
    return a

def calculateavg(x,peaks,troughs):
    """Calculates the average for each cylinder and send data to plot functions

    Parameters
    ----------
    x : array
        the signal data
    peaks: array
        the indices of peaks in x
    troughs: array
        the indices of troughs in x

    Returns
    -------
    peakValues : list
        list of peak numerical values
    troughValues : list
        listf of troughs numerical values
    avgCylPeak1 : float
        the average of cylinder 1 peaks
    avgCylPeak2 : float
        the average of cylinder 2 peaks
    avgCylPeak3 : float
        the average of cylinder 3 peaks
    avgCylPeak4 : float
        the average of cylinder 4 peaks
    avgCyl1 : float
        the average of cylinder 1 troughs
    avgCyl2 : float
        the average of cylinder 2 toughs
    avgCyl3 : float
        the average of cylinder 3 troughs
    avgCyl4 : float
        the average of cylinder 4 troughs
    """
    peakValues = []
    troughValues = []

    #gets the values of peaks and troughs and saves them to a list
    i = 0
    for i in range (peaks.size):
        peakValues.append("%3f" % float(x[peaks[i]]))
    i = 0
    for i in range (troughs.size):
        troughValues.append("%3f" % float(x[troughs[i]]))

 #########find avg of peaks#############################
    cyl1Peak = 0
    cyl1Peakcount = 0
    cyl2Peak = 0
    cyl2Peakcount = 0
    cyl3Peak = 0
    cyl3Peakcount = 0
    cyl4Peak = 0
    cyl4Peakcount = 0
    i=0
    while i < len(peaks): #find the peaks of each cylinder

        cyl1Peak += float(peakValues[i])
        cyl1Peakcount += 1
        if (i + 1 >= len(peakValues)): break
        cyl2Peak += float(peakValues[i + 1])
        cyl2Peakcount += 1
        if (i + 2 >= len(peakValues)): break
        cyl3Peak += float(peakValues[i + 2])
        cyl3Peakcount += 1
        if (i + 3 >= len(peakValues)): break
        cyl4Peak += float(peakValues[i + 3])
        cyl4Peakcount += 1

        i += 4
        if (i >= len(peakValues)):
            while (i >= len(peakValues)):
                i -= 1
    
    ###calculate the avg of peaks for each cylinder
    if (cyl1Peakcount == 0):
        avgCylPeak1 = 0
    else:
        avgCylPeak1 = float(cyl1Peak / cyl1Peakcount)
    if (cyl2Peakcount == 0):
        avgCylPeak2 = 0
    else:
        avgCylPeak2 = float(cyl2Peak / cyl2Peakcount)
    if (cyl3Peakcount == 0):
        avgCylPeak3 = 0
    else:
        avgCylPeak3 = float(cyl3Peak / cyl3Peakcount)
    if (cyl4Peakcount == 0):
        avgCylPeak4 = 0
    else:
        avgCylPeak4 = float(cyl4Peak / cyl4Peakcount)
 ###################################################################

 ###find avg of troughs##################################################
    cyl1 = 0
    cyl1count = 0
    cyl2 = 0
    cyl2count = 0
    cyl3 = 0
    cyl3count = 0
    cyl4 = 0
    cyl4count = 0
    i=0
    while i < len(troughValues): #find the troughs for each cylinder
    
        cyl1 += float(troughValues[i])
        cyl1count += 1
        if (i + 1 >= len(troughValues)): break
        cyl2 += float(troughValues[i + 1])
        cyl2count += 1
        if (i + 2 >= len(troughValues)): break
        cyl3 += float(troughValues[i + 2])
        cyl3count += 1
        if (i + 3 >= len(troughValues)): break
        cyl4 += float(troughValues[i + 3])
        cyl4count += 1

        i += 4
        if (i >= len(troughValues)):
            while (i >= len(troughValues)):
                i -= 1
    
    #calculate the avg of troughs for each cylinder
    if (cyl1count == 0):
        avgCyl1 = 0
    else:
        avgCyl1 = float(cyl1 / cyl1count)

    if (cyl2count == 0):
        avgCyl2 = 0
    else:
        avgCyl2 = float(cyl2 / cyl2count)

    if (cyl3count == 0):
        avgCyl3 = 0
    else:
        avgCyl3 = float(cyl3 / cyl3count)

    if (cyl4count == 0):
        avgCyl4 = 0
    else:
        avgCyl4 = float(cyl4 / cyl4count)

    plotavg(avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4) #plot the average drop of each cylinder
    plotCylpercentage(avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, max(peakValues)) #plot the percentage of each cylinder

    return peakValues , troughValues , avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4
 
def plotavg(avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4):
    """Plot the average for each cylinder
    Parameters
    ----------
    avgCylPeak1 : float
        the average of cylinder 1 peaks
    avgCylPeak2 : float
        the average of cylinder 2 peaks
    avgCylPeak3 : float
        the average of cylinder 3 peaks
    avgCylPeak4 : float
        the average of cylinder 4 peaks
    avgCyl1 : float
        the average of cylinder 1 troughs
    avgCyl2 : float
        the average of cylinder 2 toughs
    avgCyl3 : float
        the average of cylinder 3 troughs
    avgCyl4 : float
        the average of cylinder 4 troughs
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print('matplotlib is not available.')
    else:
        _, ax = plt.subplots(1, 1, figsize=(8, 4))
        
        #plot the figure depending on how many cylinders we have measurements for
        #if for 1 cylinder we have a peak but not a trough it is not plotted as 
        #it will return a non representative figure
        if (avgCylPeak4 == 0 and avgCylPeak3 == 0 and (avgCylPeak2 == 0 or avgCyl2 == 0)):
            x = np.arange(5)
            ax.plot([avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak1])
            ax.set_xticks(x)
            ax.set_xticklabels(['','','Cylinder 1','',''])  
        elif (avgCylPeak4 == 0 and (avgCylPeak3 == 0 or avgCyl3 == 0)):
            x = np.arange(8)
            ax.plot([avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak2, avgCyl2, avgCylPeak2, avgCylPeak2])
            ax.set_xticks(x)
            ax.set_xticklabels(['','','Cylinder 1','', '', 'Cylinder 2','',''])  
        elif (avgCylPeak4 == 0 or avgCyl4 == 0):
            x = np.arange(14)
            ax.plot([avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak2, avgCyl2, avgCylPeak2, avgCylPeak3, 
                            avgCyl3, avgCylPeak3, avgCylPeak3])
            ax.set_xticks(x)
            ax.set_xticklabels(['','','Cylinder 1','', '', 'Cylinder 2','', '',
                                'Cylinder 3','', ''])  
        else:
            x = np.arange(14)
            ax.plot([avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak2, avgCyl2, avgCylPeak2, avgCylPeak3, 
                            avgCyl3, avgCylPeak3, avgCylPeak4, avgCyl4, avgCylPeak4, avgCylPeak4])
            ax.set_xticks(x)
            ax.set_xticklabels(['','','Cylinder 1','', '', 'Cylinder 2','', '',
                                'Cylinder 3','', '', 'Cylinder 4'])        
        
        ax.set_ylabel('Average Amplitude', fontsize=14)
        ax.set_title("Average amplitude of each cylinder")
        plt.savefig('Average amplitude')#saves the figure
        plt.show()

def plotavgall(avgAfter, avgBefore,avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4):
    """Plot the average for each cylinder and the average of battery before and after ignition
    Parameters
    ----------
    avgAfter: float
        the average of the battery after ignition
    avgBefore: float
        the average of the battery before ignition
    avgCylPeak1 : float
        the average of cylinder 1 peaks
    avgCylPeak2 : float
        the average of cylinder 2 peaks
    avgCylPeak3 : float
        the average of cylinder 3 peaks
    avgCylPeak4 : float
        the average of cylinder 4 peaks
    avgCyl1 : float
        the average of cylinder 1 troughs
    avgCyl2 : float
        the average of cylinder 2 toughs
    avgCyl3 : float
        the average of cylinder 3 troughs
    avgCyl4 : float
        the average of cylinder 4 troughs
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print('matplotlib is not available.')
    else:
        _, ax = plt.subplots(1, 1, figsize=(8, 4))
        
        #plot the figure depending on how many cylinders we have measurements for
        #if for 1 cylinder we have a peak but not a trough it is not plotted as 
        #it will return a non representative figure
        if (avgCylPeak4 == 0 and avgCylPeak3 == 0 and (avgCylPeak2 == 0 or avgCyl2 == 0)):
            x = np.arange(11)
            plt.plot([avgBefore, avgBefore, avgBefore, avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak1, avgAfter, avgAfter, avgAfter])
            ax.set_xticks(x)
            ax.set_xticklabels(['','Before\nignition','','','','Cylinder 1','','','', 'After\nignititon']) 
        elif (avgCylPeak4 == 0 and (avgCylPeak3 == 0 or avgCyl3 == 0)):
            x = np.arange(14)
            plt.plot([avgBefore, avgBefore, avgBefore, avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak2, avgCyl2, 
                                                                        avgCylPeak2, avgCylPeak2, avgAfter, avgAfter, avgAfter])
            ax.set_xticks(x)
            ax.set_xticklabels(['','Before\nignition','','','','Cylinder 1','', '', 'Cylinder 2','', '','', 'After\nignititon']) 
        elif (avgCylPeak4 == 0 or avgCyl4 == 0):
            x = np.arange(17)
            plt.plot([avgBefore, avgBefore, avgBefore, avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak2, avgCyl2, avgCylPeak2, avgCylPeak3, 
                            avgCyl3, avgCylPeak3, avgCylPeak3, avgAfter, avgAfter, avgAfter])
            ax.set_xticks(x)
            ax.set_xticklabels(['','Before\nignition','','','','Cylinder 1','', '', 'Cylinder 2','', '',
                                'Cylinder 3','','','', 'After\nignititon']) 
        else:
            x = np.arange(20)
            plt.plot([avgBefore, avgBefore, avgBefore, avgCylPeak1, avgCylPeak1 ,avgCyl1, avgCylPeak1, avgCylPeak2, avgCyl2, avgCylPeak2, avgCylPeak3, 
                            avgCyl3, avgCylPeak3, avgCylPeak4, avgCyl4, avgCylPeak4, avgCylPeak4, avgAfter, avgAfter, avgAfter])
            ax.set_xticks(x)
            ax.set_xticklabels(['','Before\nignition','','','','Cylinder 1','', '', 'Cylinder 2','', '',
                                'Cylinder 3','', '', 'Cylinder 4','','','', 'After\nignititon'])        
        
        ax.set_ylabel('Average Amplitude', fontsize=14)
        ax.set_title("Average amplitude of each cylinder before during and after ignition")
        plt.savefig('Average amplitude all stages')
        plt.show()

def plotCylpercentage(avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, max):
    """Plot the average for each cylinder
    Parameters
    ----------
    avgCylPeak1 : float
        the average of cylinder 1 peaks
    avgCylPeak2 : float
        the average of cylinder 2 peaks
    avgCylPeak3 : float
        the average of cylinder 3 peaks
    avgCylPeak4 : float
        the average of cylinder 4 peaks
    max : float
        the maximum value of peak available in the data. used to compare average of each cylinder to it
    """
    try:
        import matplotlib.pyplot as plt
        import numpy as np
    except ImportError:
        print('matplotlib is not available.')
    else:
        _, ax = plt.subplots()
        percentage = 100/ float(max)
        cyl1per = "%.2f" % (avgCylPeak1 * percentage)
        cyl2per = "%.2f" % (avgCylPeak2 * percentage)
        cyl3per = "%.2f" % (avgCylPeak3 * percentage)
        cyl4per = "%.2f" % (avgCylPeak4 * percentage)

        #plot the figure depending on how many cylinders we have measurements for
        if (avgCylPeak4 == 0 and avgCylPeak3 == 0 and avgCylPeak2 == 0):
            x = np.arange(1)
            val = [avgCylPeak1 * percentage, avgCylPeak2 * percentage]
            plt.bar(x, val)
            ax.set_xticks(x)
            ax.set_xticklabels(['Cylinder 1\n' + cyl1per + "%"])
        elif (avgCylPeak4 == 0 and avgCylPeak3 == 0):
            x = np.arange(2)
            val = [avgCylPeak1 * percentage, avgCylPeak2 * percentage]
            plt.bar(x, val)
            ax.set_xticks(x)
            ax.set_xticklabels(['Cylinder 1\n' + cyl1per + "%", 'Cylinder 2\n' + cyl2per + "%"])
        elif (avgCylPeak4 == 0):
            x = np.arange(3)
            val = [avgCylPeak1 * percentage, avgCylPeak2 * percentage, avgCylPeak3 * percentage]
            plt.bar(x, val)
            ax.set_xticks(x)
            ax.set_xticklabels(['Cylinder 1\n' + cyl1per + "%", 'Cylinder 2\n' + cyl2per + "%", 
                                'Cylinder 3\n' + cyl3per + "%"])
        else:
            x = np.arange(4)
            val = [avgCylPeak1 * percentage, avgCylPeak2 * percentage, avgCylPeak3 * percentage, avgCylPeak4 * percentage]
            plt.bar(x, val)
            ax.set_xticks(x)
            ax.set_xticklabels(['Cylinder 1\n' + cyl1per + "%", 'Cylinder 2\n' + cyl2per + "%", 
                                'Cylinder 3\n' + cyl3per + "%", 'Cylinder 4\n' + cyl4per + "%"])
        
        
        ax.set_ylabel('Average Amplitude', fontsize=14)
        ax.set_title("Average amplitude percentage of each cylinder\ncompared to maximum amplitude value")
        plt.savefig('Average amplitude percentage')
        plt.show()