from fiji.plugin.trackmate import Model
from fiji.plugin.trackmate import Settings
from fiji.plugin.trackmate import TrackMate
from fiji.plugin.trackmate import SelectionModel
from fiji.plugin.trackmate import Logger
from fiji.plugin.trackmate.detection import DogDetectorFactory, LogDetectorFactory
from fiji.plugin.trackmate.tracking.sparselap import SparseLAPTrackerFactory
from fiji.plugin.trackmate.tracking import LAPUtils
from ij import *
from ij import IJ, ImagePlus, ImageStack
import ij.measure
import ij.measure.ResultsTable
import fiji.plugin.trackmate.visualization.hyperstack.HyperStackDisplayer as HyperStackDisplayer
import fiji.plugin.trackmate.features.FeatureFilter as FeatureFilter
import sys
import fiji.plugin.trackmate.features.track.TrackDurationAnalyzer as TrackDurationAnalyzer
import ij.plugin.filter.Analyzer
import ij.plugin.frame.RoiManager
import ij.gui.OvalRoi
import fiji.plugin.trackmate.features.FeatureFilter
import fiji.plugin.trackmate.features.FeatureAnalyzer
import fiji.plugin.trackmate.features.spot
#import fiji.plugin.trackmate.features.spot.SpotContrastandSNRAnalyzerFactory
import fiji.plugin.trackmate.io.TmXmlReader
import fiji.plugin.trackmate.action.ExportTracksToXML
import fiji.plugin.trackmate.io.TmXmlWriter
import fiji.plugin.trackmate.features.ModelFeatureUpdater
import fiji.plugin.trackmate.features.SpotFeatureCalculator
import fiji.plugin.trackmate.features.spot.SpotContrastAndSNRAnalyzer
import fiji.plugin.trackmate.features.spot.SpotIntensityAnalyzerFactory
import fiji.plugin.trackmate.features.track
import fiji.plugin.trackmate.features.track.TrackSpeedStatisticsAnalyzer
import fiji.plugin.trackmate.util.TMUtils
import csv
from ij.gui import *
from ij.process import *
from ij.measure import *
from ij.util import *
from ij.plugin import *
from ij.plugin.filter import *
from ij.plugin.frame import *
from ij.io import *
from java.lang import *
from java.awt import *
from java.awt.image import *
from java.awt.geom import *
from java.util import *
from java.io import *
import ij.gui.Overlay
import ij.plugin.frame.RoiManager
import os

#Script Part 2
#Outline: 
#1. Open data
#2. Upload xyzt coordinates of spots from tracking of poles
#3. Draw circles around each spot at each frame and save as ROI
#4. Save measured data inside each circle at each frame


#1.
# Open data
the_input = getArgument()
the_list = the_input.rpartition(" ")
image = the_list[0]
imp = IJ.openImage(image)
imp.show()
dimensions = float(the_list[2])

#2. Uploading coordinates, converting data from csv to arrays of floats.
filename = image.replace(".tif", "")
raw = csv.reader(open(filename+"_coordinates.txt"), delimiter = ",", quotechar = '|')
rawdata = list(raw)
del rawdata [:16]
coordinates = [0 for index in range(0,4)]
coordinates = [[row[i] for row in rawdata] for i in range(len(rawdata[0]))]
t = coordinates[0]; 
for i in range(len(t)):
	t[i] = float(t[i])
x = coordinates[1]; 
for i in range(len(x)):
	x[i] = float(x[i]) * dimensions
y = coordinates[2];
for i in range(len(y)):
	y[i] = float(y[i]) * dimensions
m = coordinates[3];
for i in range(len(m)):
	m[i] = float(m[i])

#3. 
rm = RoiManager.getInstance()
#prompt Set Measurements GUI
IJ.run("Set Measurements...")
if (rm==None):
	rm = RoiManager()

for i in range(len(t)):
	if x[i] != 0:
		#imp.setPosition switches to GFP channel and sets frame for each ROI
		imp.setPosition(2, 1, int(t[i])+1)
		#adds an oval ROI centered around coordinates
		rm.addRoi(ij.gui.OvalRoi(x[i]-5, y[i]-5, 10, 10))
		
#measures requested data on all ROIs
rm.runCommand(imp,"Measure")

#4. Saving measured data to desktop
IJ.selectWindow("Results")
IJ.saveAs("Text", filename+"_results")
IJ.run("Close")