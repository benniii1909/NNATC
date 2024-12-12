import speech_recognition as sr
from DIEUKHIENCHUOT import *
import subprocess
import os
from DONG_MO_UNG_DUNG import*
from CHUYEN_CUA_SO import*
from CHUYEN_VAN_BAN_THANH_GIONG_NOI import *
from AM_LUON import *
from CUONCHUOT import *
from gtts import gTTS
import playsound
import pyttsx3
import pystray
from pystray import MenuItem as item
from PIL import Image
import threading
import shutil
import tkinter as tk


def find_file_in_system(filename):
    for root, dirs, files in os.walk('/'):
        if filename in files:
            return os.path.join(root, filename)
    return None

def find_file_in_system_l(foldername):
    for root, dirs, files in os.walk('C:/Users/'):
        if foldername in files:
            return os.path.join(root, foldername)
    return None

def run():

    def giong_noi(textt):
        tts = gTTS(text=textt, lang='vi')
        filename='giong noi.mp3'
        tts.save(filename)
        playsound.playsound(filename)
        os.remove(filename)
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

    def nhan_dien_chuc_nang(text):
        if "mở chuột máy tính" in text:
            giong_noi("đang mở chuột máy tính")
            run_chuot_may_tinh()

        if "mở bàn phím" in text:
            giong_noi("đang mở bàn phím bằng giọng nói")
            nhan_dien_giong_noi()

        if 'mở cuộn chuột máy tính' in text:
            run_cuon_chuot_may_tinh()
        
        if 'mở chrome' in text:
            giong_noi("đang mở chrome")
            file_path = find_file_in_system("chrome.exe")
            if file_path is None:
                giong_noi("không có chrome trên máy")
            subprocess.Popen([file_path])

        if "tăng âm lượng lên" in text:
            tang_am_luong(text)

        if "giảm âm lượng xuống" in text:
            giam_am_luong(text)

        if 'mở zalo' in text:
            giong_noi("đang mở zalo")
            
            file_path = find_file_in_system("Zalo.exe")
            if file_path is None:
                giong_noi("không có zalo trên máy")
            subprocess.Popen([file_path])
        if 'mở file explorer' in text:
            giong_noi("đang mở file explorer")
            pyautogui.hotkey('win','e')

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
                    print(so)
                for i in range (1,so):
                    pyautogui.hotkey('backspace')
            xoa_ki_tu(text)
        
    recognizer = sr.Recognizer()
    while not stop_event.is_set():
        print(".")
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio=recognizer.listen(source)
            try:
                text1=recognizer.recognize_google(audio, language='vi-VN')#nhận giọng nói tiếng Việt
                text = text1.lower()#chuyển tất cả về viết thường
                print(text)
                text=text+" "#thêm kí tự cách để ko bị lỗi
                nhan_dien_chuc_nang(text)
                if text!=" ":
                    thread_thong_bao=threading.Thread(target=thong_bao(text))
                    thread_thong_bao.start()
                if 'dừng chương trình' in text:
                    break
            except sr.UnknownValueError:
                pass
            except sr.RequestError:
                engine = pyttsx3.init()
                engine.say('No internet connection')
                engine.runAndWait()

stop_event = threading.Event()


def thong_bao_1():
    window = tk.Tk()
    window.title("NNATC")
    label = tk.Label(window, text="Đã chạy chương trình",font=3)
    label.pack()

    # Hàm để đóng cửa sổ sau 3 giây
    def close_window():
        window.destroy()

    # Đặt hẹn giờ để đóng cửa sổ
    window.after(3000, close_window)

    # Hiển thị cửa sổ thông báo
    window.mainloop()

def thong_bao_2():
    window = tk.Tk()
    window.title("NNATC")
    label = tk.Label(window, text="Đã dừng chương trình",font=3)
    label.pack()

    # Hàm để đóng cửa sổ sau 3 giây
    def close_window():
        window.destroy()

    # Đặt hẹn giờ để đóng cửa sổ
    window.after(3000, close_window)

    # Hiển thị cửa sổ thông báo
    window.mainloop()

    # Hàm để đóng cửa sổ sau 3 giây
    def close_window():
        window.destroy()

    # Đặt hẹn giờ để đóng cửa sổ
    window.after(3000, close_window)

    # Hiển thị cửa sổ thông báo
    window.mainloop()

