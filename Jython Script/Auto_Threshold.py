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
import fiji.plugin.trackmate.Spot
import fiji.plugin.trackmate.features.track.TrackAnalyzer

imp = IJ.openImage("/Users/vanessa/Desktop/a/Cell1_13.tif")
imp.show()

model = Model()
settings = Settings()
settings.setFrom(imp)
settings.addSpotAnalyzerFactory(SpotIntensityAnalyzerFactory())
trackmate = TrackMate(model, settings)
trackmate.execDetection()
trackmate.execInitialSpotFiltering()
trackmate.computeSpotFeatures(1);
trackmate.execSpotFiltering(1);

spotFeatures = model.getFeatureModel().getSpotFeatures()

spotFeatureValues = model.getFeatureModel().getSpotFeatureValues()

featureValues = spotFeatureValues.get('QUALITY')

optimalMeanIntensity = fiji.plugin.trackmate.util.TMUtils.otsuThreshold(featureValues)

