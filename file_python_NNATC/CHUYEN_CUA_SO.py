import speech_recognition as sr
import pyautogui 

def run_chuyen_cua_so():
    def chuyen_den_cua_so(text):
        vt=text.find("cửa sổ số")
        if vt!=-1:
            vtri=vt+10
            so=0
            while text[vtri]>="0" and text[vtri]<="9":
                so=so*10+int(text[vtri])
                vtri+=1
            for i in range(1,so):
                pyautogui.hotkey('right')
        pyautogui.hotkey('enter')
                    
    def chuyen_cua_so():
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
                    if 'cửa sổ số' in text:
                        chuyen_den_cua_so(text)
                        pyautogui.keyUp('alt')
                        break
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
    chuyen_cua_so()