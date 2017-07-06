# pole-tracking-script
For Vogel Lab. Tracks poles and measures features of proteins near poles.

Instructions on Use:
July 4, 2017

Download all files in a folder titled "Tracking Script" onto your desktop. Leave the Jython scripts inside their folder. This includes the macro for Fiji, all of the python scripts called by Fiji, and the Jupyter notebook for data manipulation. Drag and drop the “Run This.ijm” macro file into Fiji and run. Only select “Mean Grey value” when it asks you what you’d like to measure. Open “Python Data Manipulation.ipynb” as a Jupyter notebook*. Note that some hardcoding is required throughout, as marked as the start of a hardcoding cell with “#HARDCODED!” and explained with comments. Thus, it is recommended that you run this program cell-by-cell by clicking ‘Shift-Enter’ on each cell, one at a time. Please ensure that after you have run all codes for a single cell that you close the “ROI Manager” window that pops up during the Fiji script before beginning your analysis on the next cell. If you have created a folder just for your cell, after running all scripts you will be left with:

	1. The cropped image of your cell
	2. The raw coordinates and mean intensity of the poles in a “coordinates” file
	3. The raw measurements on the GFP channel in a “results” file
	4. An “Old Pole Data” file that has sorted the raw data and includes only the tracks manually chosen as old.
	5. A “New Pole Data” file that has sorted the raw data and includes only the tracks manually chosen as new.
	6. A “Pole Distance Data” file that has the distance between your two poles


Overview of what each script does:

	“Run This.ijm” - Leads user through selecting image, cropping image, saving cropped image in a 	folder of their choosing (as well as all addition files associated with this cell). Calls Jython scripts 	to track on this cropped image.

	“Part_1.py” - Runs Trackmate on the cell using its Simple LAP tracker, and saves required raw data for further manipulation as a “coordinates” file

	“Part_2.py” - Upload coordinates, saves them as ROIs, and uses Fiji’s ‘Measure’ feature to 	measure mean intensity of the pole. Records in a “results” file

	“Python Data Manipulation.ipynb”  - sorts and edits data until it is parseable. Calculates 	distance between poles. Provides a diagnostic figure so that the user can understand which object is associated to which track. Saves an “Old Pole Data”, “New Pole Data”, “Pole Distance Data”, and “Pole Symmetry Index” file. 


*Note: This requires running a Python (2.7) script on a Jupyter notebook. If you don’t already have access to Jupyter, download “Anaconda Python 2.7” from https://www.continuum.io/downloads. When you open Anaconda, it will give you several options of “My Applications” with which you can run Python code. Select Jupyter Notebook. This will open Jupyter’s “home” directory page where you can find the Python script from this folder and select it to open.
