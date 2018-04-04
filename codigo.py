import copy
import PIL as pil
import numpy as np
import scipy as sc
import matplotlib.pyplot as plt
import tkinter.filedialog as tkfile

def abre_img():
	loc_img = tkfile.askopenfilename()
	img = pil.Image.open(loc_img, mode='r')
	
	return img

def img_p_RGB(img):
	return np.array(img)
	
def img_p_TC(img):
	return 0

def RGB_p_TC(array_rgb):
	return 0
	
def TC_p_RGB(array_rgb):
	return 0

def RGB_p_img(array_rgb, formato):
	img = 0
	
	if formato=='.jpg':
		return 0
	if formato=='.png':
		img = pil.Image.fromarray(array_rgb, 'RGB')
	
	return img
	
def TC_p_img(array_rgb, formato):
	if formato=='.jpg':
		return 0
	if formato=='.png':
		return 0

def MSE(img1, img2):
	l1, a1 = img1.size #largura e altura img1
	l2, a2 = img2.size #largura e altura img1
	
	img1_rgb = img_p_RGB(img1)
	img2_rgb = img_p_RGB(img2)
	
	dim = img1_rgb.shape[-1]
	
	erro = 0.0
	
	if l1==l2 and a1==a2 and type(img1)==type(img2):
		for i in range(a1):
			for j in range(l1):
				for k in range(dim):
					erro += (img1_rgb[i,j,k]/255.0 - img2_rgb[i,j,k]/255.0)**2
					#print("+=", (img1_rgb[i,j,k] - img2_rgb[i,j,k])**2)
	else:
		print("imagens de tipo ou tamanho diferente!")
		
	return erro/(l1*a1)

def filtro_vermelho_RGB(array_rgb):
	nl, nc, dim = array_rgb.shape
	for i in range(nl):
		for j in range(nc):
			array_rgb[i,j,0] = 255
	
	return array_rgb
			
def filtro_vermelhoLeve_RGB(array_rgb):
	nl, nc, dim = array_rgb.shape
	for i in range(nl):
		for j in range(nc):
			array_rgb[i,j,0] += 30
			
	return array_rgb


'''
#abre uma imagem e aplica um filtro vermelho leve e forte:

img1 = abre_img() #img original
img2 = copy.copy(img1) #com filtro vermelho leve
img3 = copy.copy(img1) #com filtro vermelho forte

img1 = RGB_p_img(img_p_RGB(img1), '.png') #manter todas as imagens da mesma classe do 'pil': pil.* -> PIL.Image
img2 = RGB_p_img(filtro_vermelhoLeve_RGB(img_p_RGB(img2)), '.png')
img3 = RGB_p_img(filtro_vermelho_RGB(img_p_RGB(img3)), '.png')

img1.save("teste_MSE1.png")
img2.save("teste_MSE2.png")
img3.save("teste_MSE3.png")
'''


#teste MSE:
img1 = abre_img()
img2 = abre_img()
img3 = abre_img()

print("MSE 1-2:", MSE(img1, img2))
print("MSE 1-3:", MSE(img1, img3))




'''
#testes avulços:

loc_img = tkfile.askopenfilename()
img = pil.Image.open(loc_img, mode='r')
largura_img, altura_img = img.size

print(loc_img, "\n", largura_img, "x", altura_img, "\nformato: ", type(img))

#img.show()

img_rgb = np.array(img)
print(img_rgb)
#print("img_rgb[2,2]: ",img_rgb[2,2], "  ", img_rgb.shape[1], "x", img_rgb.shape[0], "  ", img_rgb[2,2].shape[0])
print(img_rgb.shape)

img = pil.Image.fromarray(img_rgb, 'RGB')
#img = pil.JpegImagePlugin.fromarray(img_rgb, 'RGB')

img.show()

#print(type(img))
#img.save('output.png')

#img = pil.JpegImagePlugin.JpegImageFile(img)

#print(type(img))



#img1 = abre_img()
#img2 = abre_img()
#MSE(img1, img2)
'''