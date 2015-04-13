from Find import Find
import cPickle as pickle
#import dropbox
import enchant
from enchant import DictWithPWL
from enchant.checker import SpellChecker
#from main import *

#hash_table = {}
code = 0
ranks = []
keyweights = {}
d = DictWithPWL("en_US", "allkeys.txt")

def getKeyWeights():
	global keyweights
	f = open("keyweights.p", "rb")
	keyweights = pickle.load(f)
	f.close()
	return keyweights

#def getCode():
#	global code
#	if code == 0:
#		code = raw_input("Enter authorization code: ")
#	return code

def getData():
	f = open("data.p", "rb")
	hash_table = pickle.load(f)
	f.close()
	return hash_table
	
def getRanks():
	global ranks
	f = open("ranks.txt" ,"r")
	ranks = f.readlines()
	f.close()
	return ranks
	
def swap(listOfUrls, i, j):
	tmp = listOfUrls[i]
	listOfUrls[i] = listOfUrls[i-1]
	listOfUrls[i-1] = tmp


def hashFunc(key):
	hashout = 0
	for i in range(len(key)):
		hashout = hashout + ord(key[i])
	return hashout
	

def findinKeyTable(key, Table):
	hashkey = hashFunc(key)
	if hashkey in Table:
		for i in range(len(Table[hashkey])):
			if Table[hashkey][i][1] == key:
				return i
		return False
	return False


def spellCheck(word):
	if d.check(word) == True:
		return True
	else:
		suggest = d.suggest(word)
		for i in range(len(suggest)):
			suggest[i] = suggest[i].lower()
		#keyweights = getKeyWeights()
		bestweight = 0
		bestword = suggest[0]
		for entry in suggest:
			hashkey = hashFunc(entry)
			secKey = findinKeyTable(entry, keyweights)
			if secKey != False:
				if keyweights[hashkey][secKey][0] >= bestweight:
					bestword = keyweights[hashkey][secKey][1]
					bestweight = keyweights[hashkey][secKey][0]
			return bestword
		return False
		

def ngrams(word):
	Ngrams = []
	for i in range(3,len(word)+1):
		Ngrams.append(word[ : i])
	return Ngrams
	

def exactQuery(entry):
	return entry.split()


def Query(entry):
	words = entry.split() #words has to be returned somehow
	searchlist = []
	for i in range(len(words)):
		searchlist = searchlist + ngrams(words[i].lower())
	#print searchlist
	return searchlist
	
	
def Sort(listOfUrls):
	#f = open(file_name, "r")	#pageranks file
	#ranks = f.readlines()
	with open("pageranks.p","rb") as fp:
		table = pickle.load(fp)
	ranks = []
	for url in listOfUrls:
		hashkey = hashFunc(url)
		for i in range(len(table[hashkey])):
			if table[hashkey][i][0] == url:
				ranks.append(table[hashkey][i][1])
	for i in range(1,len(listOfUrls)):
		if ranks[i] > ranks[i-1]:
			swap(listOfUrls, i, i-1)
	return listOfUrls
	
def removeRepeats(result):
	for i in range(len(result)):
		for j in range(i):
			if result[i] == result[j]:
				result[i] = 0
	resultFinal = filter(lambda a: a != 0, result)
	return resultFinal
	

def primarySort(result, matches):
	for i in range(1,len(result)):
		if matches[i] > matches[i-1]:
			swap(result, i, i-1)
	resultSort = removeRepeats(result)
	return resultSort


def findin(key, query, table):
	for i in range(len(table[key])):
		if table[key][i][0] == query:
			return i
	return -1

def numberOfMatches(url, result):
	Count = 0
	for link in result:
		if url == link:
			Count = Count + 1
	return Count


def Search(searchlist, file_name, hash_table):
	result = []
	for i in range(len(searchlist)):
		key = hashFunc(searchlist[i])
		table = hash_table
		secKey = findin(key, searchlist[i], table)
		if secKey == -1:
			return -1
		temp = table[key][secKey][1 :]
		for j in range(len(temp)):
			#if Find(result, temp[j]) == 0:
			result.append(temp[j])
	matches = []
	#before sorting, first sort according to no. of matches
	for link in result:
		matches.append(numberOfMatches(link, result))
	result = Sort(result)
	result = primarySort(result, matches)
	return result
		
def SearchFinal(entry, hash_table):
	#getCode()
	#ranks = getRanks(code)
	return Search(Query(entry), "NGramkeys.txt", hash_table) 

