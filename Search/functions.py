from Find import Find
import cPickle as pickle
import enchant
from enchant import DictWithPWL
import os

class Search:
	ranks = {}
	keyweights = {}
	hash_table = {}
	titles = {}
	d = {}
		
	def __init__(self):
		f = open(str(os.getcwd()) + "/data/keyweights.p", "rb")
		self.keyweights = pickle.load(f)
		f.close()
		
		f = open(str(os.getcwd()) + "/data/data.p", "rb")
		self.hash_table = pickle.load(f)
		f.close()
		
		with open(str(os.getcwd()) + "/data/pageranks.p","rb") as fp:
			self.ranks = pickle.load(fp)
			
		with open(str(os.getcwd()) + "/data/titles.p","rb") as fp:
			self.titles = pickle.load(fp)
		
		self.d = DictWithPWL("en_US", str(os.getcwd()) + "/data/allkeys.txt")
	
	def swap(self, listOfUrls, i, j):
		tmp = listOfUrls[i]
		listOfUrls[i] = listOfUrls[i-1]
		listOfUrls[i-1] = tmp
		return


	def hashFunc(self,key):
		hashout = 0
		for i in range(len(key)):
			hashout = hashout + ord(key[i])
		return hashout
	

	def findinKeyTable(self, key, Table):
		hashkey = self.hashFunc(key)
		if hashkey in Table:
			for i in range(len(Table[hashkey])):
				if Table[hashkey][i][1] == key:
					return i
			return False
		return False


	def spellCheck(self, word):
		if self.d.check(word) == True:
			return True
		else:
			suggest = self.d.suggest(word)
			for i in range(len(suggest)):
				suggest[i] = suggest[i].lower()
			#keyweights = getKeyWeights()
			bestweight = 0
			bestword = suggest[0]
			for entry in suggest:
				hashkey = self.hashFunc(entry)
				secKey = self.findinKeyTable(entry, self.keyweights)
				if secKey != False:
					if self.keyweights[hashkey][secKey][0] >= bestweight:
						bestword = self.keyweights[hashkey][secKey][1]
						bestweight = self.keyweights[hashkey][secKey][0]
				return bestword
			return False
		

	def ngrams(self, word):
		Ngrams = []
		for i in range(3,len(word)+1):
			Ngrams.append(word[ : i])
		return Ngrams
	

	def exactQuery(self, entry):
		return entry.split()


	def Query(self, entry):
		words = entry.split() #words has to be returned somehow
		searchlist = []
		for i in range(len(words)):
			searchlist = searchlist + self.ngrams(words[i].lower())
		#print searchlist
		return searchlist
	
	
	def Sort(self, listOfUrls):
		loc_ranks = []
		for url in listOfUrls:
			hashkey = self.hashFunc(url)
			for i in range(len(self.ranks[hashkey])):
				if self.ranks[hashkey][i][0] == url:
					loc_ranks.append(self.ranks[hashkey][i][1])
		for i in range(1,len(listOfUrls)):
			if loc_ranks[i] > loc_ranks[i-1]:
				self.swap(listOfUrls, i, i-1)
		return listOfUrls
	
	def removeRepeats(self, result):
		for i in range(len(result)):
			for j in range(i):
				if result[i] == result[j]:
					result[i] = 0
		resultFinal = filter(lambda a: a != 0, result)
		return resultFinal
	

	def primarySort(self, result, matches):
		for i in range(1,len(result)):
			if matches[i] > matches[i-1]:
				self.swap(result, i, i-1)
		resultSort = self.removeRepeats(result)
		return resultSort


	def findin(self, key, query, table):
		for i in range(len(table[key])):
			if table[key][i][0] == query:
				return i
		return -1

	def numberOfMatches(self, url, result):
		Count = 0
		for link in result:
			if url == link:
				Count = Count + 1
		return Count

	
	def search(self, query):
		result = []
		searchlist = self.Query(query)
		for i in range(len(searchlist)):
			key = self.hashFunc(searchlist[i])
			secKey = self.findin(key, searchlist[i], self.hash_table)
			if secKey == -1:
				return []
			temp = self.hash_table[key][secKey][1 :]
			for j in range(len(temp)):
				#if Find(result, temp[j]) == 0:
				result.append(temp[j])
		matches = []
		#before sorting, first sort according to no. of matches
		for link in result:
			matches.append(self.numberOfMatches(link, result))
		result = self.Sort(result)
		result = self.primarySort(result, matches)
		final = [[] for i in range(len(result))]
		for i in range(len(result)):
			try:
				if self.titles[result[i]] == '': final[i] = [result[i], result[i]]
				else: final[i] = [result[i], self.titles[result[i]]]
			except:
				final[i] = [result[i], result[i]]
		return final
		
		
	def searchWSC(self, query):
		change = False
		searchlist = query.split()
		for i in range(len(searchlist)):
			bestword = self.spellCheck(searchlist[i])
			if bestword != True: 
				searchlist[i] = bestword
				change = True
		changedEntry = ""
		if change:
			for word in searchlist:
				changedEntry = changedEntry + word + " "
			result = self.search(changedEntry)
		else: result = self.search(query)
		return {'change' : change,'query' : changedEntry , 'search' : result}
