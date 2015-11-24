import socket
import urllib, urllib2

class Downloader:
	def __init__(self, uri, qparams):
		self.uri = uri
		self.qparams = qparams
		qstr = urllib.urlencode(self.qparams)
		self.req = urllib2.Request('?'.join([uri, qstr]))

	def download(self):
		try:
			f = urllib2.urlopen(self.req)
			return f.read()
		except urllib2.URLError, e:
			print self.uri, e
		except Exception, e:
			print self.uri, e
		return None


TCP_IP = '59.66.130.209'
TCP_PORT = 6881
BUFFER_SIZE = 1024

if __name__ == '__main__':
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind((TCP_IP, TCP_PORT))
	s.listen(5)

	conn, addr = s.accept()
	print addr
	while True:
		data = conn.recv(BUFFER_SIZE)
		print 'data: ', data
	conn.close()