from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"

# -------------------- CARDS CONFIG ------------------------- #

current_card = {}
to_learn = {}

try:
    data = pandas.read_csv("data/words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/french_words.csv")
    print(original_data)
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")


def next_card():
    global current_card, flip_timer
    window.after_cancel(flip_timer)
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_text, text=current_card["French"], fill="black")
    canvas.itemconfig(card, image=front_card)
    flip_timer = window.after(3000, func=flip_card)

# ------------------------FLIP CARD --------------------------#

def flip_card():
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_text, text=current_card["English"], fill="white")
    canvas.itemconfig(card, image =back_card)


def is_known():
    to_learn.remove(current_card)
    print(len(to_learn))
    data = pandas.DataFrame(to_learn)
    data.to_csv("data/words_to_learn.csv", index=False)
    next_card()


# -----------------------UI DESIGN --------------------------#

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_timer = window.after(3000, func=flip_card)


canvas = Canvas(height=528, width=800)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
card = canvas.create_image(400, 264, image = front_card)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 45, "italic"))
card_text = canvas.create_text(400, 264, text="", font=("Ariel", 65, "bold"))
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.grid(row=0, column=0, columnspan=2)

unknown_img = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=unknown_img, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0 )

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=is_known)
known_button.grid(row=1, column=1)


next_card()



window.mainloop()