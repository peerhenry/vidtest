from os import listdir
from os.path import isfile, join

def getVidList(path):
  return [join(path, f) for f in listdir(path) if isfile(join(path, f)) and isVid(f)]

def isVid(filename):
  return filename.endswith('.mp4') or filename.endswith('.wmv') or filename.endswith('.flv') or filename.endswith('.avi') or filename.endswith('.webm') or filename.endswith('.mpeg')