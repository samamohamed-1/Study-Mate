import tkinter as tk
from tkinter import ttk
from googletrans import Translator
from googletrans.constants import LANGUAGES
import pygame
import time
from gtts import gTTS
from PIL import Image, ImageTk
import uuid
import threading
import os
import subprocess
import sys

translator = Translator()
lang_codes = {v: k for k, v in LANGUAGES.items()}

def go_back(current_window):
    current_window.destroy()
    subprocess.Popen([sys.executable, "timer_interface.py"])

def open_translator():
    show_translator_window()

def show_start_window():
    global start_window
    start_window = tk.Tk()
    start_window.title("Python Translator - Start page")
    start_window.attributes("-fullscreen", True)
    start_window.bind("<Escape>", lambda e: start_window.attributes("-fullscreen", False))
    screen_width = start_window.winfo_screenwidth()
    screen_height = start_window.winfo_screenheight()

    if os.path.exists(os.path.join(os.path.dirname(__file__), "..", "Assets", "translatorlogo.jpeg")):    
        original_image = Image.open(os.path.join(os.path.dirname(__file__), "..", "Assets", "translatorlogo.jpeg"))
        resized_image = original_image.resize((screen_width, screen_height))
        image = ImageTk.PhotoImage(resized_image)
        image_label = tk.Label(start_window, image=image)
        image_label.image = image
        image_label.place(x=0, y=0, relwidth=1, relheight=1)

        canvas = tk.Canvas(start_window, width=355, height=150, bg="#FADADD", bd=0, highlightthickness=0)
        canvas.place(relx=0.52, rely=0.5, anchor="center")
        canvas.create_oval(10, 10, 340, 150, fill="#D67D8F", outline="")
        button_rect = canvas.create_oval(10, 10, 340, 150, fill="#FCA3B7", outline="")
        canvas.tag_raise(button_rect)
        canvas.create_text(160, 80, text="Start", font=("Arial", 56, "bold"), fill="white")

        def on_click(event):
            x, y = event.x, event.y
            if (x - 110) ** 2 + (y - 50) ** 2 < 100 ** 2:
                open_translator()

        canvas.bind("<Button-1>", on_click)

    else:
        start_window.configure(bg='#FADADD')
        canvas = tk.Canvas(start_window, width=355, height=150, bg="#FADADD", bd=0, highlightthickness=0)
        canvas.place(relx=0.52, rely=0.5, anchor="center")
        canvas.create_oval(10, 10, 340, 150, fill="#D67D8F", outline="")
        button_rect = canvas.create_oval(10, 10, 340, 150, fill="#FCA3B7", outline="")
        canvas.tag_raise(button_rect)
        canvas.create_text(160, 80, text="Start", font=("Arial", 56, "bold"), fill="white")

        def on_click(event):
            x, y = event.x, event.y
            if (x - 110) ** 2 + (y - 50) ** 2 < 100 ** 2:
                open_translator()

        canvas.bind("<Button-1>", on_click)

    tk.Button(start_window, text="Back", bg="#A0526C", fg="white", font=("Arial", 12),
              command=lambda: [start_window.destroy(), subprocess.Popen([sys.executable, "timer_interface.py"])]).place(x=20, y=20, width=80, height=40)

    start_window.mainloop()

