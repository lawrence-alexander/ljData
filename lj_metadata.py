# Gathers tabulated data (username, account number and registration date)
# on extended network of LiveJournal accounts, based on friends-of-friends of starting user

# By Lawrence Alexander @LawrenceA_UK

import requests
import time
import argparse
from BeautifulSoup import BeautifulStoneSoup
import re
import csv
import urllib

# define arguments

ap = argparse.ArgumentParser()
ap.add_argument("-u","--username",    required=True,help="Enter username of starting LiveJournal account.")
args = vars(ap.parse_args())
ljuser = args['username']

outCSV = "LiveJournal_blogs.csv"

# Main function to extract an LJ user's friends

def getFriends(username, allfriends):   
        
    url  = "http://www.livejournal.com/misc/fdata.bml?user=" + username
    
    user_agent = {'User-Agent': 'Web scraper by la2894@my.open.ac.uk @LawrenceA_UK'}
    
    print "Getting friends for user " + username
    try:
        
        response = requests.get(url, headers=user_agent)    
    except:
        print "Error getting page: " + url
        pass
    
    # Process response
        
    if response.status_code == 200:        
        userFriends= response.content
        outFriends = userFriends.split(">")
        inFriends = userFriends.split("<")
        allFriends = []        
        
        for x in range(1, len(outFriends) - 2):
            friendName= outFriends[x]
            allFriends.append(friendName)
            
        for y in range(1, len(inFriends) - 2):
            friendName= inFriends[y]
            allFriends.append(friendName)                   
            getFriends.allfriends = allFriends
        
            return (allfriends)

# get network from starting user

getFriends (username=ljuser, allfriends=[])
all_friends=getFriends.allfriends
all_friends = list(set(all_friends)) 

friendsOf=[]

for user in all_friends:
    time.sleep(1) # Good manners
    getFriends(username=user, allfriends=[])    
    friendsOf.extend(getFriends.allfriends)
    
all_friends.extend(friendsOf)

# Remove any duplicates from friends list

clean = []
for f in all_friends:
    if f not in clean:
            clean.append(f)          
all_friends = clean 

print "Usernames collected: " + str(len(all_friends))

for accountName in all_friends:   
    time.sleep(1) # Good manners
    accountName=accountName.replace(" ", "")
    accountName=accountName.rstrip()    
    
    url  = "http://%s" % urllib.quote(accountName)
    
    url += ".livejournal.com/data/foaf.rdf"   
        
    user_agent = {'User-Agent': 'Web scraper by lawz.alexander@gmail.com @LawrenceA_UK'}
    print "Getting metadata for user " + accountName    
            
    response = requests.get(url, headers=user_agent)
    
    try:
        
        if response.status_code == 200:
            
            soup = BeautifulStoneSoup(response.content)            
            result = soup.contents[3].contents[1]    
            nickname = soup.contents[3].contents[1].contents[1].contents[0]    
            accountno = soup.findAll('foaf:img', limit=1)  
            
            # Get blog creation date and time
            
            timestamp_pattern='lj:datecreated(.+?) '
            pattern=re.compile(timestamp_pattern)
            datestamp = soup.findAll(name='foaf:weblog', limit=1)
            datestamp=re.findall(pattern,str(datestamp))
            datestamp=str(datestamp)
            datestamp=datestamp.strip( "\'']" )
            datestamp=datestamp.strip( "'['=")
            datestamp=datestamp.strip('"')
            
            # Get sequential LiveJournal account number from avatar URL
            
            account_pattern='rdf:resource="(.+?\d)"'
            pattern=re.compile(timestamp_pattern)
            account=re.findall(account_pattern,str(accountno))
            account=account[0]
            account = account[-8:]
            datestamp=datestamp[:10]
            
            acnumber=int(account)
            
            # Filter by time period of interest
            
            if acnumber > 68000000 and acnumber < 71500000:
                troll_flag="Yes"
            else:
                troll_flag="No"
                
            with open(outCSV, 'a') as ljData:
                
                blogs = csv.writer(ljData, delimiter=',', lineterminator='\n', dialect='excel')        
                blogs.writerow([nickname] + [datestamp] + [account] + [troll_flag])        
                ljData.close()    
    
    except:
        print "Error getting account."
        pass
    
print "Complete. CSV file written." 