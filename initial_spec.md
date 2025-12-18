# Spec for plot a json path

## Purpose

Plot a map showing the track in a series of json files

## Audience

Sophisticated code user

## Use case

* display map bounded by the minimum and maximum latitude and longitude coordinates in a list of json files
* graph the path documented in the json files
 

## Technology

* Python flask app
* Should use uv managed virtual environment

## Notes

* Create a readme with usage instructions

## Update
* Plot the line blue when rpm field is zero, otherwise red
* animate a blue line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the twa and the length of the arrow is proportional to the tws
* animate a green line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the cog and the length of the arrow is proportional to the sog
* animate an orange line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the awa and the length of the arrow is proportional to the aws
* Use a consistent scaling for all arrow lengths
* On the right of the screen add a window with three tabs for Home, Photo and Annotation
* On the home tab add a small legend explaining the arrows and place a radio button in front of each entry to allow the user to select displaying the arrow or not. 
* On the home tab add an entry in current data to show distance travelled in nautical miles and kilometers
* On the home tab add text explaining the line colors
* On the home tab display the values for date/time, lat, lon, rpm, cog, sog, twa, tws, awa and aws
* On the home tab add a slider to the tab to move the boat's position along the track
* When moving the slider show the timestamp
* On the Photo tab add a button to select a file directory with photos
* display on the map a small icon corresponding to the pictures gps coordinate in the location metadata
* Display a large scale photo when the icon is clicked on. but keep the tab on the right visible
* On the Annotation tab allow ther user to enter text to annotate the map at the current position along the track
* Display on the map a small icon identifying the position which was annotated
* Add to the Annotation tab two buttons: one to save all annotation and one to load annotations
* When the annotation icon is clicked on open a window shoing the text and display the timestamp of the boat's position below the text
* add the button pan which will pan the map so that the boats position is centered and reverse to animate backwards
* Do not overwrite the track during the animation
