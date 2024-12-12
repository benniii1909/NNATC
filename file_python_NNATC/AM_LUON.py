import pyautogui 

def tang_am_luong(text):
    vt=text.find("tăng âm lượng lên")
    if vt!=-1:
        
        vtri=vt+18
        so=0
        while text[vtri]>="0" and text[vtri]<="9":
            so=so*10+int(text[vtri])
            vtri+=1
        for i in range(0,so//2):
            pyautogui.hotkey('volumeup')
def giam_am_luong(text):
    vt=text.find("giảm âm lượng xuống")
    if vt!=-1:
        vtri=vt+20
        so=0
        while text[vtri]>="0" and text[vtri]<="9":
            so=so*10+int(text[vtri])
            vtri+=1
        for i in range(0,so//2):
            pyautogui.hotkey('volumedown')
