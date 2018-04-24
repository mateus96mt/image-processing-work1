import codigo
import argparse
import numpy as np
import PIL.Image as pil
import matplotlib.pyplot as plt

def img_p_rgba(img_entrada):
    if img_entrada!=None:
        array_rgba = codigo.img_p_rgba(img_entrada)
        print("\n\narray_rgba:\n", array_rgba)
    else:
        print("faltando argumento -i [img_entrada]")

def img_p_tc(img_entrada, o, s):
    
    if img_entrada!=None:
        
        if o==None: #conversao para tons de cinza usando media como padrao
            o = 2
        
        o = int(o)
        
        if (o in range(1,4))==True:
                
            array_rgba = codigo.img_p_rgba(img_entrada)
            print("\n\narray_rgba:\n", array_rgba)
            
            array_tc = codigo.rgba_p_tc(array_rgba, o)
            print("\n\narray_tc:\n", array_tc)

            if s != None:
                img = pil.fromarray(array_tc, 'L')
                img.save(str(s))
        else:
            print("\nargumento -o inválido!")
    else:
        print("faltando argumento -i [img_entrada]")
        
def tc_p_rgba(img_entrada, s):
    
    if img_entrada != None:
        
        array_tc = np.array(pil.open(img_entrada).convert('L'))
        print("\n\narray_tc:\n", array_tc)
        
        array_rgba = codigo.tc_p_rgba(array_tc)
        print("\n\narray_rgba:\n", array_rgba)
        
        img = pil.fromarray(array_rgba, 'RGBA')
        img.show()
        
        if s != None:
            img.save(str(s))
    else:
        print("faltando argumento -i [img_entrada]")

def binarizadorrgb(img_entrada, o, s):
    
    if img_entrada != None:
        img = pil.open(img_entrada).convert('RGBA')
        img.show()
        
        array_rgba = np.array(img)

        limiar = [0, 0, 0]
        
        if o==None:
            o='otsu'        
        
        if o=='otsu':
            limiar = codigo.otsu_rgb(img)
        else:
            limiar = o[1:-1].split(',')
        
        limiar = np.array(limiar).astype(int)
        print("limiar: ", limiar)
        
        array_bin = codigo.binarizador_rgb(array_rgba, limiar[0], limiar[1], limiar[2])
        
        img = pil.fromarray(array_bin, 'RGBA')
        img.show()
        
        if s!=None:
            img.save(s)
            
    else:
        print("faltando argumento -i [img_entrada]")

def binarizadortc(img_entrada, o, s):
    
    if img_entrada != None:
        img = pil.open(img_entrada).convert('L')
        img.show()
        
        array_tc = np.array(img)

        limiar = 0
        
        if o==None:
            o='otsu'        
        
        if o=='otsu':
            limiar = codigo.otsu_tc(img)
        else:
            limiar = int(o)
        
        print("limiar: ", limiar)
        
        array_bin = codigo.binarizador_tc(array_tc, limiar)
        
        img = pil.fromarray(array_bin, 'L')
        img.show()
        
        if s!=None:
            img.save(s)
            
    else:
        print("faltando argumento -i [img_entrada]")

def quantizadorUni(img_entrada, o, s):
    if img_entrada != None:
        
        img = pil.open(img_entrada)
        img.show()
        
        bits = [8, 8, 8]
        
        if o==None:
            o = [8, 8, 8]
        else:
            bits = o[1:-1].split(',')
        
        bits = np.array(bits).astype(int)
        
        array_rgba = np.array(pil.open(img_entrada).convert('RGBA'))
        
        rgba_quant = codigo.quantizadorUniforme(array_rgba, bits[0], bits[1], bits[2])
        
        #print(rgba_quant[1])
        
        rgba = codigo.conversorImgQuantizada(rgba_quant)
        img = pil.fromarray(rgba, 'RGBA')
        img.show()
        
        if s!=None:
            img.save(s)
        
    else:
        print("faltando argumento -i [img_entrada]")

def MSE(img_entrada1, img_entrada2):
    
    '''img_entrada1 = pil.open(img_entrada1).convert('RGBA')
    img_entrada2 = pil.open(img_entrada2).convert('RGBA')'''
    
    
    if img_entrada1 != None and img_entrada2 != None:
    
        img_entrada1_rgba = codigo.img_p_rgba(img_entrada1)
        img_entrada2_rgba = codigo.img_p_rgba(img_entrada2)
    
        shape1 = img_entrada1_rgba.shape
        shape2 = img_entrada2_rgba.shape
        
    
        l1, a1 = shape1[0], shape1[1]  # largura e altura img_entrada1
        l2, a2 = shape2[0], shape2[1]  # largura e altura img_entrada2
        
        erro = 0

        if l1 == l2 and a1 == a2 and type(img_entrada1) == type(img_entrada2):
            erro = ( ((img_entrada1_rgba[:, :, :-1]/255.0 - img_entrada2_rgba[:, :, :-1]/255.0)) ** 2 ).sum()
        else:
            print("imagens de tipo ou tamanho diferente!")

        erro =  erro / (3 * l1 * a1)
    
        print("\nMSE: ", erro)
    
    else:
        print("faltando argumento -i1 [img_entrada1] ou -i2 [img_entrada2]")

