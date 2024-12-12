import cv2
import mediapipe as mp
import pyautogui
import threading
import time
import speech_recognition as sr
import subprocess
import os
from gtts import gTTS
import playsound
from CHUYEN_CUA_SO import*
from AM_LUON import *
import tkinter as tk

def giong_noi(textt):
    tts = gTTS(text=textt, lang='vi')
    filename='giong noi.mp3'
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)


from DONG_MO_UNG_DUNG import*
from CHUYEN_VAN_BAN_THANH_GIONG_NOI import *

pyautogui.FAILSAFE = False

diem_bat_dau_1x=(0,0)
diem_ket_thuc_1x=(0,0)

diem_bat_dau_2x=(0,0)
diem_ket_thuc_2x=(0,0)

diem_bat_dau_3x=(0,0)
diem_ket_thuc_3x=(0,0)

diem_bat_dau_4x=(0,0)
diem_ket_thuc_4x=(0,0)
        
start_1=(0,0)
end_1=(0,0)
        
start_2=(0,0)
end_2=(0,0)

start_3=(0,0)
end_3=(0,0)

start_4=(0,0)
end_4=(0,0)
text=""

def find_file_in_system(filename):
    for root, dirs, files in os.walk('/'):
        if filename in files:
            return os.path.join(root, filename)
    return None

