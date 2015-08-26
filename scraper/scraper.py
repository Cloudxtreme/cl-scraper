from lxml import html
from lxml.cssselect import CSSSelector
import requests

clBaseURL = 'http://newyork.craigslist.org'
clSearchURL = clBaseURL + '/search'
noFeeAptsURL = clSearchURL + '/nfa'
byOwnerAptsURL = clSearchURL + '/abo'
allAptsURL = clSearchURL + '/aap'

activeURL = noFeeAptsURL

def scrapeListings( url ):
  print 'Scraping ...\nURL: ' + url
  page = requests.get( url )
  tree = html.fromstring( page.text )
  tree.make_links_absolute( activeURL , False )
  listings = tree.cssselect('.content > p.row')
  headers = [ listing.cssselect('a.hdrlnk')[0] for listing in listings ]
  titles = [ header.text_content() for header in headers ]
  postLinks = [header.get('href') for header in headers ]
  print postLinks
  exit()
  postLink = clBaseURL = header.get('href')

  
scrapeListings( activeURL )
