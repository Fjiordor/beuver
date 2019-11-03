print("Hello World")

import os
import re

import matplotlib.pyplot as plt
import numpy as np
import beutools.Datahandling as dt

# Globals
rawColumn0 = []
rawColumn1 = []
rawColumn2 = []


# functions
def convertToNumber(myString: str) -> float:
    if myString == 'NaN':
        return 0
    else:
        return float(myString.replace(",", "."))

def parsefile(myFile) -> None:
    lines = myFile.readlines()
    rawColumn0.clear()
    rawColumn1.clear()
    rawColumn2.clear()
    for line in lines:
        if line[0] is not "#":
            line = re.split(r'\t+', line)
            rawColumn0.append(convertToNumber(line[0]))
            rawColumn1.append(convertToNumber(line[1]))
            rawColumn2.append(convertToNumber(line[2]))
    return


def doCalculationsforFile(readFile, saveName: str) -> None:
    # Read raw data
    inFile = open(dt.createReadPath(readFile), "r")
    dt.createSaveFile(saveName)
    parsefile(inFile)

    # Plot and save raw data
    plt.plot(rawColumn1, rawColumn2, 'k')
    plt.title('raw data')
    plt.xlabel('position in mm')
    plt.ylabel('measured value in v')
    plt.savefig(dt.createSavePath(saveName + 'RawPlot.svg'))
    plt.show()

    # switch to loacal Data to work with it
    index = list(map(lambda value: int(value), rawColumn0))
    xAxis = rawColumn1
    yAxis = rawColumn2

    # Reducenoise
    compFactor = 100
    yAxis = list(np.convolve(yAxis, np.ones((compFactor,)) / compFactor, mode='valid'))
    dt.addToSaveFile(saveName, "Es wurde mit dem Komprimierungsfaktor " + str(compFactor) + ' kompriemiert')
    compFactor = None
    del compFactor

    # debug
    print(len(xAxis))
    print(len(yAxis))

    # Ugly Hack of doom to solve issues with differing lengths.
    if len(xAxis) > len(yAxis):
        xAxis = xAxis[:len(yAxis)]
    elif len(xAxis) < len(yAxis):
        yAxis = yAxis[:len(xAxis)]

    # debug
    print(len(xAxis))
    print(len(yAxis))

    # find Maximum
    maxValue = max(yAxis)
    maxIndex = yAxis.index(maxValue)
    dt.addToSaveFile(saveName, '\nmaximum Value: ' + str(maxValue) + 'V at ' + str(xAxis[maxIndex]) + 'mm')

    # center on maximum
    xOffset = xAxis[maxIndex]
    xAxis = list(map(lambda value: value - xOffset, xAxis))

    # draw new plot
    plt.clf()
    plt.plot(xAxis, yAxis, 'k')
    plt.title('adjusted plot')
    plt.xlabel('position in mm')
    plt.ylabel('measured value in v')
    plt.savefig(dt.createSavePath(saveName + 'adjustedPlot.svg'))
    plt.show()

    # find minima
    minima = []
    for x in index:
        try:
            if yAxis[x] <= yAxis[x - 1] and yAxis[x] <= yAxis[x + 1]:
                minima.append(x)
        except IndexError:
            pass

    # (np.gradient(np.sign(np.gradient(yAxis))) > 0).nonzero()[0] + 1  # local min
    print('Minima: ' + str(minima))

    # draw new plot with minima added
    plt.clf()
    plt.plot(xAxis, yAxis, 'k')
    plt.title('adjusted plot with minima pre cleanup')
    plt.xlabel('position in mm')
    plt.ylabel('measured value in v')
    for mindex in minima:
        myX = xAxis[mindex]
        plt.axvline(x=myX)
    plt.savefig(dt.createSavePath(saveName + 'minimaPlot.svg'))
    plt.show()

    # minima cleanup
    minimaList = []
    for mindex in minima:
        minimaList.append([mindex, xAxis[mindex]])
    minimaGroups = [[]]
    groupcounter = 0
    minimaGroups[0].append(minimaList[0])
    for x in range(len(minimaList) - 1):
        if abs(minimaList[x][1] - minimaList[x + 1][1]) < 1:
            minimaGroups[groupcounter].append(minimaList[x + 1])
        else:
            groupcounter += 1
            minimaGroups.append([])
            minimaGroups[groupcounter].append(minimaList[x + 1])

    for group in minimaGroups:
        for touple in group:
            touple.append(yAxis[touple[0]])

    minimaPreCleaned = []
    for lista in minimaGroups:
        lowest_number = False

        for listb in lista:
            if not lowest_number:
                lowest_number = listb[2]
                selected_list = listb
            else:
                if listb[2] < lowest_number:
                    lowest_number = listb[2]
                    selected_list = listb
        # noinspection PyUnboundLocalVariable
        minimaPreCleaned.append(selected_list)  # this could be changed to selected_list.copy() if need be
    print(len(minimaPreCleaned))
    minimumpostCleanup = []
    for minimum in minimaPreCleaned:
        try:
            if minimum[2] <= yAxis[minimum[0] - 10] and minimum[2] <= yAxis[minimum[0] + 10]:
                minimumpostCleanup.append(minimum)
        except IndexError:
            pass

    print(len(minimumpostCleanup))

    # postcleanup plot

    plt.clf()
    plt.plot(xAxis, yAxis, 'k')
    plt.title('adjusted plot with minima post cleanup')
    plt.xlabel('position in mm')
    plt.ylabel('measured value in v')
    plt.xticks(np.arange(-60, 60, 10.0))
    for minimum in minimumpostCleanup:
        myX = xAxis[minimum[0]]
        plt.axvline(x=myX)
    plt.savefig(dt.createSavePath(saveName + 'minimaPlotPostCleanup.svg'))
    plt.show()

    dt.addToSaveFile(saveName, 'Gefundene minima: \n' + str(minimumpostCleanup))


doCalculationsforFile("24_09_2019_13_10_19_GR4_GITTER_18500.dat", 'Gitter_')
