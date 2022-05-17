from PredictText import PredictText
import os
import time
from utils import show_img, write_text, write_docx
import fitz


class ProcessToFileText:
	
	def __init__(self):
		self.predictText = PredictText()
	
	def process_with_folder(self, pathFolder, saveType, pathFolderSave):
		if not os.path.isdir(pathFolderSave):
			os.makedirs(pathFolderSave)
		allTextPredict = []
		nameFile = pathFolder.split("/")[-1]
		st = time.time()
		for i in range(len(next(os.walk(pathFolder))[2])):
			textPredict = self.predictText.predict_text(os.path.join(pathFolder, f"{nameFile}_{i+1}.png"))
			allTextPredict.append(textPredict)
		if saveType == 'txt':
			write_text(allTextPredict, f"{pathFolderSave}/{nameFile}")
		if saveType == 'docx':
			write_docx(allTextPredict, f"{pathFolderSave}/{nameFile}")
		print(f"{nameFile}........ok")
		print(time.time() - st)
		return "ok"
	
	def process_with_one_file(self, pathImg, saveType, pathFolderSave):
		folder, fileName = os.path.split(pathImg)
		if not os.path.isdir(pathFolderSave):
			os.makedirs(pathFolderSave)
		
		st = time.time()
		fileName = fileName[:-4]
		fullText = [self.predictText.predict_text(pathImg)]
		
		if saveType == 'txt':
			write_text(fullText, f"{pathFolderSave}/{fileName}")
		if saveType == 'docx':
			write_docx(fullText, f"{pathFolderSave}/{fileName}")
		print(f"{fileName}........ok")
		print(time.time() - st)
		return "ok"
	
	@staticmethod
	def covert_pdf_to_img(pathPdf):
		head, filePdf = os.path.split(pathPdf)
		fileName = filePdf.rstrip(".pdf")
		pathOutput = f"imagePdf/{fileName}"
		if not os.path.isdir(pathOutput):
			os.makedirs(pathOutput)
		doc = fitz.open(pathPdf)
		
		zoom = 2
		mat = fitz.Matrix(zoom, zoom)
		for i in range(len(doc)):
			pix = doc[i].get_pixmap(matrix=mat)
			output = f"{pathOutput}/{fileName}_{i + 1}.png"
			
			pix.save(output)
		return pathOutput
	
	@staticmethod
	def convert_folder_pdf(inputFolder):
		listOutPut = []
		for pathPdf in os.listdir(inputFolder):
			folderAFilePdf = f"imagePdf/{pathPdf[:-4]}"
			if not os.path.isdir(folderAFilePdf):
				os.makedirs(folderAFilePdf)
			pathOutPut = ProcessToFileText.covert_pdf_to_img(f"{inputFolder}/{pathPdf}")
			listOutPut.append(pathOutPut)
		return listOutPut
