from tkinter import *
#this is the debugging screen

def check_input(input):
    print(input)
    print("check input")
    correct_answer = 'print("Hello, world!")'

    if input == correct_answer:
        info_label.config(text='Correct, proceed to the next level!')
        #move on here           
    else:
        info_label.config(text='Incorrect, try again!')

def get_input():
    input_code = code_entry.get()
    print(input_code)
    check_input(input_code)

def debugging_window():
    global debug_window 
    debug_window = Tk()
    debug_window.title("Debugging Code")
    debug_window.geometry('500x300')

    head_label = Label(debug_window, text='Find the mistake!', font=('Calibri', 30))
    head_label.pack(side='top')

    #show the screenshot with broken code
    wrong_code_img = PhotoImage(file='broken_code.png')
    label = Label(debug_window, image=wrong_code_img)
    label.image = wrong_code_img
    label.pack()

    #secondary label
    second_label = Label(debug_window, text='Enter the correct code below!', font=('Calibri', 15))
    second_label.pack(side='top')

    #input field for correct code
    global code_entry
    code_entry = Entry(debug_window, width=25)
    code_entry.pack(side='top')

    #check button
    check_button = Button(debug_window, text='Check', font=('Calibri', 10), command=get_input, padx=20, pady=10)
    check_button.pack(side='top')

    #feedback label
    global info_label
    info_label = Label(debug_window, font=('Calibri', 20))
    info_label.pack(side='top')

    debug_window.mainloop()

debugging_window()

