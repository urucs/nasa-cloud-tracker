import re
import os
from urllib2 import urlopen
from BeautifulSoup import BeautifulSoup
from cStringIO import StringIO
from PIL import Image
import filecmp
import logging
import logging.handlers


Image.MAX_IMAGE_PIXELS = None


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# create a file handler

handler = logging.handlers.RotatingFileHandler('/home/guido/scripts/logs/update_log.out', maxBytes=10*1024, backupCount=5)
handler.setLevel(logging.INFO)

# create a logging format

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger

logger.addHandler(handler)





def updateLatest(images_url):
    max_files = 20;
    i = max_files -1;
    images_root = '/var/www/clouds/img/'
    pattern = re.compile(r'http://goes.gsfc.nasa.gov/')
    match = pattern.search(images_url)
    prelen = len (match.group(0))
    subpath = images_url[prelen:]
    file_url = images_url + 'latest.info'

    try:
        latest_remote_file = urlopen(file_url)
    except:
        print "No existe latest.info"
        return

    if not os.path.exists(images_root + subpath):
        os.makedirs(images_root + subpath)
    remote_latest = open(images_root + subpath + 'remote_latest.info','wb')
    remote_latest.write(latest_remote_file.read())
    remote_latest.close()
    try:
        files_cmp = filecmp.cmp(images_root + subpath + 'latest.info',images_root + subpath + 'remote_latest.info' )
    except:
        new_latest = open(images_root + subpath + 'latest.info', 'wb')
        new_latest.write("Initial file")
        new_latest.close()
        files_cmp = filecmp.cmp(images_root + subpath + 'latest.info',images_root + subpath + 'remote_latest.info' )
        os.remove(images_root + subpath + 'latest.info')
        os.rename(images_root + subpath + 'remote_latest.info',images_root + subpath + 'latest.info')
    if not files_cmp:
        try:
            os.remove(images_root + subpath + str(i) + '.jpg')
        except:
            logger.info(str(i) + '.jpg  doesnt exist')
        i = i-1
        while(True):
            if (i > -1):
                try:
                    os.rename(images_root + subpath + str(i) + '.jpg',images_root + subpath + str(i+1) + '.jpg')
                except:
                    logger.info(str(i) + '.jpg  doesnt exist')
                i = i-1
            else:
                #logger.info('Trying to update latest')
                imagesDownloader(images_url,1)
                return




def imagesDownloader(images_url, totalImages = 20):


    images_root = '/var/www/clouds/img/'

    file_url = images_url + 'latest.info'
    pattern = re.compile(r'http://goes.gsfc.nasa.gov/')
    match = pattern.search(images_url)
    prelen = len (match.group(0))
    subpath = images_url[prelen:]


    print "Esperando a la NASA"

    response = urlopen(images_url)
    try:
        latest_remote_file = urlopen(file_url)
    except:
        print "No existe latest.info"
        return
    if not os.path.exists(images_root + subpath):
        os.makedirs(images_root + subpath)
    remote_latest = open(images_root + subpath + 'remote_latest.info','wb')
    remote_latest.write(latest_remote_file.read())
    remote_latest.close()
    print "La NASA nos muestra su pagina"
    html = response.read()
    soup = BeautifulSoup(html)
    i = 0
    if not os.path.exists(images_root + subpath):
        os.makedirs(images_root + subpath)
    try:
        files_cmp = filecmp.cmp(images_root + subpath + 'latest.info',images_root + subpath + 'remote_latest.info' )
    except:
        new_latest = open(images_root + subpath + 'latest.info', 'wb')
        new_latest.write("Initial file")
        new_latest.close()
        files_cmp = filecmp.cmp(images_root + subpath + 'latest.info',images_root + subpath + 'remote_latest.info' )
    if (not files_cmp):
        os.remove(images_root + subpath + 'latest.info')
        os.rename(images_root + subpath + 'remote_latest.info',images_root + subpath + 'latest.info')
        for trs in reversed (soup.findAll('a')[-totalImages -1:]):
            print soup.findAll('a')[-totalImages -1:]
            match = re.search(r'>(.*).tif',str(trs))
            if match is not None:
                try:
                    filenametif = match.group(1) + '.tif'
                    print filenametif
                    filenamejpg = match.group(1) + '.jpg'
                    print "Pongo a bajar" + images_url + filenametif
                    fi = urlopen(images_url + filenametif)
                    print "Ahi se bajo y la voy a nombrar" + str(i)+'.jpg'
                    fi_read = fi.read()
                    print "Y la lei"
                    file_tif = StringIO(fi_read)
                    image_jpg = Image.open(file_tif)
                    if not os.path.exists(images_root + subpath):
                        os.makedirs(images_root + subpath)

                    try:
                        image_jpg.save(images_root + subpath + str(i)+'.jpg', quality = 90)
                        #logger.info(images_root + subpath + str(i)+'.jpg' + "Downloaded")
                    except:
                        try:
                            image_jpg.convert('RGB').save(images_root + subpath + str(i)+'.jpg', quality = 90)
                        except:
                            logger.error(images_root + subpath + str(i)+'.jpg couldnt save after converting to RGB')


                    i += 1
                except: 
                    print "Something went wrong with image handling"
            else:
                print "no matchea"


imagesDownloader('http://goes.gsfc.nasa.gov/goeseast/argentina/ir4/',20)
#updateLatest('http://goes.gsfc.nasa.gov/goeseast/argentina/ir4/')