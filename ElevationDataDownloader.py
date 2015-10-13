#!/usr/bin/env python3

import ftplib
import re
import sys
import os
import argparse
import time

parser = argparse.ArgumentParser(description="Read files from the USGS FTP site. Designed for use with the 1/3 arc-second elevation data, but will probably also download other types and resolutions.")
parser.add_argument('REMOTEDIR',
	help="directory to read from on the USGS FTP site")
parser.add_argument('LOCALDIR',
	help="directory to write to on your local computer")
parser.add_argument('--start-on',
	help="first file name to download")
parser.add_argument('--end-on',
	help="last file name to download")
args = parser.parse_args()

remote_path = args.REMOTEDIR.rstrip("/") + '/'
local_path = os.path.abspath(args.LOCALDIR) + '/'

ftp = None
downloading = False

try:
	if not os.path.exists(local_path):
		raise OSError("LOCALDIR does not exist.")

	# Connect and go to the right directory
	print("Opening remote connection")
	with ftplib.FTP('rockyftp.cr.usgs.gov', user='anonymous', passwd='andymrussell777+gis@gmail.com') as ftp:
		print("Navigating to the right remote directory")
		ftp.cwd(remote_path)

		# Get and refine the file lists
		print("Getting remote file list")
		file_list = ftp.nlst()
		print("Finding remote files")
		file_list = [x for x in file_list if re.match(r'^[ns]\d{2}[ew]\d{3}\.zip', x)]
		if args.start_on:
			try:
				first = file_list.index(args.start_on)
				file_list = file_list[first:]
			except:
				raise OSError("Invalid starting file!")
		if args.end_on:
			try:
				last = file_list.index(args.end_on)
				file_list = file_list[:last+1]
			except:
				raise OSError("Invalid ending file.")
		if len(file_list) == 0:
			raise OSError("No files to download.")

		# Do a bit of user interaction
		print("========")
		print("{:,d} files queued for download".format(len(file_list)))
		print("Downloading from \"%s\"" % remote_path)
		print("Storing into \"%s\"" % local_path)
		print("========")
		while True:
			x = input("Do you want to begin the download? [y/n] ")
			if x.lower() == "y":
				break
			elif x.lower() == "n":
				raise KeyboardInterrupt()

		# Download each file
		for file_name in file_list:
			# Determine actual file names
			source = remote_path + file_name
			destination = local_path + file_name
			print("%s => %s" % (source, destination))

			# Pull remote file onto local
			start = time.time()
			with open(destination, "wb") as file_handle:
				downloading = True
				ftp.retrbinary("RETR %s" % file_name, file_handle.write)
				downloading = False
			end = time.time()

			# Write a nice epilogue
			duration = end - start
			size = os.path.getsize(destination)
			rate = float(size) / float(duration)
			print("  Downloaded {:,d} bytes in {:,.1f} seconds".format(size, duration))
			print("  {:,.0f} bytes per second average".format(rate))

		print("All files downloaded successfully")
except KeyboardInterrupt:
	print("Terminating download process")
except ftplib.error_perm as e:
	if not downloading:
		print("Permissions error: %s" % e)
except OSError as e:
	print("OS error: %s" % e)
