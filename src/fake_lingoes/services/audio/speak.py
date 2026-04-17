# -*- coding: utf-8 -*-
import pyttsx3

# Initialize engine globally to avoid garbage collection issues
try:
	engine = pyttsx3.init()
except Exception as e:
	print(f"Error initializing pyttsx3: {e}")
	engine = None

def myPyttsx3(textNeedSpeech, rate=100):
	if engine is None:
		print("Error: TTS engine not initialized")
		return

	try:
		# Remove driverName='sapi5' to support cross-platform (it will auto-detect)
		engine.setProperty('rate', rate)
		engine.setProperty('volume', 1.0)
		engine.say(textNeedSpeech)
		engine.runAndWait()
	except Exception as e:
		print(f"Error myPyttsx3: {e}")