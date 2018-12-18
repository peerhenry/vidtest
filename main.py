import xml.dom
import xml.etree.cElementTree as ET
import json
import random
from os import walk
from os.path import join
import sys

import vlc
import vidlist
from playlist import PlayList

# read settings
# setup xml
playlist = PlayList()

# fill xml with contents

x = vlc.Instance()

def handle(index, tpath, trackLength):
  media = x.media_new(tpath)
  media.parse()
  duration = media.get_duration()-1
  if duration < 0:
    print("error: duration is 0 for file " + str(tpath))
    print("media state: " + str(media.get_state()))
  else:
    playlist.addTrack(index, tpath, duration, trackLength, 0, duration)

def handleSegment(index, tpath, duration, trackLength, segstart, segstop):
  media = x.media_new(tpath)
  media.parse()
  duration = media.get_duration()-1
  playlist.addTrack(index, tpath, duration, trackLength, segstart, segstop)

def getFiles(path, withSubDirs, exclusions):
  f = []
  for (dirpath, dirnames, filenames) in walk(path):
    fullnames = []
    for filename in filenames:
      toAdd = True
      for ex in exclusions:
        if(filename.endswith(ex)):
          toAdd = False
      if(toAdd):
        fullnames.append(join(dirpath, filename))
    f.extend(fullnames)
    if not withSubDirs:
      break
  return f

progressIndex = 0
milestones = []

def setMileStones(count):
  global progressIndex
  global milestones
  progressIndex = 0
  milestones = [
    count/10, 
    count/5, 
    3*count/10, 
    4*count/10, 
    count/2, 
    6*count/10, 
    7*count/10, 
    8*count/10, 
    9*count/10, 
    count
  ]

def printProgress(i):
  global progressIndex
  global milestones
  if i == milestones[progressIndex]:
    perc = (progressIndex+1)*10
    print(str(perc)+'%')
    progressIndex += 1

from collections import deque
past = deque([])

def handleSection(section):
  opts = section["options"]
  segmentLength = int(opts["segmentLength"])
  files = []

  if 'noRepeat' in opts:
    count = opts["noRepeat"]
    for i in range(0, count):
      past.append(0)

  # append files from directories
  for dir in section["directories"]:
    extra = getFiles( dir["path"], dir["includeSubDirs"], dir["exclusions"] )
    files.extend( extra )

  # append single files
  if 'files' in section:
    for eFile in section["files"]:
      files.append(eFile["path"])

  if(len(files) == 0):
    sys.exit("invalid section: no files found'")
  else:
    print(str(len(files)) + ' files used')

  # create random segments for playlist
  count = int(section["options"]["segmentCount"])
  setMileStones(count)
  for i in range(0, count):
    printProgress(i)
    maxi = len(files)-1
    n = random.randint(0, maxi)
    while n in past: n = random.randint(0, maxi)
    past.append(n)
    past.popleft()
    file = files[n]
    handle(i, file, segmentLength)

settings = json.load(open('settings.json'))
for section in settings["sections"]:
  handleSection(section)

# write xml file
playlist.finalize(settings["name"])