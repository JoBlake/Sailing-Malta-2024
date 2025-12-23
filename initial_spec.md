# Spec for plot a json path

## Purpose
Plot a map showing the track in a series of tracking files

## Audience

Sophisticated code user

## Use case
* Prompt the use to enter the location of the tracking files
* look for either json or gpx files with tracking data at the directory location given by the user 
* If annotation data is available in the directory where the tracking files are load the annotation data, otherwise initialize the annotation data
* display map bounded by the minimum and maximum latitude and longitude coordinates in a list of tracking files
* graph the path documented in files
* If the files are in json format sailing data is available, otherwise just the track is available
* On the right of the screen add a window with three tabs for Home, Photo and Annotation
* If sailing data is available,then
    * plot the line blue when rpm field is zero, otherwise red
    * animate a blue line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the twa and the length of the arrow is proportional to the tws
    * animate a green line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the cog and the length of the arrow is proportional to the sog
    * animate an orange line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the awa and the length of the arrow is proportional to the aws
    * use a consistent scaling for all arrow lengths
    * on the home tab add a small legend explaining the arrows and place a radio button in front of each entry to allow the user to select displaying the arrow or not. 
    * On the home tab add an entry in current data to show distance travelled in nautical miles and kilometers
    * on the home tab add text explaining the line colors
    * on the home tab display the values for date/time, lat, lon, rpm, cog, sog, twa, tws, awa and aws
* If only tracking data is available 
    * if the tracking data is over water plot the line solid blue and animate a boat icon along the tracking line
    * if tracking data is over land 
        * plot the line solid blue and animate a person icon along the tracking line
        * calculate the sog and cog from the gps coordinate data as it varies over time cog  on the home tab
    * on the home tab display the values for date/time, lat, lon, cog as a bearing and sog as speed in km/hr. Add next to cog and sog (est.)
* On the home tab add a slider to the tab to move the boat's position along the track
* When moving the slider show the timestamp
* On the Photo tab 
    * add a button to select a file directory with photos
    * add a button to select whether to only load pictures taken between the start and end timestamp in the tracking data
    * if the button is not selected load all pictures chosen
* display on the map a small icon corresponding to the pictures gps coordinate in the location metadata
* Display a large scale photo when the icon is clicked on. but keep the tab on the right visible
* On the Annotation tab allow the user to enter text to annotate the map at the current position along the track
* Display on the map a small icon identifying the position which was annotated
* Add to the Annotation tab two buttons: one to save all annotation and one to load annotations. 
* Have the default directory for saving and loading annotations be the same as where the track data is
* When the annotation icon is clicked on open a window showing the text and display the timestamp of the boat's position below the text
* add the button pan which will pan the map so that the boats position is centered and reverse to animate backwards
* Do not overwrite the track during the animation
* Allow the user to change the size of the tabbed interface

## Technology

* Tracks are stored in either json or gpx files 
* Python flask app
* Should use uv managed virtual environment

## Notes

* Create a readme with usage instructions

## Update



