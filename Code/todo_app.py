import tkinter as tk
import ttkbootstrap as tkk
from tkinter import Listbox, END, SINGLE
from PIL import Image, ImageTk
import os

class WelcomeScreen:
    def __init__(self, root, on_start):
        self.root = root
        self.on_start = on_start
        self.style = tkk.Style(theme="flatly")
        self.root.attributes("-fullscreen", True)
        # تحميل الصورة
        original_image= Image.open(os.path.join(os.path.dirname(__file__), "..", "Assets", "to do.jpeg"))
        self.img = ImageTk.PhotoImage(original_image)
        # عرضها ووضعها
        self.bg_label = tk.Label(root, image=self.img)
        self.bg_label.pack()
        # start button
        self.style.configure('My.TButton', font=('Helvetica', 24, 'bold'))
        self.start_button = tkk.Button(root, text="Organize your tasks", bootstyle="primary", style='My.TButton', command=self.start,
        width=25)
        self.start_button.place(relx=0.5, rely=0.85, anchor="center")
        # زر ال back
        back_button = tkk.Button(root, text="back", bootstyle="primary", command=self.root.destroy, width=8)
        back_button.place(relx=0.0, rely=0.0, anchor="nw")

    def start(self):
        self.bg_label.destroy()
        self.start_button.destroy()
        self.on_start()

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.attributes('-fullscreen', True)
        self.style = tkk.Style(theme="flatly")
        self.style.configure('Big.TButton',
        font=('Helvetica', 18, 'bold'),
        padding=(20, 10),
        foreground='white',
        background='#6c757d'  # لون رصاصى
        )
        self.root.configure(bg="#ffe6ea")
        # زر ال exit
        exit_button = tkk.Button(root, text="✖️", bootstyle="primary", command=root.destroy)
        exit_button.pack(side="top", anchor="nw")

        title = tkk.Label(root, text="🦋 To-Do List 🦋", font=("Helvetica", 32, "bold"), background="#ffe6ea")
        title.pack(pady=40)
        self.task_entry = tkk.Entry(root, width=40, font=("Helvetica", 24))
        self.task_entry.pack(pady=10)
        btn_frame = tkk.Frame(root, padding=10)
        btn_frame.pack()
        tkk.Button(btn_frame, text="➕ Add", style='Big.TButton', command=self.add_task, width=18).grid(row=0, column=0, padx=5)
        tkk.Button(btn_frame, text="✔️ Done", style='Big.TButton', command=self.mark_done, width=18).grid(row=0, column=1, padx=5)
        tkk.Button(btn_frame, text="🗑️ Delete", style='Big.TButton',command=self.delete_task, width=18).grid(row=0, column=2, padx=5)
        tkk.Button(btn_frame, text="💾 Save", style='Big.TButton', command=self.save_tasks, width=18).grid(row=0, column=3,padx=5)
        tkk.Button(btn_frame, text="📥 Load", style='Big.TButton', command=self.load_tasks, width=18).grid(row=0, column=4, padx=5)
        self.listbox = Listbox(root, font=("Helvetica", 24), selectmode=SINGLE, width=80, height=50)
        self.listbox.pack(pady=20)
        self.tasks = []

    def add_task(self):
        task = self.task_entry.get()
        if task:
            self.tasks.append(task)
            self.update_list()
            self.task_entry.delete(0, END)

    def delete_task(self):
        selected = self.listbox.curselection()
        if selected:
            del self.tasks[selected[0]]
            self.update_list()

    def mark_done(self):
        selected = self.listbox.curselection()
        if selected:
            index = selected[0]
            self.tasks[index] += " ✔️"
            self.update_list()

    def save_tasks(self):
        with open("tasks.txt", "w", encoding="utf-8") as file:
            for task in self.tasks:
                file.write(task + "\n")

    def load_tasks(self):
        try:
            with open("tasks.txt", "r", encoding="utf-8") as file:
                self.tasks = [line.strip() for line in file.readlines()]
            self.update_list()
        except FileNotFoundError:
            print("No saved tasks found.")

    def update_list(self):
        self.listbox.delete(0, END)
        for task in self.tasks:
            self.listbox.insert(END, task)

if __name__ == "__main__":
    root = tk.Tk()
    def launch_todo():
        ToDoApp(root)
    welcome = WelcomeScreen(root, on_start=launch_todo)
    root.mainloop()

