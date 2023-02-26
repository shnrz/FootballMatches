from bs4 import BeautifulSoup

FRAME_HEIGHT = '576'
FRAME_WIDTH = '1024'

def getIframeTag(soup):

   print('Detecting known scripts...')

   if (str(soup).find('radamel.icu') > -1 ):
      print('Found Radamel script!')
      scripts = soup.select('script')
      stream_id = str(scripts[0]).split('"')[1]
      print(stream_id)
      frame_tag = '<iframe src="https://radamel.icu/reproductor/' + stream_id + '.php?width=' + FRAME_WIDTH + '&amp;height=' + FRAME_HEIGHT + '" frameborder="0" scrolling="no" allowtransparency="true" allowfullscreen="true" width="' + FRAME_WIDTH + '" height="' + FRAME_HEIGHT + '"></iframe>'
      return frame_tag

   elif (str(soup).find('vikistream.com') > -1 ):
      print('Found VikiStream script!')
      scripts = soup.select('script')
      stream_id = str(scripts[0]).split('"')[1]
      print(stream_id)
      frame_tag = '<iframe src="https://vikistream.com/embed2.php?player=desktop&amp;live=' + stream_id + '" style="overflow:hidden;height:' + FRAME_HEIGHT + ';width:' + FRAME_WIDTH + '" width="' + FRAME_WIDTH + '" height="' + FRAME_HEIGHT + '" scrolling="no" autoplay="yes" frameborder="0" allowfullscreen="true" allowtransparency="true" allow="autoplay, fullscreen" allowautoplay="yes" id="thatframe" webkitallowfullscreen="" mozallowfullscreen=""></iframe>'
      return frame_tag

   elif (str(soup).find('<iframe id="streamIframe"') > -1):
      print('Found streamIframe!')
      frame_tag = soup.select('iframe#streamIframe')
      return frame_tag

   else:
      print('Unable to detect known scripts :-(')
      print('Here\'s the soup:')
      print(soup.prettify())
      return None
