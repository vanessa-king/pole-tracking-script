# pole-tracking-script
For Vogel Lab. Tracks poles and measures features of proteins near poles.

Tracking Script  - Instructions on Use
Last Updated by Vanessa on Aug 18, 2017

Table of Contents:
	General Instructions
	Workflow of Code
		Kar9 Analysis
		Cin8 Analysis
	Parameters Library


General Instructions:

Download this “Tracking Script” folder and all its contents onto your desktop. Inside this Tracking Script folder is all of the macro and python scripts called by Fiji, and the Jupyter notebooks* for data manipulation. Drag and drop the “Start.ijm” macro file into Fiji and run.If you have created a folder just for your cell, after running all scripts you will be left with a cropped image of your cell, an “Old Pole Data” file that has sorted the raw data and includes only the tracks manually chosen as old, a “New Pole Data” file that has sorted the raw data and includes only the tracks manually chosen as new, a “2D Pole Distance Data” file that has the distance between your two poles, and a “Measurements” file that shows the protein intensities.

Note: Please ensure that after you have run all codes for a single cell that you close the “ROI Manager” window that pops up during the Fiji script before beginning your analysis on the next cell. Please also ensure that when you are given the option of where to create your cell folder, please select or create a folder on your desktop.

*Note: This requires running a Python (2.7) script on a Jupyter notebook. If you don’t already have access to Jupyter, download “Anaconda Python 2.7” from https://www.continuum.io/downloads. When you open Anaconda, it will give you several options of “My Applications” with which you can run Python code. Select Jupyter Notebook. This will open Jupyter’s “home” directory page where you can find the Python script from this folder and select it to open.


