import speech_recognition as sr
import pyautogui 
import pyperclip
from gtts import gTTS
import playsound
import os

def giong_noi(textt):
    tts = gTTS(text=textt, lang='vi')
    filename='giong noi.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)
def nhan_dien_giong_noi():
    recognizer = sr.Recognizer()
    while True:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio=recognizer.listen(source)
            try:
                text1=recognizer.recognize_google(audio, language='vi-VN')#nhận giọng nói tiếng Việt
                text = text1.lower()#chuyển tất cả về viết thường
                print(text)
                text+=" "
                pyperclip.copy(text)
                if 'tắt bàn phím' in text:
                    giong_noi("đang tắt bàn phím bằng giọng nói")
                    print("da tat")
                    break
                pyautogui.hotkey('ctrl', 'v')
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                pass