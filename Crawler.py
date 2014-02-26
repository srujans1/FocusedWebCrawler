import urllib2
import urlparse
import gQuery
import urlnorm
from MyPriorityQueue import MyPriorityQueue
import time
import mechanize
import mimetypes
from os.path import splitext, basename, getsize
import os.path
import priorityCalculator
import re
import stemmer
import tokenizer
import hashlib
import sys
from Queue import Queue
import threading

def get_size(start_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def urlContains(url, searchTags):
    count = 0
    for tag in searchTags:
        if tag in url:
            count +=1
    return count
        

# Extensions to be avoided
excludedExtentions = ['.png', '.gif', '.jpg', '.jpeg', '.pdf', '.mp3', '.wmv', '.svg', '.ogg','.jsp', '.ogv', '.py', '.tar.gz', '.css', '.ico', '.gz', '.ppt', '.zip', '.rar', '.ps', '.ppsx']
excludedExtensions = set(excludedExtentions)    # Making set for easy membership test

errorcount = 0
query = sys.argv[1]  # Initial query for focused crawler
urlcount = int(sys.argv[2])
searchTags = stemmer.stemmer(tokenizer.stringTokenizer(query))  # Stemming and tokenizing search query to avoid duplicate effort
print "Search tokens : "
print searchTags

top10urls = gQuery.googleSearch(query)

urls = MyPriorityQueue()    # Queue for storing URLs yet to be visisted
results = {}    # Dictionary structure for storing results URLs
visited = set()

for i in range(len(top10urls)): # Adding top 10 results to Queue
    urls.put(top10urls[i],1)

br = mechanize.Browser()   
f = open('results.txt','w+')

def FileWriteUtil(pri, url):
    try:
        br.open(url, timeout=10.0)
        regex = re.compile("mailto:|javascript:|action=edit")
        match = re.match(regex, url)      # Check for Javascript
        if match is None:
            print "adding to results : " + url
            results[url] = time.time()
            f.write("adding to results : %s \t priority: %s , time: %s , status: %s\n" % (unicode(url), pri, time.asctime(), br.response().code))
            f.flush()
            s = hashlib.sha1()
            s.update(url)
            fileloc = "Downloads/" + s.hexdigest() + ".txt"     #downloading html
            j = open(fileloc, 'w+')
            j.writelines(br.response().read())
            j.close()
    except urllib2.HTTPError, e:
        if e.code == 403 or e.code == 401: 
            print "Forbidden by robots.txt : " + url
            results[url] = time.time()
            f.write("Forbidden by robots.txt : %s \t priority: %s , time: %s , status: %s\n" % (unicode(url), pri, time.asctime(), br.response().code))
            f.flush()
        elif e.code == 404:
            print "Page not found: " + url
            results[url] = time.time()
            f.write("Page not found : %s \t priority: %s , time: %s , status: %s\n" % (unicode(url), pri, time.asctime(), br.response().code))
            f.flush()

urlpool = Queue()

def processPage():
    while not urls.counter > urlcount:
        try:
            link = urlpool.get()
            newurl = urlparse.urljoin(link.base_url, link.url) # Converting relative URLs to Absolute ones
            newurl = unicode(urlnorm.norm(newurl)) # Normalizing URL
            print "out: " + newurl
            disassembled = urlparse.urlsplit(newurl)
            filename, file_ext = splitext(basename(disassembled.path)) # Finding file extension for filtering exclusions
            file_ext = file_ext.lower()
            if filename == 'index':
                newurl = newurl[:-len(filename + file_ext)]
            if (file_ext not in excludedExtensions and disassembled.scheme in ['http', 'https'] and disassembled.fragment == ''):
                print "in : " + newurl
                if newurl not in visited: # Checking to see if URL has already been queued once
                    visited.add(newurl)
                    if urlContains(newurl, searchTags) > 0:
                        urls.put(newurl, 1)
                    else:
                        priority = priorityCalculator.searchPage(newurl, searchTags)
                        if priority < len(searchTags) + 1:
                            urls.put(newurl, priority) # Adding URL to queue with calculated priority
        except UnicodeEncodeError:
            print "UnicodeEncodeError"
        except:
            print "Invalid URL"

timestart = time.time()

while not urls.empty() and urls.counter <= urlcount:     # Crawl till queue empty or target results count is reached
    try:
        pri, url = urls.get()    # Fetch URL with highest possible priority while preserving insertion order
        regex = re.compile("mailto:|javascript:|action=edit")
        match = re.match(regex, url)      # Check for Javascript
        if not results.has_key(url) and match is None:
            print len(results)
            FileWriteUtil(pri, url)
            contents = br.response().info()["content-type"]
            mimetype = contents.split(";")[0]
            if not mimetype in ["text/html", "application/xhtml+xml", "application/rss+xml"]:
                continue
            for link in br.links():
                urlpool.put(link)
            workers=[]
            for i in range(6):
                t = threading.Thread(target = processPage)
                t.start()
                workers.append(t)
            
            for t in workers:
                t.join()
    except:
        print "other error"

while not urls.empty():
    pri, url = urls.get()   
    FileWriteUtil(pri, url)
        
    
timestop = time.time()
timetotal = timestop - timestart
print "time taken :" + str(timetotal)
downloaded = get_size('Downloads')
g = open('stats.txt','w+')
g.write("time taken :" + str(timetotal))
g.write("\nsize downloaded :" + str(downloaded))
g.flush()
print "size downloaded :" + str(downloaded)
print results
print len(results)
sorted_x = sorted(results.items(), key=lambda x: x[1])
print sorted_x
print errorcount
f.close()
g.close()
print visited








    

