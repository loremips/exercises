#!/usr/bin/python
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

import os
import re
import sys
import urllib
import commands

"""Logpuzzle exercise
Given an apache logfile, find the puzzle urls and download the images.

Here's what a puzzle url looks like:
10.254.254.28 - - [06/Aug/2007:00:13:48 -0700] "GET /~foo/puzzle-bar-aaab.jpg HTTP/1.0" 302 528 "-" "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.6) Gecko/20070725 Firefox/2.0.0.6"
"""

'''
# first puzzle
def read_urls(filename):
  """Returns a list of the puzzle urls from the given log file,
  extracting the hostname from the filename itself.
  Screens out duplicate urls and returns the urls sorted into
  increasing order."""
  address='http://code.google.com'
  list1=[]
  list2=[]
  f = open(filename, 'rU')
  for line in f:
    #print line 
    match = re.search(r'GET ([/\w+.-]*puzzle[/\w+.-]*) HTTP/', line)
    if match:
      #print match.group(1)
      if not address+match.group(1) in list1:
        list1.append(address+match.group(1))
        #print match.group(1)
  list2=sorted(list1)
  #for i in list2:
  #  print i
  f.close()
  return list2
'''

def sortkeyfunc(s):
  return s[1]

# second puzzle
def read_urls(filename):
  address='http://code.google.com'
  dict1={}
  list1=[]
  list2=[]
  f = open(filename, 'rU')
  for line in f:
    #GET /edu/languages/google-python-class/images/puzzle/p-bhhe-bahd.jpg HTTP/
    match = re.search(r'GET ([/\w+.-]*puzzle/\w+-\w+-)(\w+)([.\w+]*) HTTP/', line)
    if match:
      if not match.group(2) in dict1:
        dict1[match.group(2)]=address+match.group(1)+match.group(2)+match.group(3)

  for key in sorted(dict1.keys()):
    print key, dict1[key]
    list2.append(dict1[key])
 
  f.close()
  return list2
  

def htmlfilewrite(urllist):  
  f = open('anim.html', 'w')
  f.write('<head></head><body>')
  for url in urllist:
    #print url
    st = "<img src='%s'>" % url 
    f.write(st)
  f.write('</body>')
  f.close() 

def download_images(img_urls, dest_dir):
  """Given the urls already in the correct order, downloads
  each image into the given directory.
  Gives the images local filenames img0, img1, and so on.
  Creates an index.html in the directory
  with an img tag to show each local image file.
  Creates the directory if necessary.
  """
  index=0
  
  if not os.path.exists(dest_dir):
    os.mkdir(dest_dir)
    
  cmd = 'touch ' + dest_dir + '/index.html'
  (status, output) = commands.getstatusoutput(cmd)
  if status:    
    sys.stderr.write(output)
    sys.exit(1)

  f = open('%s/index.html' % dest_dir, 'w')
  f.write('<head></head><body>')

  for url in img_urls:
    print 'Retrieving ', url
    urllib.urlretrieve(url, '%s/img%d' % (dest_dir, index))
    f.write("<img src='img%d'>" % index)
    index += 1
    
  f.write('</body>')
  f.close    
    
    

def main():
  args = sys.argv[1:]

  if not args:
    print 'usage: [--todir dir] logfile '
    sys.exit(1)

  todir = ''
  if args[0] == '--todir':
    todir = args[1]
    del args[0:2]

  img_urls = read_urls(args[0])

  if todir:
    download_images(img_urls, todir)
  else:
    print '\n'.join(img_urls)
  
  #htmlfilewrite(read_urls(args[0]))

if __name__ == '__main__':
  main()
