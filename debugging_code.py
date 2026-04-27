from tkinter import *
#this is the debugging screen

def check_input(input):
    print(input)
    print("check input")
    correct_answer = 'print("Hello, world!")'

    if input == correct_answer:
        correct_label = Label(debug_window, text='Correct! Proceed to next level', font=('Calibri', 20))
        correct_label.pack(side='top')

        #move on here
        
    else:
        incorrect_label = Label(debug_window, text='Incorrect, try again', font=('Calibri', 20))
        incorrect_label.pack(side='top')

def get_input():
    input_code = code_entry.get()
    print(input_code)
    check_input(input_code)

def debugging_window():
    global debug_window 
    debug_window = Tk()
    debug_window.title("Debugging Code")

    head_label = Label(debug_window, text='Find the mistake!', font=('Calibri', 30))
    head_label.pack(side='top')

    #show the screenshot with broken code
    wrong_code_img = PhotoImage(file='broken_code.png')
    label = Label(debug_window, image=wrong_code_img)
    label.image = wrong_code_img
    label.pack()

    #secondary label
    second_label = Label(debug_window, text='Enter the correct code below!')
    second_label.pack(side='top')

    #input field for correct code
    global code_entry
    code_entry = Entry(debug_window)
    code_entry.pack(side='top')

    #check button
    check_button = Button(debug_window, text='Check', command=get_input)
    check_button.pack(side='top')

    debug_window.mainloop()

debugging_window()