def thong_bao_3():
    window = tk.Tk()
    window.title("NNATC")
    label = tk.Label(window, text="Đã đóng chương trình",font=3)
    label.pack()

    # Hàm để đóng cửa sổ sau 3 giây
    def close_window():
        window.destroy()

    # Đặt hẹn giờ để đóng cửa sổ
    window.after(3000, close_window)

    # Hiển thị cửa sổ thông báo
    window.mainloop()

def thong_bao_4():
    window = tk.Tk()
    window.title("NNATC")
    label = tk.Label(window, text="Đã lưu file vào thư mục Startup",font=3)
    label.pack()

    # Hàm để đóng cửa sổ sau 3 giây
    def close_window():
        window.destroy()

    # Đặt hẹn giờ để đóng cửa sổ
    window.after(3000, close_window)

    # Hiển thị cửa sổ thông báo
    window.mainloop()

def thong_bao_5():
    window = tk.Tk()
    window.title("NNATC")
    label = tk.Label(window, text="Đã xóa file khỏi thư mục Startup",font=3)
    label.pack()

    # Hàm để đóng cửa sổ sau 3 giây
    def close_window():
        window.destroy()

    # Đặt hẹn giờ để đóng cửa sổ
    window.after(3000, close_window)

    # Hiển thị cửa sổ thông báo
    window.mainloop()


def exit(icon, item):
    thong_bao_3()
    icon.stop()
    
def on(icon, item):
    global thread
    thong_bao_1()
    stop_event = threading.Event()
    # Bắt đầu thread
    thread = threading.Thread(target=run(), args=(stop_event,))
    thread.start()
def off(icon, item):
    global thread
    thong_bao_2()
    stop_event.set()
def startup(icon, item):
    thong_bao_4()
    global new_file_path
    global new_file_path_anh
    filename = 'MAIN_NNATC.exe'
    file_path=find_file_in_system(filename)
    print (file_path)
    filename_anh = 'iconNNATC.png'
    diri=find_file_in_system(filename_anh)
    # Đường dẫn của thư mục startup
    startup_dir = os.path.expanduser('~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup')
    startup_dir_l = os.path.expanduser('~\AppData\Roaming\Microsoft\Windows\Start Menu\Programs')
    # Đường dẫn của file sau khi được chuyển vào thư mục startup
    new_file_path = os.path.join(startup_dir, os.path.basename(file_path))
    new_file_path_anh = os.path.join(startup_dir_l, os.path.basename(diri))
    # Chuyển file vào thư mục startup
    shutil.copyfile(file_path, new_file_path)
    shutil.copyfile(diri, new_file_path_anh)
def delete_startup(icon, item):
    thong_bao_5()
    
    # Kiểm tra xem file có tồn tại không
    if os.path.exists(new_file_path):
    # Xóa file
        os.remove(new_file_path)
    # Kiểm tra xem file có tồn tại không
    if os.path.exists(new_file_path_anh):
    # Xóa file
        os.remove(new_file_path_anh) 
# Tạo menu cho icon

# Sử dụng hàm
filename = 'iconNNATC.png'
dir=find_file_in_system(filename)
print(dir)
menu = (item('Thoát', exit),item('Chạy chương trình', on), item('Dừng chương trình', off)
        ,item('Khởi động cùng Window', startup),item('Tắt khởi động cùng Window', delete_startup))

# Đọc hình ảnh icon từ file hoặc sử dụng hình ảnh mặc định
image = Image.open(dir) if dir else pystray.Icon.DEFAULT_IMAGE

# Tạo icon trong khay hệ thống
icon = pystray.Icon("name", image, "Title", menu=menu)

# Khởi động icon
icon.run()

