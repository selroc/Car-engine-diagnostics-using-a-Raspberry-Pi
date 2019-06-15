"""@package read

The program starts by asking if the car is diesel or petrol. If any other than the two options
is inputed it terminates and prompts the user to start again. Then continues by reading the battery 
voltage before ignition and calculating its average.
Then it ask the user if they are ready to start the car. If the user says yes it runs the ignition phase 
subsequently plotting the signal with peaks and troughs detected, the average and the percentage graphs
and then passing the values to the after ignition phase to calculate the average of the battery after
ignition and plot the graph of all the stages
"""

from utilities import valuesAfter, valuesBefore, valuesIgnittion




fuel = input("is the car diesel or petrol powered?\nPlease enter 'd' for diesel or 'p' for petrol\n")
if str(fuel) == 'd': #if the car is diesel the mpd is set to 1500
    mpd = 1500
elif str(fuel) == 'p': #if the car is petrol the mpd is set to 1000
    mpd = 1000
else: #if anything else than d or p is inserted the program terminates
    print("please restart the process when you are ready to complete the cycle")
    quit()
 
avgBefore = valuesBefore() #the program measures the level of the battery before ignition
    
var = input("are you ready to start the car? enter y to proceed ") #the program ask if you are ready to start the car

# if you say yes it measures the car battery for a certain time 
# and then measures the battery level after the car has started
# and generates all the reports'''
if str(var) == 'y': 
    avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4 = valuesIgnittion(mpd)
    valuesAfter(avgBefore, avgCylPeak1, avgCylPeak2, avgCylPeak3, avgCylPeak4, avgCyl1, avgCyl2, avgCyl3,avgCyl4)
else:
    print("please restart the process when you are ready to complete the cycle")