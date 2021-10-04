import tkinter as tk
#import qrcode as qr
import re
from tkinter.constants import CENTER
from typing import Text
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from functools import partial

def validate(window):
    if (True):
         window.destroy()
    else:
        pass

def genererDiplome(nom,prenom,formation):
    attestation = Image.open("test.png")
    draw = ImageDraw.Draw(attestation)
    draw.text((500, 430),"CERTIFICAT DÉLIVRÉ",(0,0,0),font=ImageFont.truetype("algerian-condensed-std-regular.otf", 110))
    draw.text((860, 560),"À",(0,0,0),font=ImageFont.truetype("algerian-condensed-std-regular.otf", 110))
    draw.text((550, 680),nom.get().upper()+" "+prenom.get().upper(),(0,0,0),font=ImageFont.truetype("algerian-condensed-std-regular.otf", 110))
    attestation.save(nom.get()+prenom.get()+'Diplome'+formation.get()+'.jpg')

def checkMail():
    if re.match("^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",mail.get()):
        inputMail.config(background="#3AC9A4")
    else:
        inputMail.config(background="#FF5252")
    root.after(100,checkMail)

# Regex check email : .*\@.*\.com

#Fenêtre racine
root = tk.Tk()
root.title("Application de création de diplôme")
root.geometry("1600x900+100+50")

##Fenêtre de demande d'OTP initiale
otpWindow= tk.Toplevel(root)
otpWindow.geometry("250x100+750+400")
otpWindow.attributes('-topmost', True)

otp = tk.IntVar()
textOTP = tk.Label(otpWindow,text="Entrez votre OTP")
inputOTP = tk.Entry(otpWindow,textvariable=otp)
buttonOTP = tk.Button(otpWindow,text="Valider",command=otpWindow.destroy)

textOTP.place(relx=0.5, rely=0.1, anchor=CENTER)
inputOTP.place(relx=0.5, rely=0.25, anchor=CENTER)
buttonOTP.place(relx=0.5, rely=0.5,anchor=CENTER)
otpWindow.resizable(False, False) 
otpWindow.grab_set()

##Elements de la fenêtre racine
nom = tk.StringVar()
textNom=tk.Label(root,text="Nom :")
inputNom = tk.Entry(root,textvariable=nom)
 
prenom = tk.StringVar()
textPrenom=tk.Label(root,text="Prénom :")
inputPrenom = tk.Entry(root,textvariable=prenom)

formation = tk.StringVar()
optionsFormations=['ING1 GI', 'ING1 GM',"ING2 GSI", "ING2 SIE","ING3 CS","ING3 INEM","ING3 VISUAL"]
textFormations = tk.Label(root,text="Formation : ")
dropFormations = tk.OptionMenu(root, formation, *optionsFormations)

mail = tk.StringVar()
textMail = tk.Label(root,text="Adresse e-mail :",pady=30)
inputMail = tk.Entry(root,textvariable=mail)

buttonValider = tk.Button(root,text="Valider",command=partial(genererDiplome,nom,prenom,formation))

textNom.grid(row=0,column=0)
inputNom.grid(row=0,column=1)
textPrenom.grid(row=1,column=0)
inputPrenom.grid(row=1,column=1)
textFormations.grid(row=2,column=0)
dropFormations.grid(row=2,column=1)
textMail.grid(row=3,column=0)
inputMail.grid(row=3,column=1)

buttonValider.grid(row=10,column=0)

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