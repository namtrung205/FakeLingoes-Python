# -*- coding: utf-8 -*-
import pyttsx3

def myPyttsx3(textNeedSpeech, rate=100):
	try:
		# Remove driverName='sapi5' to support cross-platform (it will auto-detect)
		engine = pyttsx3.init()
		engine.setProperty('rate', rate)
		engine.setProperty('volume', 10)
		engine.say(textNeedSpeech)
		engine.runAndWait()
	except:
		print("Error myPyttsx3")