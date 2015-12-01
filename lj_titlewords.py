# -*- coding: UTF-8 -*-

# Gather words from titles of recent LiveJournal blog entries based on input file 
# By Lawrence Alexander @LawrenceA_UK

import codecs
import feedparser
import urllib
import time
import re

# Set source and output files

inputfile = "blogs.txt"
outputfile = "blogs_titlewords.txt"


outfile = codecs.open(outputfile, 'a', 'utf-8')

allWords = []

with open(inputfile) as infile:
    
    for account in infile:
        account=account.strip()
        time.sleep(1)  
        
        print "Getting post titles for user: " + account
        url  = "http://%s" % urllib.quote(account)            
        url += ".livejournal.com/data/rss"         
        
        try:
            feed = feedparser.parse(url,agent='Web scraper by la2894@my.open.ac.uk @LawrenceA_UK')
            
        except:
            print "Error getting user: " + account
            continue
        
        # Get titles of last five posts
        
        for i in range (0,4):
            
            try:
                # Get post title
                titleText= feed.entries[i].title
                
                # Get list of words from post title
                titleWords = re.findall(r'[\w]+',titleText,re.U)
                
                
                # Append them to output file
                for titleWord in titleWords:                    
                    outfile.write(titleWord + u"\n")

            except:
                pass


print "Finished collecting title words."

outfile.close()
infile.close()