import mtranslate
from googletrans import Translator


# Translate_ return a string
def googleTrans(myText,fromLang='en', toLang='vi'):
	outText = "Lỗi!!! Không thể dịch được"
	try:
		outText = str(mtranslate.translate(myText, to_language=toLang, from_language=fromLang))
		return outText
	except :
		try:
			myTransTool = Translator()
			myTrans = myTransTool.translate(myText,src=fromLang, dest = toLang)
			outText = str(myTrans.text)
			return outText
		except:
			print("Error googletrans 1")
	return outText

