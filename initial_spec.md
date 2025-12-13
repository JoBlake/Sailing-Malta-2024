# Spec for plot a json path

## Purpose

Plot a map showing the track in a series of json files

## Audience

Sophisticated code user

## Use case

* display map bounded by the minimum and maximum latitude and longitude coordinates in a list of json files
* animate an icon moving from the start to the end of the tracks
* graph the path documented in the json files
 

## Technology

* Python flask app
* Should use uv managed virtual environment

## Notes

* Create a readme with usage instructions

## Update
* Plot the line black when rpm field is 0
* When rpm is not zero, plot the line color as a function of the value tws in the jason file. Use the cold ice / hot metal color map 
* display the values for date/time, rpm, and tws in the lower right during the animation
