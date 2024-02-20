# How to use this file...
#
# python3
# 
# import sys, os
# sys.path.extend([f'./{name}' for name in os.listdir(".") if os.path.isdir(name)])
# import url
# 
# url.open('http://www.google.com')

import sys
import os
import subprocess
import webbrowser

def open(url):
  if sys.platform == 'darwin': # for OS X
    subprocess.Popen(['open', url])
  else:
    webbrowser.open_new_tab(url)