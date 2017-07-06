title_1 = "Image Selection";
msg_1 = "Please open your image.";
waitForUser(title_1, msg_1);
open();
myImageID = getImageID();
setTool("rectangle");
title_2 = "ROI Selection";
msg_2 = "Please draw rectangle around a cell then click OK.";
waitForUser(title_2, msg_2);
selectImage(myImageID);
if (selectionType() != 0)                           
exit("You did not draw a rectangle.");
run("Crop");
newImageID = getImageID();
cell = getString("What would you like to save this cell as?", "Cell1");
selectImage(newImageID);
title_2 = "Directory";
msg_2 = "Please select or make a folder for this cell.";
waitForUser(title_2, msg_2);
directory = getDirectory("Choose a Directory");
saveAs("Tiff", directory+cell+".tif");
run("Close");

jythonText_1 = File.openAsString(getDirectory("home") +"Desktop/Tracking Script/Jython Script/Part_1.py");
jythonText_2 = File.openAsString(getDirectory("home") +"Desktop/Tracking Script/Jython Script/Part_2.py");

call("ij.plugin.Macro_Runner.runPython", jythonText_1, directory+cell+".tif");
call("ij.plugin.Macro_Runner.runPython", jythonText_2, directory+cell+".tif");

thenewImageID = getImageID();
selectImage(thenewImageID);
run("Split Channels");
selectWindow("C1-"+cell+".tif");
run("Rotate 90 Degrees Left");
run("Flip Horizontally");
saveAs("PNG", directory+cell+"_RFP.png");
run("Close");
selectWindow("C2-" +cell+".tif");
run("Close");
