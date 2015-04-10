# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "EFR003_DFEFARA_gov"
url = "http://data.gov.uk/dataset/financial-transactions-data-defra"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'Jan': '01', 'Feb': '02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 'Jul':'07', 'Aug':'08', 'Sep':'09','Oct':'10','Nov':'11','Dec':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)


# find all entries with the required class
blocks = soup.findAll('div', {'class':'dataset-resource'})

for block in blocks:

	a = block.findAll('a')[2]
	link = a['href']
	title = block.find('div',{'class':'inner2'}).getText()
	title = title.strip()
	
	if len(title.split()) > 4:
		print "not a usable file"
	else:
		# create the right strings for the new filename
		title = title.strip()
		csvYr = title.split(' ')[-2]
		csvMth = title.split(' ')[-3][:3]
		csvMth = convert_mth_strings(csvMth);
		
		filename = entity_id + "_" + csvYr + "_" + csvMth
	
		todays_date = str(datetime.now())
		
		scraperwiki.sqlite.save(unique_keys=['l'], data={"l": link, "f": filename, "d": todays_date })
			
		print filename
