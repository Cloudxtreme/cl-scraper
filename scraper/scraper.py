from lxml import html
from lxml.cssselect import CSSSelector
import requests
import pprint

clBaseURL = 'http://newyork.craigslist.org'
imageBaseURL = "http://images.craigslist.org/"
clSearchURL = clBaseURL + '/search'
noFeeAptsURL = clSearchURL + '/nfa'
byOwnerAptsURL = clSearchURL + '/abo'
allAptsURL = clSearchURL + '/aap'
pp = pprint.PrettyPrinter(indent=4)

activeURL = noFeeAptsURL

def firstIn( list ):
    try:
        return list[0]
    except Exception:
        return None

def cleanAptLayoutData(layoutData):
  try:  
      return layoutData.strip("\s / -") 
  except Exception:
      return layoutData

def scrapeListings( url ):
  print 'Scraping ...\nURL: ' + url
  page = requests.get( url )
  tree = html.fromstring( page.text )
  tree.make_links_absolute( activeURL , False )
 
  listingDict = {}
  listings = tree.cssselect('.content > p.row')
  
  headers = { listing.get('data-pid') : listing.cssselect('a.hdrlnk')[0] for listing in listings }
  titles = { listingId : header.text_content() for (listingId,header) in headers.items() }
  postLinks = { listingId : header.get('href') for (listingId,header) in headers.items() }

  textSpans = { listing.get('data-pid') : listing.cssselect('span.txt')[0] for listing in listings }
  
  priceSpans = { listingId : firstIn( span.cssselect('span.price') ) for (listingId,span) in textSpans.items() }
  prices = { listingId : span.text_content()[1:] if span is not None else None for (listingId,span) in priceSpans.items() }

  layoutSpans = { listingId : firstIn( span.cssselect('span.housing') ) for (listingId,span) in textSpans.items() }
  layouts = { listingId : cleanAptLayoutData( span.text_content()[:] ) if span is not None else None for (listingId,span) in layoutSpans.items() }

  for listingId in headers.keys():
      listingDict[listingId] = {}
      listingDict[listingId]["title"] = titles[listingId]
      listingDict[listingId]["href"] = postLinks[listingId]
      listingDict[listingId]["price"] = prices[listingId]
      listingDict[listingId]["bedrooms"] = layouts[listingId]


  pp.pprint( listingDict )

scrapeListings( activeURL )
