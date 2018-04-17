import numpy as np
import scipy as sc
from PIL import Image as pil
import copy
import matplotlib.pyplot as plt

#1
def img_p_rgba(loc_img):
	img = pil.open(loc_img, 'r')
	array = np.array(img.convert('RGBA'))
	
	return array

#2
def rgba_p_tc(array_rgba, tipo):
	nl = array_rgba.shape[0]
	nc = array_rgba.shape[1]
	
	array_tc = np.zeros((nl,nc)).astype(np.uint8)
		
	#leveza
	if tipo == 1:	
		array_tc[:, :] = ( array_rgba[:,:,:-1].astype(np.uint16).max(axis=2)+array_rgba[:,:,:-1].astype(np.uint16).min(axis=2) ) / 2
	
	#media
	if tipo == 2:
		array_tc[:, :] = (np.uint16(array_rgba[:,:,0]) + np.uint16(array_rgba[:,:,1]) + np.uint16(array_rgba[:,:,2]))//3
		
	#luminosidade
	if tipo == 3:
		array_tc[:, :] = 0.21*array_rgba[:,:,0] + 0.72*array_rgba[:,:,1] + 0.07*array_rgba[:,:,2]
		
	return array_tc

#3
def tc_p_rgba(array_tc):
	nl = array_tc.shape[0]
	nc = array_tc.shape[1]
	
	array_rgba = np.zeros((nl,nc, 4)).astype(np.uint8)	
	
	#tc media
	array_rgba[:,:,0] = np.uint8(array_tc[:,:])
	array_rgba[:,:,1] = np.uint8(array_tc[:,:])	
	array_rgba[:,:,2] = np.uint8(array_tc[:,:])
	array_rgba[:,:,3] = 255
	
	
	return array_rgba

		
#recebe uma tupla contento na primeira posição um vetor indicando o tamanho de cada canal
#e na segunda posicao a matriz rgba 16 bits
def conversorImgQuantizada(rgba_eq):
	
	rgba8bits = np.zeros(rgba_eq[1].shape).astype(np.uint8)
	rgba8bits[:,:,0] = ( rgba_eq[1][:,:,0]/(2**rgba_eq[0][0]-1) ) * 255
	rgba8bits[:,:,1] = ( rgba_eq[1][:,:,1]/(2**rgba_eq[0][1]-1) ) * 255
	rgba8bits[:,:,2] = ( rgba_eq[1][:,:,2]/(2**rgba_eq[0][2]-1) ) * 255
	rgba8bits[:,:,3] = rgba_eq[1][:,:,3]
	
	return rgba8bits	


def quantizadorUniforme(rgba_array, bitsR, bitsG, bitsB):
	r = range(1, 17)
	if bitsR in r and bitsG in r and bitsB in r:
		
		#tupla quantos bits tem em cada canal e a matriz rgba de 16 bits
		rgba_eq = [[bitsR, bitsG, bitsB], np.zeros(rgba_array.shape).astype(np.uint16)]
		
		rgba_eq[1][:,:,0] = (rgba_array[:,:,0]/255)*(2**bitsR-1)
		rgba_eq[1][:,:,1] = (rgba_array[:,:,1]/255)*(2**bitsG-1)
		rgba_eq[1][:,:,2] = (rgba_array[:,:,2]/255)*(2**bitsB-1)
		rgba_eq[1][:,:,3] = rgba_array[:,:,3]
		
		return rgba_eq
		
	else:
		print("\ntamanho dos canais esta fora do intervalo [1,16] bits!")


def binarizador_tc(tc_array, limiar):

	if limiar >=0 and limiar<=255:
		array_binario = np.zeros(tc_array.shape).astype(np.uint8)
		
		#array_binario = 255*(tc_array>limiar)#if array_binario[:,:] >=limiar else 0
		
		'''shape = tc_array.shape
		for i in range(shape[0]):
			for j in range(shape[1]):'''
		array_binario[:,:] = 255*(tc_array[:,:]>limiar)# if tc_array[i,j]>limiar else 0
		
		print(array_binario)
		return array_binario
		
	else:
		print("\nvalor invalido de limiar!")
		
def binarizador_rgb(rgba_array, limiarR, limiarG, limiarB):

	if limiarR >=0 and limiarR<=255  and limiarG >=0 and limiarG<=255 and limiarB >=0 and limiarB<=255:
		
		array_binario = np.zeros(rgba_array.shape).astype(np.uint8)

		shape = rgba_array.shape
		'''for i in range(shape[0]):
			for j in range(shape[1]):'''
		array_binario[:, :, 0] = 255*(rgba_array[:, :, 0]>limiarR)# if rgba_array[:, :, 0]>limiarR else 0
		array_binario[:, :, 1] = 255*(rgba_array[:, :, 1]>limiarG)# if rgba_array[:, :, 1]>limiarG else 0
		array_binario[:, :, 2] = 255*(rgba_array[:, :, 2]>limiarB)# if rgba_array[:, :, 2]>limiarB else 0
		array_binario[:, :, 3] = rgba_array[:, :, 3]
		
		return array_binario
		
	else:
		print("\nvalor invalido de limiar!")

