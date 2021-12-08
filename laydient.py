#! python3

import sys
import os
import random
import math

inputFilename = sys.argv[1]
outputFilename = os.path.splitext(inputFilename)[0] + "-Gradient" + os.path.splitext(inputFilename)[1]

toolsToUse=[0,1]

dithering = [
	[0,0,0,0,0,0,0,0],
	[0,0,0,0,1,0,0,0],
	[1,0,0,0,1,0,0,0],
	[1,0,0,1,0,0,1,0],
	[1,0,1,0,1,0,1,0],
	[1,0,1,0,1,0,1,1],
	[0,1,1,1,0,1,1,1],
	[1,1,1,1,0,1,1,1],
	[1,1,1,1,1,1,1,1]
]

weighting = 0

def openFiles():
	print('Reading input gcode… ', end='')
	global inputFile
	inputFile = open(inputFilename, "r")
	print('done.')


def countLayers():
	totalLayers = 0
	print('Finding layer changes… ', end='')
	for line in inputFile:
		if 'LAYER_CHANGE' in line:
			totalLayers+=1
	print(totalLayers, "found.")
	return totalLayers


# def generateGradient(totalLayers): # TABLED
# 	layerGroups = totalLayers / len(dithering[0])
# 	layerGroupsFloor = math.floor(layerGroups)
# 	print('Generating gradient… ', end='')
# 	gradientColour = []
# 	for layerGroup in range(layerGroupsFloor):
# 		chanceOfSecondary = layerGroup / layerGroups
# 		ditheredIndex = math.floor(chanceOfSecondary * len(dithering))
# 		for bit in dithering[ditheredIndex]:
# 			gradientColour.append(bit)
# 	print(len(gradientColour), 'gradient steps generated.')
# 	return gradientColour



# def generateGradient(totalLayers): # RANDOMISED
# 	weighting = 0
# 	gradientColour = []
# 	for layer in range(totalLayers):
# 		chanceOfSecondary = layer / totalLayers
# 		if random.random() > chanceOfSecondary:
# 			gradientColour.append(0)
# 		else:
# 			gradientColour.append(1)
# 	return gradientColour


def generateGradient(totalLayers): # WEIGHTED
	print('Generating gradient steps… ', end='')
	global weighting
	changeThreshold = 1
	gradientColour = []
	for layer in range(totalLayers):
		chanceOfSecondary = layer / totalLayers
		weighting += chanceOfSecondary
		if weighting >= changeThreshold:
			gradientColour.append(1)
			weighting -= changeThreshold
		else:
			gradientColour.append(0)
	print(len(gradientColour), 'generated.')
	return gradientColour


def previewGradient(gradient, totalLayers):
	print('Gradient Preview:')
	for bit in gradient:
		if bit:
			print('◻︎', end='')
		else:
			print('◼︎', end='')
	print('')


def generateGcode(gradient):
	toolchangeCount = 0
	outputFile = open(outputFilename, "wb")
	inputFile.seek(0)
	print('Writing', outputFilename, '…')
	for line in inputFile:
		outputFile.write(line.encode('utf-8'))
		if 'Layer: ' in line:
			if toolchangeCount < len(gradient):
				toolchange = "G10 ; retract\nT{0} ; toolchange\nG11 ; unretract\n".format(toolsToUse[gradient[toolchangeCount]])
				outputFile.write(toolchange.encode('utf-8'))
				toolchangeCount +=1
	outputFile.close()


def closeFiles():
	inputFile.close()

print('\n\n=======================\n      LAYDIENT!\n=======================')
openFiles()
totalLayers = countLayers()
gradient = generateGradient(totalLayers)
previewGradient(gradient, totalLayers)
generateGcode(gradient)
closeFiles()
print('Done!')
