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
from appscript import *
import re

def isOpen():
	sysevents = app('System Events')
	open_processes = sysevents.processes.name()
	if ('iTunes' in open_processes):
		return True
	else:
		return False

def open():
	app('iTunes').activate()
	
def getPlaylists():
	if (not isOpen()):
		return [];
	return {p.name():p for p in app('iTunes').playlists()}

def playPlaylist(p):
	re_str = 'app\(\'/.*?/iTunes.app\'\).sources.ID\([0-9]*?\).user_playlists.ID\([0-9]*?\)'
	if (re.search(re_str,str(p)) is not None):
		p.play()