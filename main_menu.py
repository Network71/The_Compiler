
# def play_game():
#     print("Game is running.")

# def main():
#     #main menu for the game
#     main_window = Tk()
#     main_window.title('The Compiler')

#     header_label = Label(main_window, text='Welcome to The Compiler', font=('Calibri', 44))             
#     header_label.grid(row=0, column=0)

#     button_1 = Button(main_window, text='Start', command=play_game, font=('Comic Sans MS', 30))
#     button_1.grid(row=2, column=0, columnspan=2)

#     main_window.mainloop()

# main()

from tkinter import *

game_overview_window = NONE


window = Tk()
window.title("Compiler")
window.geometry('700x700')
window.config(bg="#e39ea8")


for row in range(5):
    window.rowconfigure(row, weight=1)

for col in range(3):
    window.columnconfigure(col, weight=1)

# Heading
Hilda_label = Label(
    window,
    text="COMPILER",
    font=('Arial', 40, 'bold'),
    bg="#e39ea8"
)

Hilda_label.grid(row=0, column=1)

# Frame for buttons

button_frame = Frame(window, bg="#e39ea8")
button_frame.grid(row=1, column=1)

#-------------------game overview function-----------------
def game_overview():
    global game_overview_window
    window.withdraw()

    game_overview_window = Toplevel(window, bg='#39FF14')
    game_overview_window.geometry("700x700")

    Label(game_overview_window,
          text="Game Overview",
          bg='#39FF14',
          font=('Arial',45,'bold')).grid(row=0, column=0)

    go_back_menu = Button(
        game_overview_window,
        text="GO BACK",
        command=return_from_game_overview
    )
    go_back_menu.grid(row=3, column=2)

    game_overview_window.protocol("WM_DELETE_WINDOW",return_from_game_overview)

def return_from_game_overview():
    game_overview_window.destroy()
    window.update()
    window.deiconify()

#----------def star_play_button():-----------
#this where the function will be called for the game
#--------------------------------------------
play_button = Button(button_frame, 
                    text= "Play",
                    font=('Arial', 20, 'bold'),
                    bg="black",
                    fg="white",
)
play_button.grid(row=1, column=1, pady=10)

game_overview_button = Button(button_frame, 
                    text= "Game Overview",
                    font=('Arial', 20, 'bold'),
                    bg="black",
                    fg="white",
                    command= game_overview             
)
game_overview_button.grid(row=3, column=1, pady=10)

difficulty_button = Button(button_frame, 
                    text= "Difficulty",
                    font=('Arial', 20, 'bold'),
                    bg="black",
                    fg="white"
)
difficulty_button.grid(row=2, column=1, pady=10)



#-------------------quit window function-----------------
def quit_window():
    window.withdraw()

quit_button = Button(button_frame, 
                    text= "Quit",
                    font=('Arial', 20, 'bold'),
                    bg="black",
                    fg="white",
                    command= quit_window             
)
quit_button.grid(row=4, column=1, pady=10)


window.mainloop()



