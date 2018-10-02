# -*- coding: utf-8 -*-
import pyttsx3

def myPyttsx3(textNeedSpeech, rate=100):
	try:
		engine = pyttsx3.init(driverName='sapi5')
		engine.setProperty('rate', rate)
		engine.setProperty('volume', 10)
		engine.say(textNeedSpeech)
		engine.runAndWait()
	except:
		print("Lỗi myPyttsx3")