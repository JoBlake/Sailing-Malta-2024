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
* animate a blue line graphic arrow moving from the start to the end of the tracks. The arrow should point away from the twa and the length of the arrow is proportional to the tws
* animate a green line graphic arrow moving from the start to the end of the tracks. The arrow should point towards the cog and the length of the arrow is proportional to the sog
* display the values for date/time, lat, lon, cog, sog, rpm, and tws in the lower right during the animation
* add the buttons pan which will pan the map so that the boats position is centered and reverse to animate backwards
* display a small legend explainin the arrows
* Do not overwrite the track during the animation
