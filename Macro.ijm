title_1 = "Image Selection";
msg_1 = "Please open your image as an '.nd' and select 'Split Channels', or as a pre-merged '.tif'.";
waitForUser(title_1, msg_1);
open();

image_name = getInfo("image.filename");
split_image_name= split(image_name, ".");
split_image_name_length = lengthOf(split_image_name);
image_type = split_image_name[split_image_name_length - 1];

if (image_type == "nd"){
	original_directory = getInfo("image.directory");
	title_2 = "RFP Channel";
	msg_2 = "Please select the image that corresponds to the RFP Channel.";
	waitForUser(title_2, msg_2);
	zredimage = getImageID();
	run("Z Project...", "projection=[Max Intensity] all");
	redimage = getTitle();
	redimageid = getImageID();
	selectImage(zredimage);
	run("Close");

	title_3 = "GFP Channel";
	msg_3 = "Please select the image that corresponds to the GFP Channel.";
	waitForUser(title_3, msg_3);
	zgreenimage = getImageID();
	run("Z Project...", "projection=[Max Intensity] all");
	greenimage = getTitle();
	greenimageid = getImageID();
	selectImage(zgreenimage);
	run("Close");

	title_4 = "BF Channel";
	msg_4 = "Please select the image that corresponds to the BF Channel.";
	waitForUser(title_4, msg_4);
	width = 0.;
	height = 0.;
	channels = 0.;
	slices = 0.;
	frames = 0.;
	getDimensions(width, height, channels, slices, frames);
	if(slices != 1){
		zbrightfieldid = getImageID();
		run("Z Project...", "projection=[Max Intensity] all");
		brightfield = getTitle();
		brightfieldid = getImageID();
		selectImage(zbrightfieldid);
		run("Close");
	}
	else{
		brightfield = getTitle();
		brightfieldid = getImageID();
	}
	run("Merge Channels...", "c1=["+redimage+"] c2=["+greenimage+"] c4=["+brightfield+"] keep");
	Stack.setDisplayMode("grayscale");
	Stack.setChannel(3);

	selectImage(redimageid);
	run("Close");
	selectImage(greenimageid);
	run("Close");
	selectImage(brightfieldid);
	run("Close");

	usable = getTitle();
	selectWindow(usable);
	saveAs("tiff", original_directory+"Merged.tif");
}

myImageID = getImageID();

setTool("rectangle");
waitForUser("ROI Selection", "Please draw rectangle around a cell then click OK");
selectImage(myImageID);
if (selectionType() != 0)                           
exit("You did not draw a rectangle.");
run("Crop");
newImageID = getImageID();
cell = getString("What would you like to save this cell as?", "Cell1");
selectImage(newImageID);
title_6 = "Directory";
msg_6 = "Please select or make a folder for this cell.";
waitForUser(title_6, msg_6);
directory = getDirectory("Choose a Directory");
saveAs("tiff", directory+cell+".tif");
info = getImageInfo();
split_info= split(info, ":");
good_info = split_info[5];
split_good_info = split(good_info, " ");
dimensions = split_good_info[0];

width = 0.;
height = 0.;
channels = 0.;
slices = 0.;
frames = 0.;
getDimensions(width, height, channels, slices, frames);

showText("Dimensions ", dimensions+" "+frames);
saveAs('text', directory+cell+"_dimensions.txt");
selectWindow(cell+".tif");
run("Close");
selectWindow(cell+"_dimensions.txt");
run("Close");

subtraction = getString("What fraction of the quality filter would you like to apply?", "0.50");


jythonText_1 = File.openAsString(getDirectory("home") +"Desktop/Tracking Script/Jython Script/Part_1.py");
jythonText_2 = File.openAsString(getDirectory("home") +"Desktop/Tracking Script/Jython Script/Part_2.py");

call("ij.plugin.Macro_Runner.runPython", jythonText_1, directory+cell+".tif "+subtraction);
call("ij.plugin.Macro_Runner.runPython", jythonText_2, directory+cell+".tif "+dimensions);

thenewImageID = getImageID();
selectImage(thenewImageID);
run("Split Channels");
selectWindow("C3-"+cell+".tif");
run("Rotate 90 Degrees Right");
run("Flip Horizontally", "stack");
saveframe = getString("What frame would you like to look at the brightfield on?", "1");
setSlice(saveframe);
saveAs("PNG", directory+cell+"_BF.png");
selectWindow(cell+"_BF.png");
run("Close");
selectWindow("C2-"+cell+".tif");
run("Close");
selectWindow("C1-"+cell+".tif");
run("Close");
