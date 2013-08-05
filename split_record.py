#!/usr/bin/env python
# 
# Given a recording and a tracklist in any ffmpeg-supported audio format,
# split the single record into multiple MP3 tracks.
#
# Suggested usage: cat tracklist.txt | ./split.py > run.sh
# Then inspect and execute run.sh
#
# Tracklist is read from stdin and is expected to begin with the name of a
# side (which is used as the input filename) followed by one line for each
# track, consisting of track number, name, and duration.
# Sides are separated by a newline.
# For example:
#
# SIDE1
# 1 Track Name One 1:23
# 2 Track Name Two 3:11
#
# SIDE1
# 3 Track Name Three 0:34
# 4 Track Name Four 4:23

import datetime
import time
import subprocess
import sys

sides = {}
tracks = []
firstline = True
for line in sys.stdin:
    if line == '\n':
        sides[sidename] = tracks
        tracks = []
        firstline = True
        continue
    if firstline:
        sidename = line.strip()
        firstline = False
    else:
        line = line.strip()
        num = line.split()[0]
        name = ' '.join(line.split()[:-1])
        time = line.split()[-1]
        tracks.append((num, name, time))
sides[sidename] = tracks

for side in sides:
    seek = datetime.timedelta()
    for track in sides[side]:
        (num, name, time) = track
        t = datetime.datetime.strptime(time, '%M:%S')
        time = t.strftime('%H:%M:%S')
        print 'ffmpeg -i "%s" -ss %s -t %s "%s.mp3"' % (side, seek, time, name)
        delta = datetime.timedelta(minutes=t.minute, seconds=t.second)
        seek += delta