def SNR(img_entrada1, img_entrada2):
    
    img_entrada1 = pil.open(img_entrada1).convert('RGBA')
    img_entrada2 = pil.open(img_entrada2).convert('RGBA')
    
    img1_rgb = np.array(img_entrada1)
    
    l, a = img_entrada1.size  # largura e altura img1
    
    erro = ((img1_rgb[:,:,:-1]/255)**2).sum() / (3 * l * a) 
        
    divisor = codigo.MSE(img_entrada1, img_entrada2)
        
    erro = erro/divisor if divisor>0 else 0

    print("SNR: ", erro)

def histograma(img_entrada, o):
    
    if img_entrada != None:
        
        if o==None:
            o = 'RGB'
        if o!='RGB'and o!='L':
	        print("\nargumento -o invalido!")
        else:
            img = pil.open(img_entrada).convert(str(o))
            img.show()
            plt1 = codigo.histograma(img)
            plt1.show(block=False)
            plt.draw()
            plt.pause(0.001)
            input("Press [enter] to continue.")
    else:
        print("faltando argumento -i [img_entrada]")

def eq_histograma(img_entrada, o, s):
    
    if img_entrada != None:
        
        if o==None:
            o = 'RGB'
        if o!='RGB'and o!='L':
            print("\nargumento -o invalido!")
        else:
            
            img = pil.open(img_entrada).convert(str(o))
            
            plt1 = []
            
            codigo.plt.figure('Imagem Original')
            codigo.plt.suptitle('Histograma Imagem Original')
            plt1.append(codigo.histograma(img))
            
            codigo.plt.figure('Imagem Modificada')
            img2, plt2 = codigo.equalizacao_histograma(img)
                        

            img.show(title='Original', command=True)
            img2.show(title='Novo')
            
            plt1.append(plt2)
        
            for i in range(2):
                plt1[i].show(block=False)            
            
            if s!=None:
                img2.save(s)
            
            plt.draw()
            plt.pause(0.001)
            input("Press [enter] to continue.")
    else:
        print("faltando argumento -i [img_entrada]")

def correcao_gamma(img_entrada, o, s):
    
    if img_entrada != None:
        
        if o==None:
            print("faltando argumento -o")
        else:
            vet = o[1:-1].split(',')
            tipo = vet[0]
            try:
                vet = np.array(vet[1:]).astype(float)
            except:
                print("argumento -o invalido, valor correto:  -o [RGB <ou> L,c,gamma]")
                return 0
            
            if tipo!='RGB' and tipo!='L':
                print("argumento -o invalido, valor correto:  -o [RGB <ou> L,c,gamma]")
            else:
                
                img_entrada = pil.open(img_entrada).convert(tipo)
                img_entrada.show()                
                
                array = np.array(img_entrada)
                
                ''' vai ficar printando essas merdas mesmo?'''
                print("antes da correcao: ", array)
                
                array = codigo.correcaoGamma(array, vet[0], vet[1])
                
                print("depois da correcao: ", array)
                
                img = pil.fromarray(array, tipo)
                img.show()
                
                if s!=None:
                    img.save(s)
        
    else:
        print("faltando argumento -i [img_entrada]")
    

parser = argparse.ArgumentParser()

parser.add_argument("funcao", help="FUNCIONALIDADE A SER EXECUTADA:\timg_para_rgba\timg_para_tc\ttc_para_rgba\tmse\tsnr\tcorrecao_gamma\teq_histograma\tbinrgb\tbintc\tquantizador\thistograma")

parser.add_argument("-i", "--img_entrada", help="imagem de entrada, para funcoes que recebem somente uma imagem como parametro de entrada")

parser.add_argument("-i1", "--img_entrada1", help="imagem1 de entrada, para funcoes que recebem mais de uma imagem como parametro de entrada")

parser.add_argument("-i2", "--img_entrada2", help="imagem2 de entrada, para funcoes que recebem mais de uma imagem como parametro de entrada")

parser.add_argument("-s", "--saida", help="salvar imagem resultado da funcao em arquivo de saida, usado em funcoes que modificam a imagem de entrada")

parser.add_argument("-o", "--opcao", help="parametro de opcao da funcao, usado em funcoes que o usuario pode escolher opcoes")

args = parser.parse_args()


if args.funcao == 'img_para_rgba':
    img_p_rgba(args.img_entrada)
    
if args.funcao == 'img_para_tc':
    img_p_tc(args.img_entrada, args.opcao, args.saida)
    
if args.funcao == 'tc_para_rgba':
    tc_p_rgba(args.img_entrada, args.saida)

if args.funcao == 'binrgb':
    binarizadorrgb(args.img_entrada, args.opcao, args.saida)

if args.funcao == 'bintc':
    binarizadortc(args.img_entrada, args.opcao, args.saida)

if args.funcao == 'quantizador':
    quantizadorUni(args.img_entrada, args.opcao, args.saida)
    
if args.funcao == 'mse':
    MSE(args.img_entrada1, args.img_entrada2)

if args.funcao == 'snr':
    SNR(args.img_entrada1, args.img_entrada2)

if args.funcao == 'histograma':
    histograma(args.img_entrada, args.opcao)

if args.funcao == 'eq_histograma':
    eq_histograma(args.img_entrada, args.opcao, args.saida)

if args.funcao == 'correcao_gamma':
    correcao_gamma(args.img_entrada, args.opcao, args.saida)
