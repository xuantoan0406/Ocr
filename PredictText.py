import cv2
import config
from PIL import Image
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from utils import show_img
import time


class GetTextBox:
	
	@staticmethod
	def get_text_box(pathImg):
		
		img = cv2.imread(pathImg)
		img = cv2.resize(img, (1682, 2378))
		gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		th, threshed = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
		kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (40, 3))
		dilation = cv2.dilate(threshed, kernel=kernel, iterations=1)
		contours, _ = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		fullBox = []
		# show_img(threshed, 900)
		for cnt in contours:
			if cv2.contourArea(cnt) > 900:
				x, y, w, h = cv2.boundingRect(cnt)
				fullBox.append((x, y, x + w, y + h))
		# 		cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
		# show_img(img, 900)
		return fullBox
	
	@staticmethod
	def filter_box(boxes):
		print("a")
	
	@staticmethod
	def sorted_box(boxes):
		listBox = filter(lambda x: (250 > x[3] - x[1] > 20), boxes)
		listBox = sorted(listBox, key=lambda x: x[1])
		newListBox = []
		for i in range(len(listBox)):
			if i == len(listBox) - 1:
				continue
			else:
				if listBox[i + 1][1] - listBox[i][1] < 25 and abs(listBox[i + 1][0] - listBox[i][0]) > 60:
					twoBox = sorted((listBox[i], listBox[i + 1]), key=lambda x: x[0])
					
					if not newListBox:
						newListBox.append(twoBox[0])
					else:
						if twoBox[0] != newListBox[-1] and twoBox[1] != newListBox[-1]:
							newListBox.append(twoBox[0])
						else:
							newListBox[-1] = twoBox[0]
					newListBox.append([])
					newListBox.append(twoBox[1])
				else:
					if not newListBox:
						newListBox.append(listBox[i])
					if newListBox[-1] != listBox[i + 1] or newListBox[-1] != listBox[i]:
						newListBox.append(listBox[i + 1])
		
		return newListBox


class PredictText:
	def __init__(self):
		self.config = Cfg.load_config_from_name(config.MODEL_OCR)
		self.config['device'] = config.DEVICE
		self.detector = Predictor(self.config)
		self.getTextBox = GetTextBox()
	
	@staticmethod
	def clear_text_error(textsPredict):
		fullTextPredict = []
		for text, confidence in zip(textsPredict[0], textsPredict[1]):
			
			if confidence < 0.6:
				fullTextPredict.append("")
			else:
				fullTextPredict.append(text)
		return fullTextPredict
	
	def predict_text(self, pathImg):
		image = Image.open(pathImg)
		image = image.resize((1682, 2378), Image.LANCZOS)
		fullBox = self.getTextBox.get_text_box(pathImg)
		fullBox = self.getTextBox.sorted_box(fullBox)
		i = 0
		fullLines = []
		iTabs = []
		for box in fullBox:
			if box:
				lineImage = image.crop((box[0], box[1], box[2], box[3]))
				fullLines.append(lineImage)
				i += 1
			else:
				iTabs.append(i)
		
		fullTextPredict = self.detector.predict_batch(fullLines, return_prob=True)
		fullTextPredict = PredictText.clear_text_error(fullTextPredict)
		j = 0
		for i in iTabs:
			i -= j
			fullTextPredict[i - 1] = fullTextPredict[i - 1] + "\t" * 3 + fullTextPredict[i]
			fullTextPredict.pop(i)
			j += 1
		
		for text in fullTextPredict:
			if text == "":
				fullTextPredict.remove(text)

		return fullTextPredict


# st = time.time()
# a = PredictText()
# a.predict_text("image/letter_1.png")
#
# print(time.time() - st)

