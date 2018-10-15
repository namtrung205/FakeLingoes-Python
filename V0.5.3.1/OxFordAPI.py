# -*- coding: utf-8 -*-

import  requests
import json
# from json import JSONDecodeError


# The Custom Exceptions 
class WordNotFound(Exception):
	"""docstring for WordNotFound"""
	def __init__(self):
		pass

class OxFordDic():
	# Set your app_id and app_key
	def __init__(self, app_id, app_key ,language ="en"):
		self.app_id = app_id
		self.app_key = app_key
		self.language = language
		self.html = ""

	def getJson(self, word_id ):
		try:
			url = 'https://od-api.oxforddictionaries.com:443/api/v1/entries/'  + self.language + '/'  + word_id.lower()
			r = requests.get(url, headers = {'app_id' : self.app_id, 'app_key' : self.app_key})
			jsonData = r.json()
			return jsonData
		except:
			return None
	def JsonToDic(self, word_id):
		try:
			html = ""
			jsonDataUpdate = self.getJson(word_id.lower())
			html +="<h3>Word: %s (%s)</h3>\n" % (jsonDataUpdate["results"][0]["word"], jsonDataUpdate["results"][0]["lexicalEntries"][0]["pronunciations"][0]["phoneticSpelling"])
			# html +="<h3>Word: (%s)/h3>\n" %(jsonDataUpdate["results"][0]["lexicalEntries"][0]["pronunciations"][0]["phoneticSpelling"])
			lexicalEntries = jsonDataUpdate["results"][0]["lexicalEntries"] #gom 4 entries

			for lexicalEntry in lexicalEntries:
				lexicalCategory = lexicalEntry["lexicalCategory"]
				html +=("<h4>%s .%s </h4>\n" % (str(lexicalEntries.index(lexicalEntry)+1), lexicalCategory))
				entries = lexicalEntry["entries"]
				for entry in entries:
					senses = entry['senses']
					for defAndExs in senses: 
						if "definitions" not in defAndExs.keys():
							defAndExs["definitions"]=[""]
						definitions = defAndExs["definitions"]
						html +=("<h4><font color='blue'>%s: </font></h4>\n" % definitions[0])
						if "examples" not in defAndExs.keys():
							defAndExs["examples"]=""
						examples = defAndExs["examples"] # 1 danh sach vi du
						for ex in examples:		
							html +=("<p>- %s </p>\n" % (ex["text"]))

			self.html = html
			return html
		except:
			return None

	# Method return meaning of the word and classify by word class (html)
	def getHtml(self, word_id):
		try:
			# self.getJson(word_id)
			self.JsonToDic(word_id.lower())
			return self.html
		except:
			self.html = "<h3>The word are not in the database</h3>"
			return self.html

