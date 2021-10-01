import tkinter as tk
import qrcode as qr
import os
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw

os.chdir("H:\Cours\ING3\Cryptographie\projet-crypto-diplome")

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
    draw.text((0, 0),"AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",(0,0,0),font=ImageFont.truetype("sans-serif.ttf", 50))
    draw.line(((0,12),(500,13)))
    attestation.save('sample-out.jpg')


else:
    print("Accès refusé")