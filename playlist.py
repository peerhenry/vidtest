import random
import xml.dom
import xml.etree.cElementTree as ET

class PlayList:
  def __init__(self):
    self.root = ET.Element("playlist", xmlns="http://xspf.org/ns/0/")
    self.root.set("xmlns:vlc", "http://www.videolan.org/vlc/playlist/ns/0/")
    self.root.set("version", "1")
    title = ET.SubElement(self.root, "title")
    title.text = "playlist"
    self.tracklist = ET.SubElement(self.root, "trackList")
    self.extension = ET.SubElement(self.root, "extension", application="http://www.videolan.org/vlc/playlist/0")

  def addTrack(self, index, path, duration, trackLength, segstart, segstop):

    start = 0 
    stop = trackLength

    if(duration > trackLength):
      if(trackLength < (segstop - segstart)):
        pos = random.randint(segstart, segstop-trackLength)
        start = pos/1000
        stop = (pos+trackLength)/1000
      else:
        start = segstart/1000
        stop = segstop/1000

    track = ET.SubElement(self.tracklist, "track")
    formatted = path.replace(' ','%20')
    formatted = path.replace('#','%23')
    ET.SubElement(track, "location").text = "file:///"+formatted
    ET.SubElement(track, "duration").text = str(duration)
    ext = ET.SubElement(track, "extension", application="http://www.videolan.org/vlc/playlist/0")
    ET.SubElement(ext, "vlc:id").text = str(index)
    ET.SubElement(ext, "vlc:option").text = "start-time="+str(start)
    ET.SubElement(ext, "vlc:option").text = "stop-time="+str(stop)
    ET.SubElement(self.extension, "vlc:item", tid=str(index))
  
  def finalize(self, name):
    tree = ET.ElementTree(self.root)
    tree.write(name+".xspf")