def show_translator_window():

    def translate_text():
        src = lang_codes[source_lang.get()]
        dest = lang_codes[target_lang.get()]
        text = input_text.get("1.0", tk.END)
        result = translator.translate(text, src=src, dest=dest)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result.text)

    def speak(text, lang):
        if text:
            filename = f"temp_{uuid.uuid4()}.mp3"
            tts = gTTS(text, lang=lang)
            tts.save(filename)
            time.sleep(0.5)
            try:
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                if pygame.mixer.music.get_busy():
                    pygame.mixer.music.stop()
                time.sleep(0.2)
                pygame.mixer.music.load(filename)
                pygame.mixer.music.play()

                def delete_after_play():
                    while pygame.mixer.music.get_busy():
                        time.sleep(0.5)
                    try:
                        os.remove(filename)
                    except Exception as e:
                        print(f"Error deleting file: {e}")

                threading.Thread(target=delete_after_play, daemon=True).start()

            except pygame.error as e:
                print("Audio error", e)

    def speak_input():
        text = input_text.get("1.0", tk.END).strip()
        speak(text, lang_codes[source_lang.get()])

    def speak_output():
        text = output_text.get("1.0", tk.END).strip()
        speak(text, lang_codes[target_lang.get()])

    def stop_sound():
        if pygame.mixer.get_init():
            pygame.mixer.music.stop()

    def save_translation():
        text = output_text.get("1.0", tk.END).strip()
        if text:
            with open("saved_translation.txt", "a", encoding="utf-8") as f:
                f.write(text + "\n---\n")
            status_label.config(text="Translation Saved!")

    def show_history():
        history_window = tk.Toplevel(root)
        history_window.title("Translation History")
        history_window.geometry("800x500")
        history_window.configure(bg="#F6E5EC")
        tk.Label(history_window, text="Translation History", font=("Arial", 20, "bold"), bg="#F6E5EC").pack(pady=10)
        history_text = tk.Text(history_window, wrap="word", font=("Arial", 14))
        history_text.pack(expand=True, fill="both", padx=20, pady=10)

        try:
            with open("saved_translation.txt", "r", encoding="utf-8") as f:
                history = f.read()
            history_text.insert("1.0", history)
        except FileNotFoundError:
            history_text.insert("1.0", "No history found.")

        tk.Button(history_window, text="Close", bg="#C97B9B", fg="white", font=("Arial", 14),
                  command=history_window.destroy).pack(pady=10)

    def exit_program():
        root.destroy()
        sys.exit()

    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.title("Python Translator")
    root.configure(bg="#F6E5EC")

    tk.Button(root, text="✖", bg="#C97B9B", fg="white", font=("Arial", 16),
              command=exit_program).place(x=20, y=20, width=40, height=40)

    # النص الأصلي
    tk.Label(root, text="Original Text:", font=("Arial", 16), bg="#F6E5EC").pack(pady=(50, 0))
    input_text = tk.Text(root, height=8, font=("Arial", 16))
    input_text.pack(fill="x", padx=70)
    button = tk.Button(root, text="🔊", command=speak_input, bg="#D48C4D", fg="white", font=("Arial", 16))
    button.place(x=1475, y=230)

    # اختيار اللغات
    frame = tk.Frame(root, bg="#F6E5EC")
    frame.pack(pady=10)
    tk.Label(frame, text="From Language:", bg="#F6E5EC", font=("Arial", 16)).grid(row=0, column=0, padx=10)
    source_lang = ttk.Combobox(frame, values=list(lang_codes.keys()), font=("Arial", 14), width=15)
    source_lang.set("arabic")
    source_lang.grid(row=0, column=1, padx=10)
    tk.Label(frame, text="To Language:", bg="#F6E5EC", font=("Arial", 16)).grid(row=0, column=2, padx=10)
    target_lang = ttk.Combobox(frame, values=list(lang_codes.keys()), font=("Arial", 14), width=15)
    target_lang.set("english")
    target_lang.grid(row=0, column=3, padx=10)
    tk.Button(root, text="Translate", bg="#E78BA4", fg="white", font=("Arial", 16), command=translate_text).pack(pady=10)

    # إطار الترجمة + زر الصوت على اليمين داخل الإطار
    output_frame = tk.Frame(root, bg="#F6E5EC")
    output_frame.pack(fill="x", padx=40)
    tk.Label(output_frame, text="Translation:", font=("Arial", 16), bg="#F6E5EC").pack(anchor="center")
    text_and_btn_frame = tk.Frame(output_frame, bg="#F6E5EC")
    text_and_btn_frame.pack(fill="x")
    output_text = tk.Text(text_and_btn_frame, height=8, width=115, font=("Arial", 16))
    output_text.pack(side="left", fill="y", expand=True)
    speak_output_btn = tk.Button(root, text="🔊", command=speak_output, bg="#D48C9D", fg="white", font=("Arial", 16))
    speak_output_btn.place(x=1470, y=570)

    # أزرار Stop Sound و Save Translation بيضاوية على يسار ويمين في إطار أفقي
    buttons_frame = tk.Frame(root, bg="#F6E5EC")
    buttons_frame.pack(fill="x", padx=40, pady=20)
    stop_btn = tk.Button(buttons_frame, text="Stop Sound", bg="#B580A6", fg="white", font=("Arial", 16), command=stop_sound)
    stop_btn.pack(side="left", ipadx=25, ipady=8, padx=(0, 10))
    stop_btn.config(relief='raised', bd=3, borderwidth=3, highlightthickness=0, cursor="hand2")
    stop_btn.configure(borderwidth=3, highlightbackground="#B580A6", highlightcolor="#B580A6")
    stop_btn.configure(overrelief='ridge')
    save_btn = tk.Button(buttons_frame, text="Save Translation", bg="#B580A6", fg="white", font=("Arial", 16), command=save_translation)
    save_btn.pack(side="right", ipadx=25, ipady=8, padx=(10, 0))
    save_btn.config(relief='raised', bd=3, borderwidth=3, highlightthickness=0, cursor="hand2")
    save_btn.configure(borderwidth=3, highlightbackground="#B580A6", highlightcolor="#B580A6")
    save_btn.configure(overrelief='ridge')
    history_btn = tk.Button(buttons_frame, text="Show History", bg="#B580A6", fg="white", font=("Arial", 16),
                            command=show_history)
    history_btn.pack(side="left", ipadx=20, ipady=8, padx=(450, 10))
    history_btn.config(relief='raised', bd=3, borderwidth=3, highlightthickness=0, cursor="hand2")
    history_btn.configure(borderwidth=3, highlightbackground="#B580A6", highlightcolor="#B580A6")
    history_btn.configure(overrelief='ridge')
    status_label = tk.Label(root, text="", fg="green", bg="#F6E5EC", font=("Arial", 14))
    status_label.pack()

    root.mainloop()

show_start_window()

