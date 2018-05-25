analysis = getString("What type of analysis do you want to do? (Kar9 or Cin8)", "Kar9");
if(analysis == "Kar9"){
	runMacro(getDirectory("home")+"Desktop/Tracking Script/Macro.ijm");
	waitForUser("Next", "Open and run the 'Python Data Manipulation' Jupyter notebook.");
}
if(analysis == "Cin8"){
	runMacro(getDirectory("home")+"Desktop/Tracking Script/Macro Cin8.ijm");
	waitForUser("Next", "Open and run the 'Python Data Manipulation Cin8' Jupyter notebook.");
}
if(analysis != "Kar9"){
	if(analysis != "Cin8"){
		waitForUser("Error", "You did not enter a valid analysis type.");
	}
}
