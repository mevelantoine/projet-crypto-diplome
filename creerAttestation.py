import tkinter as tk
import qrcode as qr
import re
import time
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from functools import partial
from tkinter.filedialog import askopenfilename
from tkinter.constants import CENTER

##FONCTIONS
#Fonctions de stéganographie

def vers_8bit(c):
	chaine_binaire = bin(ord(c))[2:]
	return "0"*(8-len(chaine_binaire))+chaine_binaire

def modifier_pixel(pixel, bit):
	# on modifie que la composante rouge
	r_val = pixel[0]
	rep_binaire = bin(r_val)[2:]
	rep_bin_mod = rep_binaire[:-1] + bit
	r_val = int(rep_bin_mod, 2)
	return tuple([r_val] + list(pixel[1:]))

def recuperer_bit_pfaible(pixel):
	r_val = pixel[0]
	return bin(r_val)[-1]

def cacher(image,message):
	dimX,dimY = image.size
	im = image.load()
	message_binaire = ''.join([vers_8bit(c) for c in message])
	posx_pixel = 0
	posy_pixel = 0
	for bit in message_binaire:
		im[posx_pixel,posy_pixel] = modifier_pixel(im[posx_pixel,posy_pixel],bit)
		posx_pixel += 1
		if (posx_pixel == dimX):
			posx_pixel = 0
			posy_pixel += 1
		assert(posy_pixel < dimY)

def recuperer(image,taille):
	message = ""
	dimX,dimY = image.size
	im = image.load()
	posx_pixel = 0
	posy_pixel = 0
	for rang_car in range(0,taille):
		rep_binaire = ""
		for rang_bit in range(0,8):
			rep_binaire += recuperer_bit_pfaible(im[posx_pixel,posy_pixel])
			posx_pixel +=1
			if (posx_pixel == dimX):
				posx_pixel = 0
				posy_pixel += 1
		message += chr(int(rep_binaire, 2))
	return message


## Fonctions d'OTP
def validate(window,root,otp):
    if (True):
         window.destroy()
         root.lift()
    else:
        pass

#Fonctions de génération d'image
def genererDiplome(nom,prenom,formation):
    attestation = Image.open("assets/template.png")
    draw = ImageDraw.Draw(attestation)
    
    #Ajout du texte
    draw.text((500, 430),"CERTIFICAT DÉLIVRÉ",(0,0,0),font=ImageFont.truetype("assets/algerian-condensed-std-regular.otf", 110))
    draw.text((860, 560),"À",(0,0,0),font=ImageFont.truetype("assets/algerian-condensed-std-regular.otf", 110))
    draw.text((550, 680),nom.get().upper()+" "+prenom.get().upper(),(0,0,0),font=ImageFont.truetype("assets/algerian-condensed-std-regular.otf", 110))

    #Stéganographie
    timestamp = str(int(time.time()))
    stegano = nom.get()+prenom.get()+formation+timestamp
    while (len(stegano) < 64):
        stegano += "-"
    cacher(attestation,stegano)

    #Ajout du QRCode
    att_l, att_h = attestation.size
    #TODO : Signer avant de mettre dans le QRCODE
    imgQR = qr.make(nom.get()+prenom.get()+formation)
    offset = (1380,880)
    attestation.paste(imgQR,offset)


    attestation.save("diplomes/"+nom.get()+prenom.get()+'Diplome'+formation+'.jpg')

#Fonctions d'affichage
def checkMail():
    if re.match("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",mail.get()):
        inputMail.config(background="#3AC9A4")
    else:
        inputMail.config(background="#FF5252")
    if isOpen: #On ne lance pas d'alarme si la fenêtre est fermée
        root.after(100,checkMail)

def fermetureFenetre():
    isOpen=False
    root.destroy()

def choosefile(filename):
    tk.Tk().withdraw() 
    filename = askopenfilename()
    textNomFichier.configure(text=filename)


##MAIN
#Fenêtre racine
root = tk.Tk()
root.title("Application de création de diplôme")
root.geometry("1600x900+0+0")
isOpen=True

frameCreation = tk.LabelFrame(relief=tk.RIDGE,borderwidth=5,padx=10,pady=10,text="Création de diplôme")
frameDecodage = tk.LabelFrame(relief=tk.RIDGE,borderwidth=5,pady=10,text="Vérification de diplôme")

