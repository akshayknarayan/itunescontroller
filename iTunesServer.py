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
from urllib import parse
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
		
		if (not iTunesController.isOpen()):
			iTunesController.open()
		
		returnVal = ''
		parsed = parse.urlparse('http://localhost:8000'+self.path);
		if (parsed.path == '/'):
			self.send_response(200)
			self.send_header("Content-type", "text/html")
			self.end_headers()
			page = open('./site/index.html')
			self.wfile.write(page.read().encode('utf-8'))
			page.close()
			return
		elif (parsed.path.startswith('/site')):
			self.send_response(200)
			if (parsed.path.endswith('css')):
				self.send_header("Content-type", "text/css")
			elif (parsed.path.endswith('js')):
				self.send_header("Content-type", "application/javascript")
			elif (parsed.path.endswith('jpg')):
				self.send_header("Content-type", "image/jpeg")
				self.end_headers()
				page = open('.'+parsed.path, 'rb')
				self.wfile.write(page.read())
				page.close()
				return
			else:
				self.send_header("Content-type", "text/plain")
			self.end_headers()
			page = open('.'+parsed.path)
			self.wfile.write(page.read().encode('utf-8'))
			page.close()
			return
		elif (parsed.path == '/app'):
			self.send_response(200)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
		else:
			self.send_response(400)
			self.send_header("Content-type", "text/plain")
			self.end_headers()
			self.sendResult('invalid query')
			return
				
		tokenized = parse.parse_qs(parsed.query, True)
		argKeys = tokenized.keys()
		if ('auth' not in argKeys):
			self.sendResult('need auth key')
			return
		elif (tokenized['auth'][0].upper() != AUTH_KEY):
			print(tokenized['auth'][0].upper()+" vs. "+AUTH_KEY)
			self.sendResult('wrong auth key')
			return
		if ('playlists' in argKeys):
			playlist = list(iTunesController.getPlaylists().keys())
			playlist = [x.replace(' ','-') for x in playlist]
			self.sendResult(str(playlist))
			return
		elif ('play' in argKeys):
			iTunesController.playPlaylist(iTunesController.getPlaylists()[tokenized['play'][0].replace('-',' ')])
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