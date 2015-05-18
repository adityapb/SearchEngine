#find in listLinks

def Find(listKeys, key):
	for i in range(len(listKeys)):
		if key==listKeys[i]:
			return True
	return False

#returns index of url in the list of links
#def findInList(links,url):
#	for i in range(len(links)):
#		if url == links[i]:
#			return i
#	return -1
