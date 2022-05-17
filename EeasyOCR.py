import easyocr
import cv2
from utils import show_img
import time
st=time.time()
# import config
from vietocr.tool.predictor import Predictor
from vietocr.tool.config import Cfg
from PIL import Image


path= 'image/letter_0.png'
img=cv2.imread(path)
image = Image.open(path)
print(image)
# image = image.resize((1682, 2378), Image.Resampling.LANCZOS)
config = Cfg.load_config_from_name('vgg_transformer')
config['device'] = 'cuda:0'
reader = easyocr.Reader(['vi'],gpu=True) # this needs to run only once to load the model into memory
result = reader.readtext(path)
# result=reader.detect(img)
detector = Predictor(config)
# print("aaa")
for i in result:
    print(i[0][0][0])
    x1,y1,x2,y2=int(i[0][0][0]), int(i[0][0][1]), int(i[0][2][0]), int(i[0][2][1])
    if x1<x2 and y1<y2:
        textPredict = detector.predict(image.crop((x1, y1, x2, y2)), return_prob=True)
        print(i[1],"-------------",textPredict[0])
        cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
cv2.imwrite("test/19.jpg", img)
print(time.time()-st)
# show_img(img,900)