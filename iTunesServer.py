"""
Copyright (c) 2013 Akshay Narayan.
All rights reserved.

Redistribution and use in source and binary forms are permitted
provided that the above copyright notice and this paragraph are
duplicated in all such forms and that any documentation,
advertising materials, and other materials related to such
distribution and use acknowledge that the software was developed
by Akshay Narayan ("the author"). The name of the author
may not be used to endorse or promote products derived
from this software without specific prior written permission.
THIS SOFTWARE IS PROVIDED ``AS IS'' AND WITHOUT ANY EXPRESS OR
IMPLIED WARRANTIES, INCLUDING, WITHOUT LIMITATION, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE.
"""

from http.server import BaseHTTPRequestHandler, HTTPServer
import iTunesController
import SystemController
import re
import string
import random

global AUTH_KEY

class Handler(BaseHTTPRequestHandler):
	def do_GET(self):
		global AUTH_KEY
		#print('GET', self.path)
		self.send_response(200)
		self.send_header("Content-type", "text/plain")
		self.end_headers()
		
		if (not iTunesController.isOpen()):
			iTunesController.open()
		
		returnVal = ''
		if (not (self.path[0:2] == '/?')):
			self.sendResult('invalid query')
			return
		
		#print(self.path)
		#print(self.tokenize_Path())
		
		tokenized = self.tokenize_Path()
		argKeys = tokenized.keys()
		if ('auth' not in argKeys):
			self.sendResult('need auth key')
			return
		elif (tokenized['auth'] != AUTH_KEY):
			self.sendResult('wrong auth key')
			return
		if ('playlists' in argKeys):
			playlist = list(iTunesController.getPlaylists().keys())
			playlist = [x.replace(' ','-') for x in playlist]
			self.sendResult(str(playlist))
			return
		elif ('play' in argKeys):
			iTunesController.playPlaylist(iTunesController.getPlaylists()[tokenized['play'].replace('-',' ')])
			self.sendResult('OK')
		elif ('pause' in argKeys):
			iTunesController.pause()
			self.sendResult('OK')
		if ('sleep' in argKeys):
			delay = int(tokenized['sleep'])
			if (delay > 0):
				self.sendResult('OK')
				SystemController.sleep(int(delay))
			else:
				self.sendResult('time to sleep must be a positive integer (in seconds)')
			
	def tokenize_Path(self):
		splitPath = re.split('&',self.path[2:])
		path_tokenized_list = [re.split('=',kv) if '=' in kv else [kv,None] for kv in splitPath]
		return {kv[0]:kv[1] for kv in path_tokenized_list}
	
	def sendResult(self, returnVal):
		self.wfile.write((returnVal+'\n').encode('utf-8'))
		return

def run(server_class=HTTPServer, handler_class=Handler):
	server_address = ('', 8000)
	httpd = server_class(server_address, handler_class)
	gen_AuthKey()
	print('starting. Your auth key for this session is \''+AUTH_KEY+'\'.')
	httpd.serve_forever()
	
def gen_AuthKey():
	global AUTH_KEY
	AUTH_KEY = ''.join(random.sample(string.ascii_uppercase + string.digits, 6))

run()