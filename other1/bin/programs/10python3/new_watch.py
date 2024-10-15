import tkinter as tk
import time 
import datetime
import schedule

def button_clicked():
    app.destroy()

def update_time():
    now = datetime.datetime.now()
    time_label_time.config(text=now.strftime("%H:%M:%S.%f"))
    time_label_calender.config(text=now.strftime("%Y/%m/%d"))
    app.after(5, update_time)

app = tk.Tk()
app.title("New Watch")
app.geometry("290x175+0+0")
app.config(bg="#64FA64")

time_label_time = tk.Label(app, font=("MV Boli", "35", "bold"))
time_label_time.place(x=0, y=75)
time_label_time.config(bg="#64FA64")
time_label_calender = tk.Label(app, font=("MV Boli", "35", "bold"))
time_label_calender.place(x=0, y=0)
time_label_calender.config(bg="#64FA64")
update_time()

button = tk.Button(app,
                   text="Exit", 
                   command=button_clicked,
                   activebackground="blue", 
                   activeforeground="white",
                   anchor="center",
                   bd=3,
                   bg="red",
                   cursor="hand2",
                   disabledforeground="red",
                   fg="black",
                   font=("MV Boli", 12),
                   height=1,
                   highlightbackground="black",
                   highlightcolor="green",
                   highlightthickness=2,
                   justify="center",
                   overrelief="raised",
                   padx=1,
                   pady=1,
                   width=4,
                   wraplength=100
                   )

button.place(x=240, y=135)

app.mainloop()