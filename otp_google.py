import hmac, base64, struct, hashlib, random


def get_hotp_token(secret, intervals_no):
    key = base64.b32decode(secret, True)
    msg = struct.pack(">Q", intervals_no)
    h = hmac.new(key, msg, hashlib.sha1).digest()
    o = o = h[19] & 15
    h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
    return h

def check_otp(otp):
    test_otp = input("Entrez votre OTP : ")
    if test_otp == str(otp):
        print("OTP correct")
    else:
        print("Erreur")

secret = ''.join(random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(16))
otp = get_hotp_token(secret, intervals_no=1)
f = open("otp.txt","w")
f.write(str(otp))
f.close()

print ("Votre OTP est "+ str(otp))
#check_otp(otp)