#recebe uma imagem em tons de cinza
def otsu_tc(img_tc):
	 hist = np.array(img_tc.histogram())
	 
	 n = img_tc.size[0]*img_tc.size[1]
	 
	 vmax = 0
	 limiar = 0
	 
	 wb = 0
	 sumb = 0
	 sumt = sum(t*hist[t] for t in range(256))
	 
	 for i in range(256):
		 
		 wb += hist[i]
		 wf = n - wb
		 
		 sumb += i*hist[i]
		 sumf = sumt - sumb
		 
		 mb = sumb
		 if wb>0:
			 mb = mb/wb
			 
		 mf = sumf
		 if wf>0:
	          mf = mf/wf
		 
		 
		 var = wb*wf*((mb-mf)**2)
		 
		 if var>=vmax:
			 vmax = var
			 limiar = i
		 
	 return limiar
	
def otsu_rgb(img_rgba):
	hist = np.array(img_rgba.histogram())
	histr = hist[0:256]
	histg = hist[256:512]
	histb = hist[512:768]
	hist = [histr, histg, histb]
	
	n = img_rgba.size[0]*img_rgba.size[1]
	limiar = [0,0,0]
	
	#para r g b
	for j in range(3):
	
		vmax = 0	
		 
		wb = 0
		sumb = 0
		sumt = sum(t*hist[j][t] for t in range(256))
		 
		for i in range(256):
			 
			wb += hist[j][i]
			wf = n - wb
			 
			sumb += i*hist[j][i]
			sumf = sumt - sumb
			 
			mb = sumb
			if wb>0:
				mb = mb/wb
				 
			mf = sumf
			if wf>0:
				 mf = mf/wf
			 
			 
			var = wb*wf*((mb-mf)**2)
			 
			if var>=vmax:
				vmax = var
				limiar[j] = i
		 
	return limiar
	
def MSE(img1, img2):
    l1, a1 = img1.size  # largura e altura img1
    l2, a2 = img2.size  # largura e altura img1

    img1_rgb = np.array(img1)
    img2_rgb = np.array(img2)
    
    erro = 0

    ''' Ver a necessidade de normalizar o valor da diferença. Sem normalizar, o erro fica estranho '''
    if l1 == l2 and a1 == a2 and type(img1) == type(img2):
        erro = ( ((img1_rgb[:, :, :-1] - img2_rgb[:, :, :-1])/255.0) ** 2 ).sum()
    else:
        print("imagens de tipo ou tamanho diferente!")

    return erro / (3 * l1 * a1)


def histograma(img):
    
    L = 256
    h = img.histogram()    
    tam = len(h) // L    
    colors = ['k'] if tam == 1 else ['r', 'g', 'b']

    for i in range(tam):
        plt.subplot(tam, 1, i+1)
        plt.xlim(0, 256)
        plt.bar(range(L), h[i*L:(i+1)*L], color = colors[i], edgecolor = colors[i])
     
    return plt
  
def equalizacao_histograma(img):
	    
    L=256
    l, a = img.size    
    h = img.histogram()    
    img_rgb = np.array(img)    
    tam = len(h) // L    
    indice = []
    
    for j in range(tam):
        h_n = h[j*L:(j+1)*L]
        indice.append([])
        soma = 0
        for i in range(len(h_n)):
            soma += h_n[i]
            indice[-1].append( round ( ( (L - 1) / (l*a) ) * soma )  )
      
    indice = np.array(indice).astype(np.uint8)
    
    if tam == 3:
        for i in range(tam): 
            img_rgb[:, :, i] = indice[i, img_rgb[:, :, i]]
            img = pil.fromarray(img_rgb, 'RGB')
    else:
        img_rgb[:, :] = indice[0, img_rgb[:, :]]
        img = pil.fromarray(img_rgb, 'L')
    
    
    return img, histograma(img)

def correcaoGamma(array, c, gamma):
    array = ((c * (array/255)**gamma)*255).astype(np.uint8)
    return (array)

#quantizador do pil
'''#teste equalizador do pil
img = pil.open("TESTE.png")
rgba = np.array(img)
#print(rgba)
img.show()
#print(type(img))
nbits = 5
img = img.quantize(2**nbits, 0)
rgbanbits = np.array(img)
#print(rgbanbits)
img.show()
#print(type(img))'''



#quantizador uniforme implementado
'''img = pil.open("TESTE.png")
img.show()

img = img.convert('RGBA')
rgba_array = np.array(img)
#print("\nrgba_array:\n\n", rgba_array)

rgba_eq = quantizadorUniforme(rgba_array, 2, 2, 2)#arrayrgba quantizado
#print("\nrgba_eq:\n\n",rgba_eq[1])

rgba_eq = conversorImgQuantizada(rgba_eq)#array quantizado convertido para 8bits
#print("\nrgba_eq:\n\n",rgba_eq)


img = pil.fromarray(rgba_eq, 'RGBA')
img.show()'''





#teste binarizador limiarização
'''tc = rgba_p_tc(img_p_rgba("otsu.jpg"), 2)
img = pil.fromarray(tc, 'L')
img.show()

limiar = otsu_tc(img)
print("limiar: ", limiar)

tc = binarizador_tc(tc, limiar)
img = pil.fromarray(tc, 'L')
img.show()'''




#teste binarizador rgb
'''nome = "bin.png"
img = pil.open(nome).convert('RGBA')
img.show()
rgba_array = img_p_rgba(nome)

#limiar = [127, 127, 127]
limiar = otsu_rgb(img)

rgba_array = binarizador_rgb(rgba_array, limiar[0], limiar[1], limiar[2])
img = pil.fromarray(rgba_array, 'RGBA')
img.show()'''



#binarizador
'''
#print("tc antes de binarizar: \n\n", tc)
tc = binarizador_tc(tc, 150)
#print("tc depois de binarizar: \n\n", tc)
img = pil.fromarray(tc, 'L')
img.show()'''
