from tkinter import *
import random
import sys
import subprocess
#this is the debugging screen

def check_input(input):
    print(input)
    print("check input")
    correct_answer1 = 'print("Hello, world!")'
    correct_answer2 = 'if value == 5:'
    correct_answer3 = 'x = 5 + 10'

    #check input from user is correct
    if input == correct_answer1 or input == correct_answer2 or input == correct_answer3:
        info_label.config(text='Correct!')
        #move on here    
        print("opening second level")
        subprocess.Popen([sys.executable, r"C:\Users\aidan\OneDrive\Documents\UNI WORK\Bartek Git\The_Compiler\game\level2.py"])
        print("passed Popen")
        debug_window.destroy()
    else:
        info_label.config(text='Incorrect, try again!')

def get_input():
    input_code = code_entry.get()
    print(input_code) #testing
    check_input(input_code)

def on_enter(e):
    e.widget.config(bg="#FFD166", fg="#3A0066")

def on_leave(e):
    e.widget.config(bg="#FF8C00", fg="#FFF5CC")

def get_random():
    randnum = random.randrange(1,4)
    return randnum

def show_image():
    num = get_random()
    file_path = ''
    if num == 1:
        file_path = 'broken_code_ez1.png'
    elif num == 2:
        file_path = 'broken_code_ez2.png'
    elif num == 3:
        file_path = 'broken_code_ez3.png'

    #show the screenshot with broken code
    wrong_code_img = PhotoImage(file=file_path)
    label = Label(debug_window, image=wrong_code_img)
    label.image = wrong_code_img
    label.pack()

def debugging_window():
    global debug_window 
    debug_window = Tk()
    debug_window.title("Debugging Code")
    debug_window.geometry('500x375')
    debug_window.config(bg="#3A0066")

    head_label = Label(debug_window, text='Find the mistake!', bg="#3A0066", fg="#FFF5CC", font=('Courier', 30))
    head_label.pack(side='top', pady=10)

    #secondary label
    second_label = Label(debug_window, text='Enter the correct code below!', bg="#3A0066", fg="#FFF5CC", font=('Courier', 15))
    second_label.pack(side='top', pady=10)

    #screenshot here
    show_image()

    #input field for correct code
    global code_entry
    code_entry = Entry(debug_window, width=25, font=('Courier', 20))
    code_entry.pack(side='top', pady=20)

    #check button
    check_button = Button(debug_window, text='Check', font=('Courier', 10), 
                          bg="#FF8C00",
                          fg="#FFF5CC",
                          activebackground="#4B0082",
                          activeforeground="#00FFFF",
                          command=get_input, padx=20, pady=10)
    check_button.pack(side='top')


    #feedback label
    global info_label
    info_label = Label(debug_window, bg="#3A0066", fg="#FFF5CC", font=('Courier', 20))
    info_label.pack(side='top')

    for btn in [check_button]:
        btn.bind("<Enter>", on_enter)
        btn.bind("<Leave>", on_leave)

    debug_window.mainloop()

debugging_window()