Workflow of code:

	1. “Start.ijm” Macro: Asks if you want to run the analysis for Kar9-like protein distributions or Cin8-like protein distributions. Based on answer, runs the appropriate next several scripts.

	Kar9 Analysis:

	2. “Macro.ijm” Macro: Asks you to open your image as either a ‘.nd’ file or as a z-projected and channel-merged ‘.tif’. If a ‘.nd’ is opened, with user guidance for which channel corresponds to which, creates a max z-project and merged ‘.tif’ for use later. Saves this new formed ‘.tif’ in the same folder that the ‘.nd’ came from originally. Once the code makes the ‘.tif’, or if a ’.tif’ is originally opened, continues on to ask you to draw a rectangle around your desired cell. Please note that it is best to ensure that the poles of your cell are well within the rectangle, since if the pole comes within 5 pixels of the edge of the rectangle, it will not be able to calculate the mean intensity on the green channel around the pole. The script then crops the image to this rectangle drawn by the user, and asks what the user would like to save it as and where. Note that you must save the cell in a folder on your desktop. The script then asks what fraction of the quality filter to apply to the image. This quality filter is a cut-off number that Trackmate decides by calculating the quality values of each point, then applying the Otsu threshold to the gaussian of all the quality values. It is recommended to apply a filter equal to half of the automatic quality filter chosen by Trackmate (i.e. 0.50). It then runs the “Part_1.py” script, followed by the “Part_2.py” script. It then splits the channels our original cropped image so that it can separately save the brightfield of the cell for use later in the Python Data Manipulation. It asks the user what frame they would like to view the brightfield on later.

	3. “Part_1.py” Jython Script: First runs a stunted version of TrackMate in order to utilize TrackMate’s automatic filtering, then relays this automatic filtering decision into the next run of TrackMate. Runs Trackmate fully on the cell using a user determined fraction of the automatic quality filter found in the first short run of TrackMate. TrackMate uses its DoG detector and Simple LAP tracker, which does not allow splitting or merging events and rather saves then all as separate objects. The script then saves required raw data for further manipulation as a “coordinates” file. Besides the quality spot filter, TrackMate parameters are set at: 
				Estimated blob diameter: 0.70 micron
				Threshold: 0.0
				Use median filter: yes
				Do sub-pixel localization: yes
				Linking max distance: 1.00 micron
				Gap closing max distance:	 1.00 micron
				Max frame gap: 3
				Track Duration: 100 seconds

	4. “Part_2.py” Jython Script: Uploads coordinates file and manipulates it into usable data.  Draws a circle with a radius of 5 pixels around each set of coordinates and saves them as ROIs. Uses Fiji’s ‘Measure’ feature to 	measure mean intensity of the pole. Will ask the user what measurements they want recorded. For Kar9 analysis, please only select ‘Mean Grey Value’. Records mean grey value in a “results” file.

	5. “Python Data Manipulation.ipynb” Jupyter Notebook: sorts and edits data until it is parseable. Calculates  distance between poles. Provides a diagnostic figure so that the user can understand which object is associated to which track. Saves an “Old Pole Data”, “New Pole Data”, and “Pole Distance Data” file. Note that some hardcoding is required throughout, as marked as the start of a hardcoding cell with “#HARDCODED!” and explained with comments. Thus, it is recommended that you run this program cell-by-cell by clicking ‘Shift-Enter’ on each cell, one at a time. 


	Cin8 Analysis: 

	2. “Macro Cin8.ijm” Macro:  Asks you to open your image as either a ‘.nd’ file or as a z-projected and channel-merged ‘.tif’. If a ‘.nd’ is opened, with user guidance for which channel corresponds to which, creates a max z-project and merged ‘.tif’ for use later. Saves this new formed ‘.tif’ in the same folder that the ‘.nd’ came from originally. Once the code makes the ‘.tif’, or if a ’.tif’ is originally opened, continues on to ask you to draw a rectangle around your desired cell. Please note that it is best to ensure that the poles of your cell are well within the rectangle, since if the pole comes within 5 pixels of the edge of the rectangle, it will not be able to calculate the mean intensity on the green channel around the pole. The script then crops the image to this rectangle drawn by the user, and asks what the user would like to save it as and where. The script then asks what fraction of the quality filter to apply to the image. This quality filter is a cut-off number that Trackmate decides by calculating the quality values of each point, then applying the Otsu threshold to the gaussian of all the quality values. It is recommended to apply a filter equal to half of the automatic quality filter chosen by Trackmate (i.e. 0.50). It then runs the “Part_1.py” script, then changed the line width setting to 2 pixels, followed by running the “Part_2_Cin8.py” script.  Once “Part_2_Cin8.py” is complete, it asks the user to select “List” on the Profiles window. This is necessary as manual coding of this was not obtainable. It then splits the channels our original cropped image so that it can separately save the brightfield of the cell for use later in the Python Data Manipulation Cin8. It asks the user what frame they would like to view the brightfield on later.

	3. “Part_1.py” Jython Script: exact same script as used in Kar9 Analysis. Please see description above.

	4. “Part_2_Cin8.py” Jython Script: Uploads coordinates file and manipulates it into usable data.  Looks for every time point where we have found at least two objects. Draws a line between the centre of each spot and saves them as ROIs. Uses the ROI Manager ‘Multi Plot’ function.

	5. “Python Data Manipulation Cin8.ipynb” Jupyter Notebook: sorts and edits data until it is parseable. Calculates  distance between poles. Provides a diagnostic figure so that the user can understand which object is associated to which track. Saves an “Old Pole Data”, “New Pole Data”, “2D Pole Distance Data”, and “Measurements” file. Note that some hardcoding is required throughout, as marked as the start of a hardcoding cell with “#HARDCODED!” and explained with comments. Thus, it is recommended that you run this program cell-by-cell by clicking ‘Shift-Enter’ on each cell, one at a time.  Note that for this Jupyter Notebook, a proper green channel diagnostic tool has not yet been made and thus it not currently a feature, even though the data is saved in a Measurements file.


Parameters Library: The following is a listing of all hard-coded parameters in the code and where they can be found.


Tracking:

	Do Subpixel Localization : 				“Part_1.py”	Line 74 & 112            ‘DO_SUBPIXEL_LOCALIZATION’ : True,
	Estimated spot radius : 				“Part_1.py”	Line 75 & 113            ‘RADIUS’ : 0.350,
	Threshold : 						“Part_1.py”	Line 77 & 115            ‘THRESHOLD’ : 0.0,
	Linking maximum distance(microns):  	“Part_1.py”	Line 81 & 127            settings.trackerSettings[‘LINKING_MAX_DISTANCE’] = 1.000
	Gap-closing maximum distance(microns):  “Part_1.py”	Line 82 & 128            settings.trackerSettings[‘GAP_CLOSING_MAX_DISTANCE’] = 1.000
	Maximum frame gap : 				“Part_1.py”	Line 83 & 129            settings.trackerSettings[‘MAX_FRAME_GAP’] = 3
	Track duration filter : 					“Part_1.py”	Line 134                     filter3 = FeatureFilter(’TRACK_DURATION’, 100, True)


Kar9:	

	Circle radius : 						“Part_2.py”	Line 102                     rm.addRoi(ij.gui.OvalRoi( x[i] - 5, y[i] - 5, 10, 10 )) ,  (Note: blue must be double the radius wanted)

Cin8:
	Line width drawn between poles : 	“Macro Cin8.ijm”	Line 114                     run(“Line Width…”, “line=2”)

