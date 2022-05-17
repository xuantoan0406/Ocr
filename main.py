from ProcessToFileText import *
import os
import time
import shutil
import argparse
from ProcessToFileText import ProcessToFileText

parser = argparse.ArgumentParser()
parser.add_argument("-i", "--inputType", type=str, required=True, default='image')
parser.add_argument("-pi", "--pathInput", type=str, required=True)
parser.add_argument("-ps", "--pathFolderSave", type=str, required=True)
parser.add_argument("-t", "--saveType", type=str, required=True, default='docx')
args = vars(parser.parse_args())
processToFileText = ProcessToFileText()
if args["inputType"] == "image":
	if os.path.isdir(args["pathInput"]):
		for image in os.listdir(args["pathInput"]):
			processToFileText.process_with_one_file(args["pathInput"] + f'/{image}', args["saveType"],
			                                        args["pathFolderSave"])
	else:
		processToFileText.process_with_one_file(args["pathInput"], args["saveType"], args["pathFolderSave"])

if args["inputType"] == "pdf":
	if os.path.isdir(args["pathInput"]):
		listFolderImage = processToFileText.convert_folder_pdf(args["pathInput"])
		for folderImage in listFolderImage:
			processToFileText.process_with_folder(folderImage, args["saveType"], args["pathFolderSave"])
	
	else:
		outFolderImage = processToFileText.covert_pdf_to_img(args["pathInput"])
		processToFileText.process_with_folder(outFolderImage, args["saveType"], args["pathFolderSave"])
	for folder in os.listdir("imagePdf"):
		shutil.rmtree(os.path.join("imagePdf", folder))
# python3 main.py -i image -pi image -ps newDoc -t docx

