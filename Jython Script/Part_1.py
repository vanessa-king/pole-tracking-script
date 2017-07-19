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
import fiji.plugin.trackmate.features.track.TrackBranchingAnalyzer as TrackBranchingAnalyzer
import ij.plugin.filter.Analyzer
import ij.plugin.frame.RoiManager
import ij.gui.OvalRoi
import fiji.plugin.trackmate.features.FeatureFilter
import fiji.plugin.trackmate.features.FeatureAnalyzer
import fiji.plugin.trackmate.features.spot
import fiji.plugin.trackmate.features.spot.SpotContrastAndSNRAnalyzerFactory as SpotContrastAndSNRAnalyzerFactory
import fiji.plugin.trackmate.io.TmXmlReader
import fiji.plugin.trackmate.action.ExportTracksToXML
import fiji.plugin.trackmate.io.TmXmlWriter
import fiji.plugin.trackmate.features.ModelFeatureUpdater
import fiji.plugin.trackmate.features.SpotFeatureCalculator
import fiji.plugin.trackmate.features.spot.SpotContrastAndSNRAnalyzer as SpotContrastAndSNRAnalyzer
import fiji.plugin.trackmate.features.spot.SpotIntensityAnalyzerFactory as SpotIntensityAnalyzerFactory
import fiji.plugin.trackmate.features.track
import fiji.plugin.trackmate.features.track.TrackSpeedStatisticsAnalyzer as TrackSpeedStatisticsAnalyzer
import fiji.plugin.trackmate.util.TMUtils
import csv
import os
from fiji.plugin.trackmate.providers import DetectorProvider
from fiji.plugin.trackmate.providers import TrackerProvider
from fiji.plugin.trackmate.providers import SpotAnalyzerProvider
from fiji.plugin.trackmate.providers import EdgeAnalyzerProvider
from fiji.plugin.trackmate.providers import TrackAnalyzerProvider
import fiji.plugin.trackmate.action.ExportStatsToIJAction as ExportStatsToIJAction
import fiji.plugin.trackmate.features.track.TrackAnalyzer

#Script Part 1B
#Outline:
#1. Open data
#2. Set Image properties
#3. Configure detector
#4. Configure spot filters
#5. Configure LAP Tracker
#6. Run trackmate
#7. Get spot or track features
#8. Save log as a parsable data set

#1. 
# Open data
the_input = getArgument()
the_list = the_input.rpartition(" ")
image = the_list[0]
threshold = float(the_list[2])

imp = IJ.openImage(image)
imp.show()

#2.
model = Model()
model.setLogger(Logger.IJ_LOGGER)
settings = Settings()
settings.setFrom(imp)

#3.
# Configure detector
settings.detectorFactory = DogDetectorFactory()
settings.detectorSettings = { 
    'DO_SUBPIXEL_LOCALIZATION' : True,
    'RADIUS' : 0.350,
    'TARGET_CHANNEL' : 1,
    'THRESHOLD' : 0.0,
    'DO_MEDIAN_FILTERING' : True,
}  

#4. 
# Configure spot filters
filter2 = FeatureFilter('MEAN_INTENSITY', threshold-300, True)
settings.addSpotFilter(filter2)

# Configure tracker
settings.trackerFactory = SparseLAPTrackerFactory()
settings.trackerSettings = LAPUtils.getDefaultLAPSettingsMap()
#settings.trackerSettings['ALLOW_TRACK_SPLITTING'] = True
settings.trackerSettings['LINKING_MAX_DISTANCE'] = 1.000
settings.trackerSettings['GAP_CLOSING_MAX_DISTANCE'] = 1.000
settings.trackerSettings['MAX_FRAME_GAP'] = 3
# Configure track analyzers
settings.addTrackAnalyzer(TrackDurationAnalyzer())
settings.addTrackAnalyzer(TrackBranchingAnalyzer())
# Configure track filters
filter3 = FeatureFilter('TRACK_DURATION', 100,  True)
settings.addTrackFilter(filter3)

settings.addSpotAnalyzerFactory(SpotIntensityAnalyzerFactory())
settings.addSpotAnalyzerFactory(SpotContrastAndSNRAnalyzerFactory())
settings.addTrackAnalyzer(TrackSpeedStatisticsAnalyzer())

#5.
# Running trackmate
trackmate = TrackMate(model, settings)
ok = trackmate.checkInput()
if not ok:
    sys.exit(str(trackmate.getErrorMessage()))
ok = trackmate.process()
if not ok:
    sys.exit(str(trackmate.getErrorMessage())) 
# Display results of tracks on the image
selectionModel = SelectionModel(model)
displayer =  HyperStackDisplayer(model, selectionModel, imp)
displayer.render()
displayer.refresh()

#6.
#get spot and track features
# The feature model, that stores edge and track features.
fm = model.getFeatureModel()
for id in model.getTrackModel().trackIDs(True):
    # Fetch the track feature from the feature model.
    v = fm.getTrackFeature(id, 'TRACK_MEAN_SPEED')
    model.getLogger().log('0.0,0.0,0.0,0.0')
    track = model.getTrackModel().trackSpots(id)
    for spot in track:
        # Fetch spot features directly from spot. 
        x=spot.getFeature('POSITION_X')
        y=spot.getFeature('POSITION_Y')
        t=spot.getFeature('FRAME')
        q=spot.getFeature('QUALITY')
        snr=spot.getFeature('SNR') 
        mean=spot.getFeature('MEAN_INTENSITY')
        model.getLogger().log(str(t)+','+str(x)+','+str(y)+','+str(mean))

#7.
#saving log as a txt file on desktop, then reading txt and rewriting as csv.
IJ.selectWindow("Log")
badname = image
filename = badname.replace(".tif", "")
IJ.saveAs("Text", filename+"_coordinates");
IJ.run("Close");