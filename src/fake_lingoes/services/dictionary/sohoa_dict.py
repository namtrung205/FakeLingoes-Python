# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bts


class SoHoaDic():
	"""object SoHoaDic"""
	def __init__(self):
		self.listMean ={}
		# self.html = ""

	# return a string with format 
	def getMean(self,word,dic = "en_vi"):
		self.html = ""
		# Get url from parameters
		url = "http://tratu.soha.vn/dict/{0}/{1}".format(dic, word.lower())
		r = requests.get(url)
		soup = bts(r.text, "html.parser")
		findOutSoup = soup.find_all("div", class_="section-h2")

		# boc html
		if (findOutSoup.__len__()) != 0:
			for sec2 in soup.find_all("div", class_="section-h2"):
				# print("Nhóm:"+ sec2.h2.text)
				# add <h2> to html
				self.html+="<h2>%s</h2>\n" % sec2.h2.text
				lsSec2 = sec2.h2.text
				# Them vao list mean-1-Nhom tu
				self.listMean[str(lsSec2)]={}
				r2 = str(sec2)
				soup2 = bts(r2, "html.parser")
				findOutSoup2 = (soup2.find_all("div", class_="section-h3"))
				if (findOutSoup2.__len__()) != 0:
					# single word
					for sec3 in soup2.find_all("div", class_="section-h3"):

						# print("Lĩnh vưc:" + sec3.h3.text)
						self.html+="\n<h3>  -%s</h3>\n" % sec3.h3.text

						self.listMean[str(lsSec2)][sec3.h3.text]={}
						r3 = str(sec3)
						soup3 = bts(r3, "html.parser")
						for sec5 in soup3.find_all("div", class_="section-h5"):

							# print("--Nghĩa:" + sec5.h5.text)
							self.html+="\n<h5>\t+%s</h5>\n" % sec5.h5.text

							self.listMean[str(lsSec2)][sec3.h3.text][sec5.h5.text]=[]
							dl = sec5.dl
							if dl != None:
								lsDl = (str(sec5.dl.text)).split("\n")
								# print(lsDl)
								for dl in lsDl[0:min(6, len(lsDl))]:
									if dl =="":
										pass
									else:
										# print("\t" + dl)
										self.html+="<p>\t+%s</p>\n" % dl
							else:
								pass
				# Multiple word
				else:
					for sec5 in soup2.find_all("div", class_="section-h5"):

						# print("--Nghĩa:" + sec5.h5.text)
						self.html+="\n<h5>\t+%s</h5>\n" % sec5.h5.text

						self.listMean[str(lsSec2)][sec5.h5.text]=[]
						dl = sec5.dl
						if dl != None:
							lsDl = (str(sec5.dl.text)).split("\n")
							# print(lsDl)
							for dl in lsDl[0:min(6, len(lsDl))]:
								if dl =="":
									pass
								else:
									# print("\t" + dl)
									self.html+="<p>\t+%s</p>\n" % dl
						else:
							pass
		else:
			self.html+="Tu tim kiem khong co nghia"
			# print("Tu tim kiem khong co nghia")
		return self.html
		

	# return a string with format 
	def getFullHtmlVi(self,word):
		self.html = ""
		# Get url from parameters
		url = "http://tratu.soha.vn/dict/{0}/{1}".format("en_vi", word.lower())
		r = requests.get(url)
		soup = bts(r.text, "html.parser")
		findOutSoup = soup.find_all("div", id="column-content")
		if findOutSoup.__len__()==0:
			contentCol = "<h3> Không tìm thấy dữ liệu, hãy thử lại...</h3>"
		else:
			contentCol = findOutSoup[0]
		
		# for contentCol in findOutSoup:
		# 	# print(contentCol)
		# 	pass	
		return (str(contentCol))

	# return a string with format 
	def getFullHtmlEn(self,word):
		self.html = ""
		# Get url from parameters
		url = "http://tratu.soha.vn/dict/{0}/{1}".format("en_en", word.lower())
		r = requests.get(url)
		soup = bts(r.text, "html.parser")
		findOutSoup = soup.find_all("div", id="column-content")
		if findOutSoup.__len__()==0:
			contentCol = "<h3> Không tìm thấy dữ liệu, hãy thử lại...</h3>"
		else:
			contentCol = findOutSoup[0]
		
		# for contentCol in findOutSoup:
		# 	# print(contentCol)
		# 	pass	
		return (str(contentCol))



# a = SoHoaDic()
# print(a.getFullHtmlEn("construction"))