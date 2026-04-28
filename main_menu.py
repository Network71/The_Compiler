
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

game_overview_window = None
credits_window = None

window = Tk()
window.title("Compiler")
window.geometry('700x700')
window.config(bg="#3A0066")


for row in range(5):
    window.rowconfigure(row, weight=1)

for col in range(3):
    window.columnconfigure(col, weight=1)

# Heading
Hilda_label = Label(
    window,
    text="Compiler",
    font=('Courier', 40, 'bold'),
    bg="#3A0066",
    fg="#FFF5CC"
)

Hilda_label.grid(row=0, column=1)

# ---------------- TITLE ANIMATION ----------------
def pulse(size=40):
    new_size = size + 2 if size < 44 else 40
    Hilda_label.config(font=('Courier', new_size, 'bold'))
    window.after(500, lambda: pulse(new_size))

pulse()

# Frame for buttons

button_frame = Frame(window, bg="#3A0066")
button_frame.grid(row=1, column=1)

#-------------------game overview function-----------------
def game_overview():
    global game_overview_window
    window.withdraw()

    game_overview_window = Toplevel(window, bg="#3A0066")
    game_overview_window.geometry("700x700")

    for col in range(3):
        game_overview_window.columnconfigure(col, weight=1)
        game_overview_window.rowconfigure(1, weight=1)



    Label(game_overview_window,
          text="Game Overview",
          bg="#3A0066",
          fg= "#FFF5CC",
          font=('Courier',45)).grid(row=0, column=1)

    go_back_menu = Button(
        game_overview_window,
        font= "Courier",
        text="GO BACK",
        bg="#FF8C00",            
        fg="#FFF5CC",            
        activebackground="#4B0082",
        activeforeground="#00FFFF",
        command=return_from_game_overview
    )
    go_back_menu.grid(row=2, column=1,sticky='s', pady=20)

    Label(game_overview_window,
          text="""This 2D computer science game allows players to collect 
    and debug broken code in order to advance through levels. 
    As progression continues, players face more 
complex programming languages and increasingly 
difficult challenges.The game is aimed at a non-technical audience, 
    making debugging concepts easy to understand and engage with.
""",
          bg="#3A0066",
          fg="#FFF5CC",
          justify= "center",
          font=('Courier',13)).grid(row=1, column=1)

    game_overview_window.protocol("WM_DELETE_WINDOW",return_from_game_overview)

def return_from_game_overview():
    game_overview_window.destroy()
    window.update()
    window.deiconify()

#----------def start_play_button():-----------
#this where the function will be called for the game
#--------------------------------------------
play_button = Button(button_frame, 
                    text= "Play",
                    font=('Courier', 20, 'bold'),
                    bg="#FF8C00",            
                    fg="#FFF5CC",            
                    activebackground="#4B0082",
                    activeforeground="#00FFFF" 
                    
)
play_button.grid(row=1, column=1, pady=10)

game_overview_button = Button(button_frame, 
                    text= "Game Overview",
                    font=('Courier', 20, 'bold'),
                    bg="#FF8C00",            
                    fg="#FFF5CC",            
                    activebackground="#4B0082",
                    activeforeground="#00FFFF",
                    command= game_overview             
)
game_overview_button.grid(row=3, column=1, pady=10)


#--------credits---------------


def credits():
    global credits_window
    window.withdraw()

    credits_window = Toplevel(window, bg="#3A0066")
    credits_window.geometry("700x700")

    for col in range(3):
        credits_window.columnconfigure(col, weight=1)
        credits_window.rowconfigure(1, weight=1)

    # Title (top center)
    Label(credits_window,
          text="Credits",
          bg="#3A0066",
          fg="#FFF5CC",
          font=('Courier', 45)
    ).grid(row=0, column=1)

    # Credits text (center)
    Label(credits_window,
          text="""Game Design & Development:
Aidan 
Bartek 

Concept & Idea:
Aidan, Bartek, Vishy

Graphics & UI:
Vish

Special Thanks:
Aimee for being the GOAT as usual
""",
          bg="#3A0066",
          fg="#FFF5CC",
          justify="center",
          font=('Courier', 13)
    ).grid(row=1, column=1)

    # Go Back button (bottom center)
    go_back_menu = Button(
        credits_window,
        font="Courier",
        text="GO BACK",
        bg="#FF8C00",
        fg="#FFF5CC",
        activebackground="#4B0082",
        activeforeground="#00FFFF",
        command=return_from_credits
    )
    go_back_menu.grid(row=2, column=1, sticky='s', pady=20)

    credits_window.protocol("WM_DELETE_WINDOW", return_from_credits)

credits_button = Button(button_frame, 
                    text= "Credits",
                    font=('Courier', 20, 'bold'),
                    bg="#FF8C00",            
                    fg="#FFF5CC",            
                    activebackground="#4B0082",
                    activeforeground="#00FFFF",
                    command= credits

)
credits_button.grid(row=2, column=1, pady=10)

def return_from_credits():
    credits_window.destroy()
    window.update()
    window.deiconify()


#-------------------quit window function-----------------
def quit_window():
    window.withdraw()

quit_button = Button(button_frame, 
                    text= "Quit",
                    font=('Courier', 20, 'bold'),
                    bg="#FF8C00",            
                    fg="#FFF5CC",            
                    activebackground="#4B0082",
                    activeforeground="#00FFFF",
                    command= quit_window             
)
quit_button.grid(row=4, column=1, pady=10)

#---------button animation---------

def on_enter(e):
    e.widget.config(bg="#FFD166", fg="#3A0066")

def on_leave(e):
    e.widget.config(bg="#FF8C00", fg="#FFF5CC")

for btn in [play_button, game_overview_button, credits_button, quit_button]:
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)


window.mainloop()



