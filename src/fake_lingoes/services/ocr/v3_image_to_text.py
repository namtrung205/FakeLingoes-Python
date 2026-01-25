import os
from PIL import Image, ImageEnhance
from pytesseract import image_to_string, pytesseract

from fake_lingoes.services.ocr.orc_space_lib import OCRSpace

def ImageToText(image=os.path.join("capture", "capture.png")):
	try:
		imgOriginal = Image.open(image)

		imgColor = ImageEnhance.Color(imgOriginal)
		imgColorE = imgColor.enhance(0)

		imgSharpe = ImageEnhance.Sharpness(imgColorE)
		imgSharpeE = imgSharpe.enhance(1.75)

		imgContrast = ImageEnhance.Contrast(imgSharpeE)
		imgContrastE = imgContrast.enhance(5)

		output_path = os.path.join("capture", "capture2.png")
		imgContrastE.save(output_path)

		imgModified = Image.open(output_path)
		
		# Proactively find Tesseract path
		if os.name == 'nt':  # Windows
			tesseract_paths = [
				r'C:\Program Files\Tesseract-OCR\tesseract.exe',
				r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
				os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Tesseract-OCR", "tesseract.exe"),
				os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Tesseract-OCR", "tesseract.exe"),
			]
			
			found_path = None
			for path in tesseract_paths:
				if os.path.exists(path):
					found_path = path
					break
			
			if found_path:
				pytesseract.tesseract_cmd = found_path
			else:
				print("Warning: Tesseract-OCR not found in standard Windows paths.")
		else:
			# On Linux/macOS, tesseract is usually in PATH
			pytesseract.tesseract_cmd = 'tesseract'

		text = image_to_string(imgModified)
		print(text)
		return text
	except Exception as e:
		print("Error:" + str(e))

def ImageToText_Api(api_key, image=os.path.join("capture", "capture.png")):
	try:
		imgOriginal = Image.open(image)

		imgColor = ImageEnhance.Color(imgOriginal)
		imgColorE = imgColor.enhance(1)

		imgSharpe = ImageEnhance.Sharpness(imgColorE)
		imgSharpeE = imgSharpe.enhance(1)

		imgContrast = ImageEnhance.Contrast(imgSharpeE)
		imgContrastE = imgContrast.enhance(1)

		output_path = os.path.join("capture", "capture2.png")
		imgContrastE.save(output_path)

		# Set your APi key
		myOrc_Api = OCRSpace(api_key)
		return myOrc_Api.ocr_file(output_path)
	except Exception as e:
		print("Error:" + str(e))

