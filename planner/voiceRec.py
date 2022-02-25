import speech_recognition as sr
from tkinter import *
from tkinter import messagebox

import time

r = sr.Recognizer()

def TaskContentVoiceRec(window, x, y, object):
    fail = 0
    while True:    
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source, duration = 1)
            print('Powiedz cokolwiek:')
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio, language = 'pl-PL')
                break
            except:
                fail = 1
                break
                
    if fail == 1:            
        messagebox.showinfo("Planner", "nie mogę zrozumieć")
    
    if fail == 0:
        object.insert(END, f"{text} ")
