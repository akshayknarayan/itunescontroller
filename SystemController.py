"""
Copyright (c) 2013 Akshay Narayan.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by Akshay Narayan.  The name of author
may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""
import time
import subprocess
import iTunesController

def sleep(delay=0):
	"""Waits for the number of seconds specified by delay, then sleeps the system."""
	if (delay != 0):
		time.sleep(delay)
	iTunesController.pause()
	subprocess.call(['osascript','-e','tell app "Finder" to sleep'])