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
* Plot the line solid  when rpm field is zero, otherwise dotted
* animate a blue line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the twa and the length of the arrow is proportional to the tws
* animate a green line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the cog and the length of the arrow is proportional to the sog
* animate an orange line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the awa and the length of the arrow is proportional to the aws
* Use a consistent scaling for all arrow lengths
* add a tab to display a small legend explaining the arrows and place a radio button in front of each entry to allow the user to select displaying the arrow or not. 
* Display the value of the cog, sog, twa, tws, awa and aws to the right of each arrow 
* Have the speed control for the animation scale from 1/8 to 8x 
* display the values for date/time, lat, lon and rpm in the lower right during the animation
* add the buttons pan which will pan the map so that the boats position is centered and reverse to animate backwards
* Do not overwrite the track during the animation
* Add a tab to select a file directory with photos
* display on the map a small icon corresponding to the pictures gps coordinate in the location metadata