##Fenêtre de demande d'OTP initiale
otpWindow= tk.Toplevel(root)
otpWindow.geometry("250x100+0+0")
otpWindow.attributes('-topmost', True)

otp = tk.IntVar()
textOTP = tk.Label(otpWindow,text="Entrez votre OTP")
inputOTP = tk.Entry(otpWindow,textvariable=otp)
buttonOTP = tk.Button(otpWindow,text="Valider",command=partial(validate,otpWindow,root,otp))

textOTP.place(relx=0.5, rely=0.1, anchor=CENTER)
inputOTP.place(relx=0.5, rely=0.25, anchor=CENTER)
buttonOTP.place(relx=0.5, rely=0.5,anchor=CENTER)
otpWindow.resizable(False, False) 
otpWindow.grab_set()

##Elements de la fenêtre racine
nom = tk.StringVar()
textNom=tk.Label(frameCreation,text="Nom :")
inputNom = tk.Entry(frameCreation,textvariable=nom)
 
prenom = tk.StringVar()
textPrenom=tk.Label(frameCreation,text="Prénom :")
inputPrenom = tk.Entry(frameCreation,textvariable=prenom)

#formation = tk.StringVar()
optionsFormations=['ING1-GI', 'ING1-GM',"ING2-GSI", "ING2-SIE","ING3-CS","ING3-INEM","ING3-VISUAL"]
textFormations = tk.Label(frameCreation,text="Formation : ")
#dropFormations = tk.OptionMenu(frameCreation, formation, *optionsFormations)
listbox = tk.Listbox(frameCreation)
listbox.insert(tk.END, *optionsFormations)
formation = listbox.get(tk.ACTIVE)

mail = tk.StringVar()
textMail = tk.Label(frameCreation,text="Adresse e-mail :",pady=30)
inputMail = tk.Entry(frameCreation,textvariable=mail)

buttonValider = tk.Button(frameCreation,text="Valider",command=partial(genererDiplome,nom,prenom,formation))

nomFichier = ""
textChoisir = tk.Label(frameDecodage,text="Choisissez un diplôme à vérifier")
buttonChoisir = tk.Button(frameDecodage,text="Choisir un fichier",command=partial(choosefile,nomFichier))
textNomFichier = tk.Label(frameDecodage)


textNom.grid(row=0,column=0)
inputNom.grid(row=0,column=1)
textPrenom.grid(row=1,column=0)
inputPrenom.grid(row=1,column=1)
textFormations.grid(row=2,column=0)
listbox.grid(row=2,column=1)
textMail.grid(row=3,column=0)
inputMail.grid(row=3,column=1)

buttonValider.grid(row=10,column=0)

textChoisir.grid(row=11,column=0)
buttonChoisir.grid(row=12,column=0)
textNomFichier.grid(row=13,column=0)

frameCreation.grid(row=0,column=0,sticky="w")
frameDecodage.grid(row=1,column=0,sticky="w")

root.protocol("WM_DELETE_WINDOW", fermetureFenetre)
checkMail()
root.mainloop()

"""
print("Entrez votre OTP : ")
otpEcole = input()

if (True): #Ajouter l'application d'OTP
    print("Accès accordé\n\nVeuillez entrer un prénom :")
    prenom = input()
    print("Veuillez entrer un nom : ")
    nom = input()
    print("Veuillez entrer la formation : ")
    formation = input()
    print("Attestation pour",prenom,nom,",", formation)
    print("Entrez l'e-mail de",prenom,nom,":")
    email=input()
    print("Veuillez confirmer votre identité d'administrateur :")
    otpAdmin=input()

    attestation = Image.open("test.png")
    draw = ImageDraw.Draw(attestation)
    draw.text((500, 430),"CERTIFICAT DÉLIVRÉ",(0,0,0),font=ImageFont.truetype("algerian-condensed-std-regular.otf", 110))
    draw.text((860, 560),"À",(0,0,0),font=ImageFont.truetype("algerian-condensed-std-regular.otf", 110))
    draw.text((550, 680),"VIKEN TOPSAKAL",(0,0,0),font=ImageFont.truetype("algerian-condensed-std-regular.otf", 110))
    attestation.save('sample-out.jpg')


else:
    print("Accès refusé")

"""