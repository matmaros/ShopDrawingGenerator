# Shop Drawing Generator

This script generates a shop drawing sheet in the model space of a Rhino3d file.  The script is written in python and implemented in Rhino3D via the 'Edit Python Script' command.  The script references a 'checklist.csv' file generated from an excel file with drop down lists to provide data.  See example here:

![image](https://user-images.githubusercontent.com/67350711/119895074-5e259980-bf0b-11eb-88bc-728310a980d3.png)

The file also references a 'note.txt' file.  This is a text file to contain general drawings notes as required for the drawing.

Based on the data entered into the 'checklist.csv' file a drawing is produced by selecting 2d blocks arranged into the model space.  The below shows and example of a shower door shop drawing created for a glass shower door.  This also includes custom notes which are pulled form the csv file.

To run this project download the rhino file and two csv files to your desktop.  In the python script - edit the file path at the top of the script to show the path for your desktop.  Open the rhino file and type "editpythonscript" into the command line.  Paste the contents of the python script and click run script.

![image](https://user-images.githubusercontent.com/67350711/119895450-cd02f280-bf0b-11eb-8059-40abcc38bb34.png)
