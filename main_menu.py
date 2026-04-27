from tkinter import *

def play_game():
    print("Game is running.")

def main():
    #main menu for the game
    main_window = Tk()
    main_window.title('The Compiler')

    header_label = Label(main_window, text='Welcome to The Compiler', font=('Calibri', 44))             
    header_label.grid(row=0, column=0)

    button_1 = Button(main_window, text='Start', command=play_game, font=('Comic Sans MS', 30))
    button_1.grid(row=2, column=0, columnspan=2)

    main_window.mainloop()

main()

