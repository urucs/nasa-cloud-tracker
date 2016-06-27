import re
import imagesDownloader
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
from cStringIO import StringIO
from PIL import Image

def update():
	root_url = 'http://goes.gsfc.nasa.gov/goeseast/'
	rootDir = '/var/www/clouds/img/'

	print "Esperando a la NASA"
	response = urlopen(root_url)
	print "La NASA nos muestra su pagina"
	html = response.read()
	soup = BeautifulSoup(html)
	#imageDownloader.imagesDownloader('http://goes.gsfc.nasa.gov/goeseast/argentina/ir4/')
	for trs in soup.findAll('a'):
		match = re.search(r'>(.*)/</',str(trs))
		if match is not None:
			dir_name = match.group(1)
			level1_url = root_url + dir_name + '/'
			##print level1_url
			response = urlopen(level1_url)
			html = response.read()
			soup = BeautifulSoup(html)
			for trs in soup.findAll('a'):
				match = re.search(r'>(.*)/</',str(trs)) # anda con trs in soup.findAll('a')
				if match is not None and match.group(1) != 'maps':
				  	dir2_name = match.group(1)
					level2_url = level1_url + dir2_name + '/'
					##print level2_url
					imagesDownloader.updateLatest(level2_url)
