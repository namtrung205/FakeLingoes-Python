import os
from PIL import Image, ImageEnhance
from pytesseract import image_to_string, pytesseract

from fake_lingoes.services.ocr.orc_space_lib import OCRSpace

def ImageToText(image=os.path.join("Capture", "capture.png")):
	try:
		imgOriginal = Image.open(image)

		imgColor = ImageEnhance.Color(imgOriginal)
		imgColorE = imgColor.enhance(0)

		imgSharpe = ImageEnhance.Sharpness(imgColorE)
		imgSharpeE = imgSharpe.enhance(1.75)

		imgContrast = ImageEnhance.Contrast(imgSharpeE)
		imgContrastE = imgContrast.enhance(5)

		output_path = os.path.join("Capture", "capture2.png")
		imgContrastE.save(output_path)

		imgModified = Image.open(output_path)
		# NOTE: This path is hardcoded for Windows x86/x64 systems. 
		# In a real app, this should be configurable or bundled.
		pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

		text = image_to_string(imgModified)
		print(text)
		return text
	except Exception as e:
		print("Error:" + str(e))

def ImageToText_Api(api_key, image=os.path.join("Capture", "capture.png")):
	try:
		imgOriginal = Image.open(image)

		imgColor = ImageEnhance.Color(imgOriginal)
		imgColorE = imgColor.enhance(1)

		imgSharpe = ImageEnhance.Sharpness(imgColorE)
		imgSharpeE = imgSharpe.enhance(1)

		imgContrast = ImageEnhance.Contrast(imgSharpeE)
		imgContrastE = imgContrast.enhance(1)

		output_path = os.path.join("Capture", "capture2.png")
		imgContrastE.save(output_path)

		# Set your APi key
		myOrc_Api = OCRSpace(api_key)
		return myOrc_Api.ocr_file(output_path)
	except Exception as e:
		print("Error:" + str(e))