def run_cuon_chuot_may_tinh():
    def thong_bao(textt):
        root = tk.Tk()
        root.overrideredirect(1)  # Loại bỏ thanh điều khiển

        # Tạo nhãn với văn bản dài

        label = tk.Label(root, text=textt, wraplength=200)
        label.pack()

        # Lấy kích thước màn hình
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Đặt vị trí của cửa sổ
        position_top = screen_height - root.winfo_reqheight()  # Chiều cao yêu cầu
        position_right = screen_width - root.winfo_reqwidth()  # Chiều rộng yêu cầu


        root.geometry("+%d+%d" % (position_right, position_top))
        def close_window():
            root.destroy()

            # Đặt hẹn giờ để đóng cửa sổ
        root.after(3000, close_window)
        root.mainloop()

    def mini_recognize():
        global a
        global text
        def nhan_dien_chuc_nang(text):
            
            if 'mở chrome' in text:
                giong_noi("đang mở chrome")
                file_path = find_file_in_system("chrome.exe")
                if file_path is None:
                    giong_noi("không có chrome trên máy")
                subprocess.Popen([file_path])

            if 'mở zalo' in text:
                giong_noi("đang mở zalo")
                file_path = find_file_in_system("Zalo.exe")
                if file_path is None:
                    giong_noi("không có zalo trên máy")

            if 'đóng cửa sổ' in text:
                close_window()
            if 'chuyển cửa sổ' in text:
                pyautogui.keyDown("alt")
                pyautogui.hotkey("tab")
                pyautogui.hotkey("left")
                run_chuyen_cua_so()
            if 'ẩn cửa sổ' in text:
                minimize_window()
            if 'phóng to cửa sổ' in text:
                maximize_window()
            if 'mở file explorer' in text:
                giong_noi("đang mở file explorer")
                pyautogui.hotkey('win','e')
            if 'tắt máy tính' in text:
                giong_noi('sẽ tắt máy tính sau vài giây nữa')
                os.system('shutdown -s -t 1')
            if 'sao chép' in text:
                    giong_noi('đã sao chép')
                    pyautogui.hotkey('ctrl','c')
                    
            if 'dán' in text:
                    pyautogui.hotkey('ctrl','v')
            if 'xóa file' in text:
                    pyautogui.hotkey('delete')
            if 'xóa' in text and 'ký tự' in text:
                def xoa_ki_tu(text):
                    vt=text.find("xóa")
                    if vt!=-1:
                        vtri=vt+4
                        so=0
                        while text[vtri]>="0" and text[vtri]<="9":
                            so=so*10+int(text[vtri])
                            vtri+=1
                    for i in range (1,so):
                        pyautogui.hotkey('backspace')
                xoa_ki_tu(text)
        
        recognizer = sr.Recognizer()
        while True:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio=recognizer.listen(source)
                try:
                    text1=recognizer.recognize_google(audio, language='vi-VN')#nhận giọng nói tiếng Việt
                    text = text1.lower()#chuyển tất cả về viết thường
                    print(text)
                    text=text+" "#thêm kí tự cách để ko bị lỗi
                    if 'tắt cuộn chuột máy tính 'in text:
                        giong_noi("đang tắt cuộn chuột máy tính")
                        break
                    if "mở bàn phím" in text:
                        giong_noi("đang mở bàn phím bằng giọng nói")
                        nhan_dien_giong_noi()
                        break
                    if "tăng âm lượng lên" in text:
                        tang_am_luong(text)
                    if "giảm âm lượng xuống" in text:
                        giam_am_luong(text)
                    if text!=" ":
                        thread_thong_bao=threading.Thread(target=thong_bao(text))
                        thread_thong_bao.start()
                    nhan_dien_chuc_nang(text)
                    
                except sr.UnknownValueError:
                    pass
                except sr.RequestError:
                    pass
    thread_giong_noi = threading.Thread(target=mini_recognize)
    thread_giong_noi.start()

    def chuot_may_tinh(b):
        global a
        
        mp_khuon_mat_mesh = mp.solutions.face_mesh
        khuon_mat_mesh = mp_khuon_mat_mesh.FaceMesh()

        
        
        def ve_hinh_vuong_cung_dinh(frame):
            chieu_dai, chieu_rong, _ = frame.shape
            diem_bat_dau = (chieu_rong//2 - 35, chieu_dai//2 - 35)
            diem_ket_thuc = (chieu_rong//2 + 35, chieu_dai//2 + 35)
            mau_sac = (0, 0, 255)
            do_day = 6

            global diem_bat_dau_1x
            global diem_ket_thuc_1x
            global diem_bat_dau_2x
            global diem_ket_thuc_2x
            global diem_bat_dau_3x
            global diem_ket_thuc_3x
            global diem_bat_dau_4x
            global diem_ket_thuc_4x
            global start_1
            global end_1
            global start_2
            global end_2
            global start_3
            global end_3
            global start_4
            global end_4

            diem_bat_dau_1x=(chieu_rong//2 - 35,chieu_dai//2 + 35)
            diem_ket_thuc_1x=(0, chieu_dai//2 - 35)

            diem_bat_dau_2x=(chieu_rong,chieu_dai//2 + 35)
            diem_ket_thuc_2x=(chieu_rong//2+35, chieu_dai//2 - 35)

            diem_bat_dau_3x=(chieu_rong//2 - 35,chieu_dai//2 - 35)
            diem_ket_thuc_3x=(chieu_rong//2 + 35,0)

            diem_bat_dau_4x=(chieu_rong//2 +35,chieu_dai//2 + 35)
            diem_ket_thuc_4x=(chieu_rong//2 - 35,chieu_dai)
            
            diem_bat_dau_1=(chieu_rong,chieu_dai//2 - 35)
            diem_ket_thuc_1=(0, chieu_dai//2 - 35)

            diem_bat_dau_2=(chieu_rong,chieu_dai//2 + 35)
            diem_ket_thuc_2=(0, chieu_dai//2 + 35)

            diem_bat_dau_3=(chieu_rong//2 + 35,chieu_dai)
            diem_ket_thuc_3=(chieu_rong//2 + 35,0)

            diem_bat_dau_4=(chieu_rong//2 - 35,chieu_dai)
            diem_ket_thuc_4=(chieu_rong//2 - 35,0)

            cv2.line(frame, diem_bat_dau_1, diem_ket_thuc_1, (0, 0, 255), thickness=6)

            cv2.line(frame, diem_bat_dau_2, diem_ket_thuc_2, (0, 0, 255), thickness=6)

            cv2.line(frame, diem_bat_dau_3, diem_ket_thuc_3, (0, 0, 255), thickness=6)

            cv2.line(frame, diem_bat_dau_4, diem_ket_thuc_4, (0, 0, 255), thickness=6)

            frame = cv2.rectangle(frame, diem_bat_dau, diem_ket_thuc, mau_sac, do_day)
            return frame

        def vung_mau(a,b,frame):
            

            # Vẽ một hình vuông màu đỏ đầy đủ trên bản sao
            cv2.rectangle(frame, a, b, (0, 255, 0), -1)

            # Tạo một hình ảnh mới bằng cách kết hợp frame gốc và bản sao với độ trong suốt
            alpha = 0.3
            frame = cv2.addWeighted(frame, alpha, frame, 1 - alpha, 0)

        screen_weight, screen_height = pyautogui.size()
        toa_do_di_chuyen=round(screen_height/768*3)

        
        
        def kiem_tra_huong(diem_mui, frame):
            global huong_ngang
            global huong_doc
            chieu_dai, chieu_rong, _ = frame.shape
            huong_doc = 'giua'
            huong_ngang = 'giua'
            
            if diem_mui[0] < chieu_rong//2 - 35:
                huong_ngang = 'trai'
            elif diem_mui[0] > chieu_rong//2 + 35:
                huong_ngang = 'phai'
            
            if diem_mui[1] < chieu_dai//2 - 35:
                huong_doc = 'tren'
            elif diem_mui[1] > chieu_dai//2 + 35:
                huong_doc = 'duoi'
            
            if huong_doc=="duoi" and huong_ngang=='giua':
                pyautogui.scroll(-10)
                
            if huong_doc=="tren" and huong_ngang=='giua':
                pyautogui.scroll(10)


            return huong_doc, huong_ngang
        
        def kiem_tra_huong_va_ve_o_mau(diem_mui, frame):
            global huong_ngang
            global huong_doc
            chieu_dai, chieu_rong, _ = frame.shape
            huong_doc = 'giua'
            huong_ngang = 'giua'
            
            if diem_mui[0] < chieu_rong//2 - 35:
                huong_ngang = 'trai'
            elif diem_mui[0] > chieu_rong//2 + 35:
                huong_ngang = 'phai'
            
            if diem_mui[1] < chieu_dai//2 - 35:
                huong_doc = 'tren'
            elif diem_mui[1] > chieu_dai//2 + 35:
                huong_doc = 'duoi'
            
            if huong_doc=="duoi" and huong_ngang=='giua':
                vung_mau(diem_bat_dau_4x,diem_ket_thuc_4x,frame)

            if huong_doc=="tren" and huong_ngang=='giua':
                vung_mau(diem_bat_dau_3x,diem_ket_thuc_3x,frame)

            if huong_doc=="giua" and huong_ngang=='phai':
                vung_mau(diem_bat_dau_2x,diem_ket_thuc_2x,frame)

            if huong_doc=="giua" and huong_ngang=='trai':
                vung_mau(diem_bat_dau_1x,diem_ket_thuc_1x,frame)
   
            return huong_doc, huong_ngang


        cap = cv2.VideoCapture(0)
        while True:

            _, anh = cap.read()
     
            anh = cv2.flip(anh, 1)
            rgb_frame = cv2.cvtColor(anh, cv2.COLOR_BGR2RGB)
            ket_qua = khuon_mat_mesh.process(anh)

            if ket_qua.multi_face_landmarks:
                for cac_diem_danh_dau_khuon_mat in ket_qua.multi_face_landmarks:
                    for id, lm in enumerate(cac_diem_danh_dau_khuon_mat.landmark):
                        chieu_cao_anh, chieu_rong_anh, so_kenh_mau = anh.shape
                        x,y = int(lm.x*chieu_rong_anh), int(lm.y*chieu_cao_anh)
                        
                        if id == 1:
                            diem_mui = (x,y)
                            cv2.circle(anh,diem_mui ,10,(0, 0, 255) ,-1)

                    thread_kiem_tra_huong = threading.Thread(target=kiem_tra_huong, args=(diem_mui, anh))
                    thread_kiem_tra_huong.start()
                    thread_kiem_tra_huong_x = threading.Thread(target=kiem_tra_huong_va_ve_o_mau, args=(diem_mui, anh))
                    thread_kiem_tra_huong_x.start()

                    anh = ve_hinh_vuong_cung_dinh(anh)
                
                    # Hiển thị kết quả
                    window_name = 'lmao'
                    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
                    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
                    
                    # Thu nhỏ cửa sổ và cho cửa sổ frame xuất hiện ở góc trên bên trái màn hình
                    cv2.moveWindow(window_name, 0, round(screen_height/1360)*550)
                    cv2.resizeWindow(window_name, 200*round(screen_weight/1366), 150*round(screen_height/768))
                    cv2.imshow(window_name, anh)
        
            # Dừng vòng lặp nếu 'q' được nhấn
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            if 'tắt cuộn chuột máy tính 'in text:
                break
            if "mở bàn phím" in text:
                break
        cap.release()
        cv2.destroyAllWindows()
    chuot_may_tinh(0)
