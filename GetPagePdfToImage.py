import fitz
import os

def covert_to_img(pathPdf, pathOutput):
	if not os.path.isdir(pathOutput):
		os.makedirs(pathOutput)
	head, filePdf = os.path.split(pathPdf)
	fileName = filePdf.rstrip(".pdf")
	doc = fitz.open(pathPdf)
	zoom = 2
	mat = fitz.Matrix(zoom, zoom)
	for i in range(len(doc)):
		pix = doc[i].get_pixmap(matrix=mat)
		output = f"{pathOutput}/{fileName}_{i+1}.png"
		pix.save(output)
	return "success"

# for j,k in doc:
# 	print(k)
# 	a=j.get_text('words')
# 	for text in a :
# 		print(text[4])

covert_to_img("test2.pdf","test2")