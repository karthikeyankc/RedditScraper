from sys import argv
import requests
import json
import time
import string

script, subreddit = argv
subreddit = subreddit.lstrip('/r/')

def scrape(subreddit):
	s = requests.Session()
	s.headers.update({'User-Agent':'Scraper App'})
	content_list = []
	after = ""
	while after != None:
		time.sleep(2)
		url = "https://www.reddit.com/r/"+subreddit+"/top/.json?sort=top&t=all&limit=25&after="+after
		print "\nScraping %s\n...\n...\n...\n" %url
		html = s.get(url)
		content = html.content
		j_dict = json.loads(content)
		after = j_dict["data"]["after"]
		children = j_dict["data"]["children"] # list
		if children:
			children_data = []
			for x in children:
				children_data = x["data"]
				result = children_data["title"]
				content_list.append(result)
			if after == None:
				print "Scraping has reached the final page or hit the API limit of 1000!"
			else:
				print "Next page found at %s.\n" %after
		else:
			break
	return content_list

def textify(content_list):
	common_identifiers = ["LPT", "[LPT]", "TIL"]
	ignore_tags = ["Mod Request", "LPT Request"]
	for content in content_list:
		if any(ignore_tag in content for ignore_tag in ignore_tags):
			for tag in ignore_tags:
				if tag == "Mod Request" and tag in content:
					content_list.remove(content)
				elif tag == "LPT Request" and tag in content:
					content_list.remove(content)
		elif any(identifier in content for identifier in common_identifiers):
			for identifier in common_identifiers:
				if identifier == "TIL" and identifier in content:
					new = content.replace(identifier, "You should know", 1)
					write(new)
					break
				elif identifier == "LPT" or identifier == "[LPT]" and identifier in content:
					new = content.replace(identifier, "", 1)
					write(new)
					break
				else:
					continue
		else:
			with open("scraped contents from "+subreddit+".txt", 'a+') as text_file:
				text_file.write(content.encode('utf-8')+"\n")
	print "Scraping successful! Contents are written to 'Scraped Contents from "+subreddit+".txt'!"

def write(new):
	with open("scraped contents from "+subreddit+".txt", 'a+') as text_file:
		text_file.write(new.encode('utf-8').lstrip(string.punctuation + ' ').capitalize()+"\n")

content_list = scrape(subreddit)
if content_list:
	textify(content_list)
else:
	print "No data found. Make sure the subreddit exists and is not private."