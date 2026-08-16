import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import subprocess
import threading
import time
import random
import customtkinter as ctk
import pygame
pygame.init()
pygame.mixer.init()
import sys
import os
class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Study Timer")
        self.root.attributes('-fullscreen', True)
        # خلفية الصفحة الرئيسية
        self.bg_image_main = Image.open(os.path.join(os.path.dirname(__file__), "..", "Assets", "study mate.jpeg"))                                
        self.bg_photo_main = ImageTk.PhotoImage(
            self.bg_image_main.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight())))
        # خلفية صفحة التايمر
        self.bg_image_timer = Image.open(os.path.join(os.path.dirname(__file__), "..", "Assets", "first page.jpg"))
        self.bg_photo_timer = ImageTk.PhotoImage(
            self.bg_image_timer.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight())))
        # Canvas
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill='both', expand=True)
        # صورة الخلفية على الكانفس
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.bg_photo_main, anchor='nw')
        self.user_name = ""
        self.time_left = 0
        self.is_paused = False
        self.timer_thread = None
        self.motivational_messages = [
            "Let's go {}! ✨",
            "زي ما سيمبا رجع يحكم الغابة، إنت كمان هترجع تكسر الدنيا!🦁",
            "Great job {}! 👏",
            "قدها و قدود 🙈",
            "Stay focused {}! 💪",
            "ايه الحلاوة دى✨",
            "Keep it up {}! 🔥",
            "شغل جامد جامودة🔥",
            "You're unstoppable {}! 🚀",
            "الله ينور💡",
            "You nailed it!🫵🏻",
            """قوم يحمادة عه 
            قوم عاد يحمادة
            ذهب الليل و طفح الكيل🙆🏻"""
        ]
        self.show_welcome_screen()
    def set_background(self, image):
        self.canvas.itemconfig(self.canvas_bg, image=image)
    def show_welcome_screen(self):
        self.clear_widgets()
        self.set_background(self.bg_photo_main)
        exit_btn = tk.Button(self.root, text='×', font=('Arial', 20, 'bold'), bg='#7B4B94', fg='white',
                             borderwidth=0, command=self.root.quit)
        exit_btn.place(x=10, y=10, width=40, height=40)
        self.name_entry = ctk.CTkEntry(self.root, font=('Arial', 35), width=350, height=60, fg_color='#F0EAF4',
                                       text_color="black", corner_radius=30)
        self.name_entry.place(relx=0.5, rely=0.9, anchor='center')
        self.name_entry.insert(0, "Enter your name")
        self.name_entry.bind("<FocusIn>", self.clear_placeholder)
        self.name_entry.bind("<FocusOut>", self.add_placeholder)
        start_button = ctk.CTkButton(self.root, text="Start Study Session", fg_color='#7B4B94',
                                     text_color='white', font=('Arial', 35),
                                     command=self.start_session_clicked, corner_radius=30)
        start_button.place(relx=0.8, rely=0.9, anchor='center')
        todo_button = ctk.CTkButton(self.root, text="To-Do List", fg_color='#7B4B94', text_color='white',
                                    font=('Arial', 35),
                                    command=self.open_todo, corner_radius=30)
        todo_button.place(relx=0.2, rely=0.9, anchor='center')
    def clear_placeholder(self, event):
        if self.name_entry.get() == "Enter your name":
            self.name_entry.delete(0, tk.END)
            self.name_entry.configure(text_color='black')
    def add_placeholder(self, event):
        if not self.name_entry.get():
            self.name_entry.insert(0, "Enter your name")
            self.name_entry.configure(text_color='grey')
    def clear_widgets(self):
        for widget in self.root.winfo_children():
            if widget != self.canvas:
                widget.destroy()
    def start_session_clicked(self):
        name = self.name_entry.get().strip()
        if not name or name == "Enter your name":
            messagebox.showerror("Error", "Name is required!")
            return
        self.user_name = name
        self.show_timer_screen()
    def show_timer_screen(self):
        self.clear_widgets()
        self.set_background(self.bg_photo_timer)
        self.time_label = tk.Label(self.root, text="Enter session time:", font=('Arial', 24), fg='white', bg='#FF69B4')
        self.time_label.place(relx=0.5, rely=0.65, anchor='center')
        self.time_entry = tk.Entry(self.root, font=('Arial', 24))
        self.time_entry.place(relx=0.5, rely=0.72, anchor='center', width=200, height=40)
        self.unit_var = tk.StringVar(value='Seconds')
        self.unit_spinner = ttk.Combobox(self.root, textvariable=self.unit_var, values=['Seconds', 'Minutes', 'Hours'],
                                         font=('Arial', 18), state='readonly')
        self.unit_spinner.place(relx=0.5, rely=0.79, anchor='center', width=150)
        start_button = ctk.CTkButton(self.root, text="Start Timer", fg_color='#7B4B94',
                                     text_color='white', font=('Arial', 35),
                                     command=self.start_timer, corner_radius=30)
        start_button.place(relx=0.8, rely=0.9, anchor='center')
        back_button = ctk.CTkButton(self.root, text="back", fg_color='#7B4B94',
                                    text_color='white', font=('Arial', 35),
                                    command=self.show_welcome_screen, corner_radius=30)
        back_button.place(relx=0.2, rely=0.9, anchor='center')
    def start_timer(self):
        try:
            input_value = int(self.time_entry.get())
            unit = self.unit_var.get()
            if unit == 'Seconds':
                self.time_left = input_value
            elif unit == 'Minutes':
                self.time_left = input_value * 60
            elif unit == 'Hours':
                self.time_left = input_value * 3600
            if self.time_left <= 0:
                messagebox.showerror("Error", "Enter a value greater than 0!")
                return
        except ValueError:
            messagebox.showerror("Error", "Enter a valid number!")
            return
        self.show_countdown_screen()
        self.is_paused = False
        self.timer_thread = threading.Thread(target=self.countdown)
        self.timer_thread.daemon = True
        self.timer_thread.start()
    def show_countdown_screen(self):
        self.clear_widgets()
        self.set_background(self.bg_photo_timer)
        self.timer_label = tk.Label(self.root, text="", font=('Arial', 72), fg='white', bg='#C97B9B')
        self.timer_label.place(relx=0.5, rely=0.1, anchor='center')
        self.message_label = tk.Label(self.root, text="", font=('Arial', 36), fg='white', bg='#C97B9B')
        self.message_label.place(relx=0.5, rely=0.65, anchor='center')
        pause_btn = ctk.CTkButton(self.root, text="Pause", fg_color='#7B4B94',
                                  text_color='white', font=('Arial', 35),
                                  command=self.toggle_pause, corner_radius=30)
        pause_btn.place(relx=0.5, rely=0.9, anchor='center')
        self.pause_button = pause_btn
        translator_btn = ctk.CTkButton(self.root, text="Translator", fg_color='#7B4B94',
                                       text_color='white', font=('Arial', 35),
                                       command=self.open_translator, corner_radius=30)
        translator_btn.place(relx=0.2, rely=0.9, anchor='center')
        todo_btn = ctk.CTkButton(self.root, text="To-Do List", fg_color='#7B4B94',
                                 text_color='white', font=('Arial', 35),
                                 command=self.open_todo, corner_radius=30)
        todo_btn.place(relx=0.8, rely=0.9, anchor='center')
    def countdown(self):
        message_counter = 0
        while self.time_left > 0:
            if not self.is_paused:
                mins, secs = divmod(self.time_left, 60)
                hours, mins = divmod(mins, 60)
                time_str = f"{hours:02d}:{mins:02d}:{secs:02d}"
                self.update_timer_label(time_str)
                self.time_left -= 1
                message_counter += 1
                if message_counter == 5:
                    self.show_motivation()
                    message_counter = 0
            time.sleep(1)
        self.update_timer_label("00:00:00")
        # self.show_final_screen()
        self.root.after(0, self.show_final_screen)

    def update_timer_label(self, text):
        def update():
            if self.timer_label.winfo_exists():
                self.timer_label.config(text=text)
        self.timer_label.after(0, update)
    def show_motivation(self):
        message = random.choice(self.motivational_messages).format(self.user_name)
        def update():
            if self.message_label.winfo_exists():
                self.message_label.config(text=message)
        self.message_label.after(0, update)

    def stop_music_and_restart(self):
        pygame.mixer.music.stop()  # توقف الموسيقى
        self.show_welcome_screen()  # ارجع لشاشة الترحيب
    def show_final_screen(self):
        for widget in self.root.winfo_children():
            if widget != self.canvas:
                widget.destroy()
        pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), "..", "Assets", "alarm.wav"))
        pygame.mixer.music.play()
        final_msg = tk.Label(self.root, text=f"Well done {self.user_name}! 🎉🔥", font=('Arial', 48), fg='white',
                             bg='#C97B9B')
        final_msg.place(relx=0.5, rely=0.7, anchor='center')
        restart_btn = ctk.CTkButton(self.root, text="Restart", fg_color='#7B4B94', text_color='white',
                                    font=('Arial', 35),
                                    command=self.stop_music_and_restart, width=250, height=60, corner_radius=30)
        restart_btn.place(relx=0.2, rely=0.9, anchor='center')
        exit_btn = ctk.CTkButton(self.root, text="Exit", fg_color='#7B4B94', text_color='white',
                                 font=('Arial', 35),
                                 command=self.root.destroy, width=250, height=60, corner_radius=30)
        exit_btn.place(relx=0.8, rely=0.9, anchor="center")
    def stop_music_and_restart(self):
        pygame.mixer.music.stop()  # توقف الموسيقى
        self.show_welcome_screen()

    def toggle_pause(self):
        try:
            self.is_paused = not self.is_paused
            self.pause_button.config(text="Resume" if self.is_paused else "Pause")
        except Exception:
            pass
    def open_translator(self):
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "translator.py")])

    def open_todo(self):
        subprocess.Popen([sys.executable, os.path.join(os.path.dirname(__file__), "todo_app.py")])    
if __name__ == '__main__':
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()










