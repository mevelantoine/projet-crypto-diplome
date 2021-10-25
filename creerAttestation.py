import tkinter as tk
import qrcode as qr
import re
import requests
import subprocess
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from Crypto.Hash import SHA512
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from functools import partial
from tkinter.filedialog import askopenfilename
from tkinter.constants import CENTER
from tkinter import messagebox

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
    #r = requests.get('http://127.0.0.1/verify?otp='+str(otp.get()))
    #if (r.status_code == 200):
    if (True):
         window.destroy()
         root.lift()
    else:
        tk.messagebox.showerror(title="Erreur", message="OTP non valide")

#Fonctions de génération d'image
def genererDiplome(nom,prenom,formation):
    attestation = Image.open("assets/template.png")
    draw = ImageDraw.Draw(attestation)

    #Ajout du texte
    draw.text((500, 430),"CERTIFICAT DÉLIVRÉ",(0,0,0),font=ImageFont.truetype("assets/algerian-condensed-std-regular.otf", 110))
    draw.text((860, 560),"À",(0,0,0),font=ImageFont.truetype("assets/algerian-condensed-std-regular.otf", 110))
    draw.text((550, 680),nom.get().upper()+" "+prenom.get().upper(),(0,0,0),font=ImageFont.truetype("assets/algerian-condensed-std-regular.otf", 110))
    draw.text((740, 820),formation.get().upper(),(0,0,0), font=ImageFont.truetype("assets/algerian-condensed-std-regular.otf", 110))
    
    processQuery = subprocess.Popen(['openssl','ts','-query','-data','assets/template.png','-no_nonce','-sha512','-cert', '-out', 'file.tsq'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    processResponse = subprocess.Popen(['curl', '-H', '"Content-Type: application/timestamp-query"', '--data-binary', "'@file.tsq'",'https://freetsa.org/tsr', '-o' 'file.tsr' ],stdout = subprocess.PIPE, stderr = subprocess.PIPE)
        
    strQuery = open("file.tsq","rb").read()
    strResponse = open("file.tsr","rb").read()
    #Stéganographie : nom prenom formation timestamp

    bloc = nom.get()+" "+prenom.get()+formation.get()
    while (len(bloc) < 64):
        bloc += "-"
    
    stegano =  str(strQuery) + "||" + str(strResponse)
    print(len(strQuery),len(strResponse))
    cacher(attestation,stegano)

    #Ajout du QRCode : signature de nom prenom formation
    att_l, att_h = attestation.size
    info = nom.get()+prenom.get()+formation.get()
    infoEncoded = info.encode()

    key_pub = RSA.importKey(open("certificates/newcert.pem", "r").read(), passphrase="test")

    key_priv = RSA.importKey(open("certificates/newkey.pem", "r").read(), passphrase="test")

    h = SHA512.new(infoEncoded)
    infoSigne = PKCS1_v1_5.new(key_priv).sign(h)

    imgQR = qr.make(infoSigne, box_size=3, border=2)
    offset = (1415,930)
    attestation.paste(imgQR,offset)
    attestation.save("diplomes/"+nom.get()+prenom.get()+'Diplome'+formation.get()+'.png')

    attestation.save("diplomes/"+nom.get()+prenom.get()+'Diplome'+formation.get()+'.png')

def verifierDiplome():
    global emplacementFichier
    print(emplacementFichier)
    fichier = Image.open(open(emplacementFichier, 'rb'))
    print(recuperer(fichier,10000))

#Fonctions d'affichage
def checkMail():
    if re.match("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",mail.get()):
        inputMail.config(background="#3AC9A4")
    else:
        inputMail.config(background="#FF5252")

def fermetureFenetre():
    isOpen=False
    root.quit()

def choosefile():
    global emplacementFichier 
    tk.Tk().withdraw()
    emplacementFichier = askopenfilename()
    textNomFichier.configure(text=emplacementFichier)
    print(emplacementFichier)

##MAIN

emplacementFichier=""

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
otpWindow.protocol("WM_DELETE_WINDOW", fermetureFenetre)
otpWindow.resizable(False, False)
otpWindow.grab_set()

##Elements de la fenêtre racine
nom = tk.StringVar()
textNom=tk.Label(frameCreation,text="Nom :")
inputNom = tk.Entry(frameCreation,textvariable=nom)

prenom = tk.StringVar()
textPrenom=tk.Label(frameCreation,text="Prénom :")
inputPrenom = tk.Entry(frameCreation,textvariable=prenom)

formation = tk.StringVar()
def getElement(event):
  selection = event.widget.curselection()
  index = selection[0]
  value = event.widget.get(index)
  formation.set(value)
  print(index,' -> ',value)

textFormations = tk.Label(frameCreation,text="Formation : ")
#dropFormations = tk.OptionMenu(frameCreation, formation, *optionsFormations)
listeOptions = tk.StringVar()
listeOptions.set(('ING1-GI', 'ING1-GM',"ING2-GSI", "ING2-SIE","ING3-CS","ING3-INEM","ING3-VISUAL"))
listbox = tk.Listbox(frameCreation, listvariable=listeOptions)
listbox.bind("<<ListboxSelect>>", getElement)

mail = tk.StringVar()
textMail = tk.Label(frameCreation,text="Adresse e-mail :",pady=30)
inputMail = tk.Entry(frameCreation,textvariable=mail)

buttonValider = tk.Button(frameCreation,text="Valider",command=partial(genererDiplome,nom,prenom,formation))

nomFichier = ""
textChoisir = tk.Label(frameDecodage,text="Choisissez un diplôme à vérifier")
buttonChoisir = tk.Button(frameDecodage,text="Choisir un fichier",command=choosefile)
textNomFichier = tk.Label(frameDecodage)
buttonVerifier = tk.Button(frameDecodage,text="Valider",command=verifierDiplome)

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
buttonVerifier.grid(row=14,column=0)

frameCreation.grid(row=0,column=0,sticky="w")
frameDecodage.grid(row=1,column=0,sticky="w")

root.protocol("WM_DELETE_WINDOW", fermetureFenetre)
checkMail()
root.mainloop()