import sys, os
import urllib2
import json
import random
from secrets import *

PRONUNCIATION_API = "http://apifree.forvo.com/key/" + API_KEY + "/format/json/action/word-pronunciations/word/%s/language/en"
pwd = os.path.dirname(os.path.realpath(__file__))

def file_for_word(word):
  response = json.load(urllib2.urlopen(PRONUNCIATION_API % word))
  try:
    idx = random.randint(0,len(response["items"])-1)
    url = response["items"][idx]["pathogg"]
    cachedFile = open(pwd + "/cached/%s-%i.ogg" % (word, idx), "wb")
    cachedFile.write(urllib2.urlopen(url).read())
    cachedFile.close()

    fileLocation = pwd + "/cached/%s-%i.mp3" % (word, idx)
    # Clean up the file with sox
    bandpassFilter = "sinc 400-7k "
    compressionFilter = "compand .1,.2 -inf,-32.1,-inf,-32,-32 0 -90 .1 "
    silenceFilter = "silence 1 1 1% reverse silence 1 1 1% reverse "
    padFilter = "pad 0 0.2 "
    os.system("sox \"" + fileLocation[:-4] + ".ogg\" \"" + fileLocation + "\" norm " + bandpassFilter + compressionFilter + silenceFilter + padFilter)
    return fileLocation
  except:
    print sys.exc_info()[0]
    return None


def main():
  words = sys.argv[1].split(" ")
  sequence = []
  for word in words:
    f = file_for_word(word)
    if(f is not None):
      sequence.append(f) # Build a list of the cached mp3's
      print f
    else:
      print "No results for " + word
  command = "sox "
  for mp3 in sequence:  # Build a list of files to merge
    command += mp3 + " "
  command += pwd + "/out.mp3; play out.mp3"
  os.system(command)
if __name__ == "__main__":
  main()
