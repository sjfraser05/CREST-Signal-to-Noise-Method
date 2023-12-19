import os
import glob
import csv
import pickle
import inspect
import matplotlib.pyplot as plt
import numpy as np
import easygui
from natsort import natsorted
import readDataFile as rdf
import spc

class Analyte:
  def __init__(self, name, peakLoc, lowBound, highBound, bgWidth):
    self.name = name
    self.peakLoc = peakLoc
    self.lowBound = float(lowBound)
    self.highBound = float(highBound)
    self.bgWidth = int(bgWidth)

msg ="spc or csv?"
title = "Choose file type"
choices = ["*.spc", "*.csv"]
choice = easygui.choicebox(msg, title, choices)

if choice == None:
    easygui.buttonbox(msg='Press OK to Exit', title='SNR Calc', choices=["OK"])
    exit()

insMsg ="Tornado or other?"
institle = "Choose instrument type"
inschoices = ["Tornado HFPP", "other"]
inschoice = easygui.choicebox(insMsg, institle, inschoices)

if inschoice == None:
    easygui.buttonbox(msg='Press OK to Exit', title='SNR Calc', choices=["OK"])
    exit()

directory = easygui.diropenbox()
if directory == None:
    easygui.buttonbox(msg='Press OK to Exit', title='SNR Calc', choices=["OK"])
    exit()
else:
    print("directory found")
    os.chdir(directory)
    dirList = glob.glob(choice)
    dirList = natsorted(dirList)
    print("directory parsed")

matMsg ="Please choose an analyte."
matTitle = "Choose analyte type"
matChoices = ["cyclohexane", "isopropyl alcohol", "polystyrene", "saved custom", "new custom"]
SampleChoice = easygui.choicebox(matMsg, matTitle, matChoices)

if SampleChoice == None:
    easygui.buttonbox(msg='Press OK to Exit', title='SNR Calc', choices=["OK"])
    exit()

if SampleChoice == "cyclohexane":
    peakMsg = "Choose cyclohexane peak"
    peakTitle = "SNR Calculation"
    peakChoices = [801.3, 1028.3, "CH Stretch"]
    peakChoice = easygui.choicebox(peakMsg, peakTitle, peakChoices)
    bgWidth = 20
    MatChoice = Analyte(SampleChoice, peakChoice, float(peakChoice) - 75, float(peakChoice) + 75, 20)


    if peakChoice == "CH Stretch":
        MatChoice = Analyte(SampleChoice, peakChoice, 2780, 3080, 20)

elif SampleChoice == "isopropyl alcohol":
    peakMsg = "Choose isopropyl alcohol peak"
    peakTitle = "SNR Calculation"
    peakChoices = [819.9, 1029.0]
    peakChoice = easygui.choicebox(peakMsg, peakTitle, peakChoices)
    MatChoice = Analyte(SampleChoice, peakChoice, float(peakChoice) - 50, float(peakChoice) + 50, 20)

elif SampleChoice == "polystyrene":
    peakMsg = "Choose polystyrene peak"
    peakTitle = "SNR Calculation"
    peakChoices = [620.9, 1001.0, 1600.0]
    peakChoice = easygui.choicebox(peakMsg, peakTitle, peakChoices)
    MatChoice = Analyte(SampleChoice, peakChoice, float(peakChoice) - 50, float(peakChoice) + 50, 20)

elif SampleChoice == "saved custom":
    try:
        programPath = os.path.expanduser('~\\SNRcalc Data')
        os.chdir(programPath)
        saveCustDirList = glob.glob("*.pkl")
        peakMsg = "Choose saved custom material and peak"
        peakTitle = "SNR Calculation"
        peakChoices = saveCustDirList
        peakChoice = easygui.choicebox(peakMsg, peakTitle, peakChoices)
        with open(peakChoice, 'rb') as input:
            MatChoice = pickle.load(input)
        os.chdir(directory)
    except:
        easygui.buttonbox(msg='Press OK to exit', title='No saved custom materials found', choices=["OK"])
        exit()

