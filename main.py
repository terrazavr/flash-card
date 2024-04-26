from tkinter import *
from gtts import gTTS
import os
import pandas
import playaudio
import random


BACKGROUND_COLOR = "#B1DDC6"
current_word = {}
words_dict = {}


try:
    data = pandas.read_csv("data/to-learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("data/eng_words.csv")
    words_dict = original_data.to_dict(orient="records")
else:
    words_dict = data.to_dict(orient="records")


# ---------------------------- Functions for cards ------------------------------- #
def next_card():
    """Shows a new card with a new random word, and after 3 sec,
    it shows the card with translation. After pressing any button,
    the func restarts and opens new card."""
    language = "en"
    global current_word, flip_timer
    window.after_cancel(flip_timer)
    current_word = random.choice(words_dict)
    canvas.itemconfig(card_title, text="English", fill="black")
    canvas.itemconfig(word, text=current_word["English"], fill="black")
    canvas.itemconfig(transcription, text=current_word["Transcription"], fill="black")
    canvas.itemconfig(canvas_image, image=front_card)

    audio_output = gTTS(text=current_word["English"], lang=language)
    audio_output.save("english_word.mp3")
    playaudio.playaudio("english_word.mp3", True)
    os.remove("english_word.mp3")
    window.after(3000, flip_card)


def flip_card():
    """Flips the current card and shows the translation of the word."""
    canvas.itemconfig(canvas_image, image=back_card)
    canvas.itemconfig(card_title, text="Русский", fill="white")
    canvas.itemconfig(word, text=current_word["Русский"], fill="white")
    canvas.itemconfig(transcription, text="")


def is_known():
    """The function removes the card from the word list if a user knows the current word
    and presses the checkmark button, and then open a new card."""
    words_dict.remove(current_word)
    next_card()
    datas = pandas.DataFrame(words_dict)
    datas.to_csv("data/to-learn.csv", index=False)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Flashy")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# timer to flip the card if did not press any the button
flip_timer = window.after(3000, flip_card)

# Card interface
canvas = Canvas(width=800, height=530, bg=BACKGROUND_COLOR, highlightthickness=0)
front_card = PhotoImage(file="images/card_front.png")
back_card = PhotoImage(file="images/card_back.png")
canvas_image = canvas.create_image(400, 275, image=front_card)

card_title = canvas.create_text(400, 110, text="", font=("Courier New", 60))
word = canvas.create_text(400, 270, text="", font=("Courier New", 65, "bold", "underline"))
transcription = canvas.create_text(400, 390, text="", font=("Courier", 40))

canvas.grid(column=0, row=0, columnspan=2)

# Buttons
right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightbackground=BACKGROUND_COLOR, command=next_card)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightbackground=BACKGROUND_COLOR, command=is_known)
wrong_button.grid(column=0, row=1)


next_card()

window.mainloop()
