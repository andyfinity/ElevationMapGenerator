# Elevation Map Tools
Contains tools to download files from the USGS and create a colorized elevation map.

## ElevationDataDownloader.py
The kind folks at the USGS have freely provided a lot of very interesting data, but they've done very poorly at providing ways of accessing that data. What if I want to download an entire DEM resolution set? Their tools are abysmal for that. Fortunately for me, they've provided all sorts of GIS data on an FTP site. This tool downloads all tiles of a particular resolution.

Note that this may take a _very_ long time. The USGS servers aren't very quick. It should take about a week to download the entire 1/3 arc-second DEM tiles (as of 2015-10-11). Moreover, the FTP connection times out (without notice) after 24 hours of downloading. We also found that they do per-connection rate throttling to about 500kBps. Using the `--start-on` and `--end-on` parameters (or `-s` and `-e`, respectively), you can do segmented downloads. Segmenting the whole list into small chunks allows for a drastically increased download speed and reduces issues of the 24-hour timeout.

Syntax: `ElevationMapDownloader.py [-h] [-s START_ON] [-e END_ON] [-a EMAIL_ADDRESS] [-r REGEX] REMOTEDIR LOCALDIR`

Simplest example: `./ElevationDataDownloader.py /vdelivery/Datasets/Staged/Elevation/13/IMG/ .`

## ElevationMapCreator2D.py
Renders IMG files into beautifully-colored regular images, where color corresponds to height. Can take several and stitch them together, making a really big map.

## ElevationMapCreator3D.py
Renders IMG files into a 3D shape and lets a user fly through them.