elif SampleChoice == "new custom":

    peakMsg = "Enter your material information"
    peakTitle = "SNR Calculation"
    fieldNames = ["Material", "Peak Location", "Peak area start","Peak area end","Background width"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = easygui.multenterbox(peakMsg, peakTitle, fieldNames)
    MatChoice = Analyte(fieldValues[0], fieldValues[1], fieldValues[2], fieldValues[3], fieldValues[4])

    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break  # no problems found
        fieldValues = easygui.multenterbox(errmsg, title, fieldNames, fieldValues)

nList = len(dirList)
areaList = np.zeros(1)

# Initialize plot
fig, (ax1, ax2, ax3) = plt.subplots(3,2)
ax1 = plt.subplot(221)
ax2 = plt.subplot(222)
ax3 = plt.subplot(212)
colors = plt.cm.rainbow(np.flip(np.linspace(0,1,nList)))
bgWidth2 = MatChoice.bgWidth

for count, iFile in enumerate(dirList):
    print(str(np.round((count/len(dirList)*100), 2)) + "% Complete")

    try:
        # Read spectral data file
        x1, y1 = rdf.readDataFile(iFile)
        if inschoice == "other":
            bgWidth2 = MatChoice.bgWidth / (x1[2] - x1[1])

        # Finds the index for the peaklocs selected
        idx1 = (np.abs(x1 - MatChoice.lowBound)).argmin()
        idx2 = (np.abs(x1 - MatChoice.highBound)).argmin()
        # Average yvalues from 20 points before idx1 and 20 points after idx2
        bg1 = np.mean(y1[idx1-bgWidth2:idx1])
        bg2 = np.mean(y1[idx2:idx2+bgWidth2])

        # Insert the averaged value at idx1 and idx2
        y2 = np.insert(y1, idx1, bg1)
        y2 = np.delete(y2, (idx1+1), axis=0)

        y2 = np.insert(y2, idx2, bg2)
        y2 = np.delete(y2, (idx2+1), axis=0)

        # Calculate linear baseline used to subtract from each spectrum
        interpolant = np.interp([x1[idx1], x1[idx2]], x1, y2)
        coefficients = np.polyfit([x1[idx1], x1[idx2]], interpolant, 1)

        # Area calculation after baseline subtraction
        area = np.sum(y1[idx1:idx2] - ((x1[idx1:idx2] * coefficients[0]) + coefficients[1]))
        mody1 = y1[idx1:idx2] - ((x1[idx1:idx2] * coefficients[0]) + coefficients[1])
        areaList = np.vstack((areaList, area))
        ax2.plot(x1[idx1-bgWidth2:idx2+bgWidth2], (y1[idx1-bgWidth2:idx2+bgWidth2] - (x1[idx1-bgWidth2:idx2+bgWidth2]*coefficients[0] + coefficients[1])))

    except:
        print("Failed to read " + str(iFile))

#remove the empty row from areaList, and calculate SNR, RSD
areaList = np.delete(areaList, (0), axis=0)
print("Variance is " + str(np.var(areaList)))
SNR = np.mean(areaList) / np.std(areaList)
RSD = np.std(areaList) / np.mean(areaList) * 100

#Add vertical plot lines designating abackground and area calculation
ax2.axvline(x=MatChoice.lowBound, color='b', linestyle='--' )
ax2.text(MatChoice.lowBound, max(mody1)/1.5, ' Area start', fontsize=7)
ax2.axvline(x=MatChoice.highBound, color='b', linestyle='--')
ax2.text(MatChoice.highBound, max(mody1)/1.5, 'Area end ', ha='right', fontsize=7)
ax2.axvline(x=MatChoice.lowBound-bgWidth2, color='r', linestyle='--')
ax2.axvline(x=MatChoice.highBound+bgWidth2, color='r', linestyle='--')
ax2.text(MatChoice.lowBound-bgWidth2, max(mody1)/1.6, ' BG', fontsize=7)
ax2.text(MatChoice.highBound+bgWidth2, max(mody1)/1.6, 'BG ', ha='right', fontsize=7)

# Add title and axis names
ax1.set_title('Peak area variance for ' + str(MatChoice.name) + ' ' + str(MatChoice.peakLoc) + ' $cm^{-1}$ band' + '\n'
                + r'$\bf{RSD = ' + str(round(RSD,3)) + '%, SNR = ' + str(round(SNR,3)) + '}$', fontsize = 8)
ax3.set_title('Peak area variance trend ' + str(MatChoice.name) + ' ' + str(MatChoice.peakLoc) + ' $cm^{-1}$ band with '
              + ' ms exposures): RSD = ' + str(round(RSD, 3)) + '%, SNR = ' + str(round(SNR, 3)), fontsize=8)
ax2.set_title(str(MatChoice.peakLoc) + ' $cm^{-1}$ band for ' + str(MatChoice.name) , fontsize=8)

ax1.set(xlabel = 'Boxplot Distribution of Peak Areas', ylabel = 'Peak Area') #xlabel = 'Spectrum #',
ax2.set(xlabel = 'Raman Shifts ($cm^{-1}$)', ylabel = 'Counts')

ax2.yaxis.tick_right()
ax2.yaxis.set_label_position("right")

ax3.set(xlabel = 'Spectrum #', ylabel = 'Peak Area')
ax3.axhline(y=np.mean(areaList)-np.std(areaList), color='r', linestyle='--' )
ax3.axhline(y=np.mean(areaList)+np.std(areaList), color='r', linestyle='--' )
ax3.text(1, ((np.mean(areaList)-np.std(areaList))*0.90), 'Standard Deviation', fontsize=7)

areaRange = range(1,len(areaList)+1)
ax3.scatter(areaRange, areaList, color ='b', marker='o')
ax1.boxplot(areaList)
fig.subplots_adjust(hspace = 0.7)
fig.set_size_inches(18.5, 10.5)
plt.show()

# Save graphical figure
fig.savefig(directory + '\\' + 'SNR calc result ave ' + directory.split('\\')[-1] + '.tif')

# Writing to a CSV file
dataForCSV = np.column_stack((dirList, areaList))
with open(directory + '\\' + 'SNR calc result ' + directory.split('\\')[-1] + '.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerows(dataForCSV)

if SampleChoice == "new custom":
    saveMsg ="Do you want to save your custom peak choice?"
    saveTitle = "Custom analysis"
    saveChoices = ["Yes", "No"]
    saveChoice = easygui.choicebox(saveMsg, saveTitle, saveChoices)
else:
    saveChoice = "No"

if saveChoice == None or saveChoice == "No":
    easygui.buttonbox(msg='Press OK to Exit', title='SNR Calc', choices=["OK"])
    exit()

else:
    # This will save the custom choice as a .pkl in the User directory under SNRcalc Data folder
    try:
        programPath = os.path.expanduser('~\\SNRcalc Data')
        os.chdir(programPath)
        pklFileName = str(MatChoice.name) + " " + str(MatChoice.peakLoc) + ".pkl"
        with open(pklFileName, 'wb') as output:
            pickle.dump(MatChoice, output, pickle.HIGHEST_PROTOCOL)
    except:
        programPath = os.path.expanduser('~')
        os.chdir(programPath)
        os.mkdir('SNRcalc Data')
        os.chdir('SNRcalc Data')
        pklFileName = str(MatChoice.name) + " " + str(MatChoice.peakLoc) + ".pkl"
        with open(pklFileName, 'wb') as output:
            pickle.dump(MatChoice, output, pickle.HIGHEST_PROTOCOL)


