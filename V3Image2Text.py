# -*- coding: utf-8 -*-
from PIL import Image, ImageEnhance
from pytesseract import image_to_string

from orcSpaceLib import OCRSpace

def ImageToText(image=".\Capture\\capture.png"):
	imgOriginal = Image.open(image)


	imgColor = ImageEnhance.Color(imgOriginal)
	imgColorE = imgColor.enhance(0)

	imgSharpe = ImageEnhance.Sharpness(imgColorE)
	imgSharpeE = imgSharpe.enhance(1.75)



	imgContrast = ImageEnhance.Contrast(imgSharpeE)
	imgContrastE = imgContrast.enhance(10)

	imgContrastE.save(".\Capture\\capture2.png")

	imgModified = Image.open(".\Capture\\capture2.png")

	text = image_to_string(imgModified)
	print(text)
	return text

def ImageToText_Api(image=".\Capture\\capture.png"):
	try:
		imgOriginal = Image.open(image)

		imgColor = ImageEnhance.Color(imgOriginal)
		imgColorE = imgColor.enhance(0)

		imgSharpe = ImageEnhance.Sharpness(imgColorE)
		imgSharpeE = imgSharpe.enhance(1.5)

		imgContrast = ImageEnhance.Contrast(imgSharpeE)
		imgContrastE = imgContrast.enhance(5)

		imgContrastE.save(".\Capture\\capture2.png")


		myOrc_Api = OCRSpace()
		return myOrc_Api.ocr_file(".\Capture\\capture2.png")
	except:
		pass