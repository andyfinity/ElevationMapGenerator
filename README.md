# Elevation Map Tools
Contains tools to download files from the USGS and create a colorized elevation map.

## ElevationDataDownloader.py
The kind folks at the USGS have freely provided a lot of very interesting data, but they've done very poorly at providing ways of accessing that data. What if I want to download an entire DEM resolution set? Their tools are abysmal for that. Fortunately for me, they've provided all sorts of GIS data on an FTP site. This tool downloads all tiles of a particular resolution.

Note that this may take a _very_ long time. The USGS servers aren't very quick. It should take about a week to download the entire 1/3 arc-second DEM tiles (as of 2015-10-11).

Syntax: `ElevationMapDownloader.py [-h] REMOTEDIR LOCALDIR`

Example: `./ElevationDataDownloader.py /vdelivery/Datasets/Staged/Elevation/13/IMG/ .`

## ElevationMapCreator2D.py
Renders IMG files into beautifully-colored regular images, where color corresponds to height. Can take several and stitch them together, making a really big map.

## ElevationMapCreator3D.py
Renders IMG files into a 3D shape and lets a user fly through them.
