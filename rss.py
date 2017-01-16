import csv
import requests
import xml.etree.ElementTree as ET

def loadRSS():
	#url = 'http://feeds.feedburner.com/TechCrunchIT'
	url = 'http://www.hindustantimes.com/rss/topnews/rssfeed.xml'
	resp = requests.get(url)

	with open('topnewsfeed.xml', 'wb') as f:
		f.write(resp.content)

def parseXML(xmlfile):

	tree = ET.parse(xmlfile)
	root = tree.getroot()
	newsitems = []

	for item in root.findall('./channel/item'):
		news={}
		for child in item:
			if child.tag == '{http://search.yahoo.com/mrss/}content':
				news['media'] = child.attrib['url']
			else:
				news[child.tag] = child.text.encode('utf8')
		newsitems.append(news)

	return newsitems

def savetoCVS(newsitems, filename):
	fields = ['guid', 'title', 'pubDate', 'description', 'link', 'media']

	with open(filename, 'w') as csvfile:

		writer = csv.DictWriter(csvfile, fieldnames = fields)
		writer.writerheader()
		writer.writerows(newsitems)

def main():
	loadRSS()
	newsitems = parseXML('topnewsfeed.xml')
	savetoCVS(newsitems, 'topnews.csv')


if __name__ == "__main__":
	main()
	









