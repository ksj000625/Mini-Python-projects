import pyqrcode

def qrCode() :
    q = pyqrcode.create(input())
    q.png('qrcode.png', scale = 6)
    print("QR generated")

if __name__=='__main__' :
    qrCode()