"""Emoji Keyboard GUI for Book Recommendation System
This module creates a GUI for users to input emojis and get book recommendations based on their selections."""

import emoji
import tkinter as tk
from ..utils.query import process_query
import argparse
import gdown
import zipfile
import os


def main():
    """Main function to run the Emoji Keyboard GUI."""
    # main ideas from https://www.youtube.com/watch?v=8Tlqb14NvY8

    # download and unzip dataset if not already in data folder
    url = "https://drive.google.com/file/d/1Ai0rmMPnyJHcP1bTdFm0T89-UMJ3uOK_/view?usp=sharing"
    zip_path = "data.zip"
    extract_dir = "data/"

    if not os.path.exists(zip_path):
        gdown.download(url, zip_path, quiet=False)

    if not os.path.exists(extract_dir):
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

    emoji_names = [
        "grinning_face",
        "face_with_tears_of_joy",
        "upside-down_face",
        "winking_face",
        "smiling_face_with_hearts",
        "smiling_face_with_heart-eyes",
        "star-struck",
        "smiling_face_with_tear",
        "winking_face_with_tongue",
        "face_with_peeking_eye",
        "thinking_face",
        "shaking_face",
        "cowboy_hat_face",
        "smiling_face_with_sunglasses",
        "nerd_face",
        "astonished_face",
        "flushed_face",
        "crying_face",
        "face_screaming_in_fear",
        "disappointed_face",
        "enraged_face",
        "smiling_face_with_horns",
        "skull",
        "ghost",
        "alien",
        "broken_heart",
        "red_heart",
        "raised_fist",
        "folded_hands",
        "collision",
        "nail_polish",
        "flexed_biceps",
        "child",
        "person",
        "old_woman",
        "health_worker",
        "student",
        "teacher",
        "judge",
        "farmer",
        "cook",
        "mechanic",
        "scientist",
        "technologist",
        "singer",
        "artist",
        "astronaut",
        "firefighter",
        "police_officer",
        "detective",
        "construction_worker",
        "person_in_tuxedo",
        "Santa_Claus",
        "superhero",
        "supervillain",
        "mage",
        "fairy",
        "vampire",
        "zombie",
        "person_running",
        "woman_dancing",
        "person_in_suit_levitating",
        "kiss",
        "family",
        "dog_face",
        "cat_face",
        "horse_face",
        "bear",
        "paw_prints",
        "hatching_chick",
        "dragon_face",
        "T-Rex",
        "fish",
        "hot_beverage",
        "wine_glass",
        "fork_and_knife",
        "world_map",
        "desert_island",
        "mount_fuji",
        "camping",
        "classical_building",
        "stadium",
        "house",
        "office_building",
        "school",
        "castle",
        "night_with_stars",
        "automobile",
        "manual_wheelchair",
        "sailboat",
        "airplane",
        "rocket",
        "rainbow",
        "umbrella_with_rain_drops",
        "snowman_without_snow",
        "water_wave",
        "trophy",
        "water_pistol",
        "performing_arts",
        "necktie",
        "crown",
        "high-heeled_shoe",
        "musical_note",
        "magnifying_glass_tilted_left",
        "crossed_swords",
        "place_of_worship",
        "rainbow_flag",
        "pirate_flag",
    ]

    root = tk.Tk()
    root.title("Emoji Keyboard")
    root.geometry("1200x800")
    font_size = 20
    bg_color = "#FF8FAB"

    # this is the list that will be sent to the other functions
    emoji_input = []
    text_var = tk.StringVar(value="")

    current_dir = os.path.dirname(__file__)  # .../emoji_book_rec/emoji_book_rec/utils/
    two_up = os.path.dirname(os.path.dirname(current_dir))  # .../emoji_book_rec/
    filepath = os.path.join(two_up, "data", "emoji_keyword_list.tsv")

    # on_click functions
    def keyboard_click(emoji_name):
        """Handle emoji button click."""
        current_display = text_var.get()
        text_var.set(current_display + emoji_name)

        emoji_input.append(emoji_name)

        return

    def clear_click():
        """Handle clear button click."""
        text_var.set(" ")
        emoji_input.clear()
        return

# THIS IS THE METHOD OF MAIN WHICH CONNECTS TO THE REST OF THE PIPELINE
    def submit_click():
        """Handle submit button click."""
        # error handling
        if not emoji_input:
            text_var.set("Please enter at least one emoji. Hit \"Clear\" to reset.")
            return
        if len(emoji_input) > 5:
            text_var.set("Please enter no more than 5 emojis. Hit \"Clear\" to reset.")
            return

        text_var.set("SUBMITTED")
        print("Submitted emoji input:", emoji_input)

        # stop further input
        keyboard.pack_forget()
        bottom_buttons.pack_forget()
        output.pack_forget()
        instruction_label.pack_forget()

        # turning the list of emojis back into short_text for use on the back end
        emoji_strings = []
        for e in emoji_input:
            short_text = emoji.demojize(e)
            # remove colons on either side
            emoji_strings.append(short_text[1:-1])

        # process_query returns a full sorted dictionary
        # key=book title, value=book relevance score
        book_recs = process_query(emoji_strings, filepath, True, "emoji_book_rec/data/keyword_book_matrix.tsv")

        key_iter = iter(book_recs)
        book1 = next(key_iter, None)
        book2 = next(key_iter, None)
        book3 = next(key_iter, None)
        book4 = next(key_iter, None)
        book5 = next(key_iter, None)

        # reveal results frame!
        results_frame.pack(fill="both", expand=True)
        results_label_header.config(text=f"Top 5 books recommended for: {' '.join(emoji_input)}")
        results_label1.config(text=f"Book 1: {book1[0]}")
        results_label2.config(text=f"Book 2: {book2[0]}")
        results_label3.config(text=f"Book 3: {book3[0]}")
        results_label4.config(text=f"Book 4: {book4[0]}")
        results_label5.config(text=f"Book 5: {book5[0]}")

    # SETTING UP KEYBOARD GUI
    f1 = tk.Frame(root, background=bg_color)
    f1.pack(fill="both", expand=True, padx=20, pady=20)

    display = tk.Frame(f1, background=bg_color)
    display.pack(side="top", fill="x")

    book_emoji = emoji.emojize(":open_book:")
    instruction_label = tk.Label(
        f1,
        text=f"Enter up to 5 emoji, then hit Submit to get a {book_emoji}",
        font=("Arial", 18, "bold"),
        bg="white",
        fg="black",
    )
    instruction_label.pack(pady=(10, 0))

    output = tk.Label(
        root,
        textvariable=text_var,
        anchor="n",
        bg="white",
        height=3,
        width=30,
        bd=3,
        font=("Arial", 16, "bold"),
        cursor="hand2",
        fg="red",
        padx=15,
        pady=15,
        justify=tk.CENTER,
        relief=tk.RAISED,
        underline=0,
        wraplength=250,
    )
    output.pack(padx=10, pady=10)

    bottom_buttons = tk.Frame(f1, background=bg_color)
    bottom_buttons.pack(side="bottom", padx=10)

    clear_btn = tk.Button(
        bottom_buttons,
        text="Clear",
        font=("", font_size + 2, "bold"),
        width=20,
        height=2,
        cursor="hand2",
        command=lambda: clear_click(),
    )
    clear_btn.pack(side="left", padx=10)
    submit_btn = tk.Button(
        bottom_buttons,
        text="Submit!",
        font=("", font_size + 2, "bold"),
        width=20,
        height=2,
        cursor="hand2",
        command=lambda: submit_click(),
    )
    submit_btn.pack(side="right", padx=10)

    keyboard = tk.Frame(f1, background=bg_color)
    keyboard.pack(fill="both", expand=True, pady=10)

    # frame within keyboard frame (using to center the keys)
    center_frame = tk.Frame(keyboard, background=bg_color)
    center_frame.place(relx=0.5, rely=0.5, anchor="center")  # this centers it

    for i, name in enumerate(emoji_names):
        try:
            e = emoji.emojize(f":{name}:", language="alias")
        except:
            e = name  # if the emoji name is not found
        btn = tk.Button(
            center_frame,
            text=e,
            font=("", font_size),
            width=4,
            height=2,
            command=lambda emoji_name=e: keyboard_click(emoji_name),
        )
        btn.grid(row=i // 12, column=i % 12)

    # setting up results page
    results_frame = tk.Frame(f1, background="white")
    results_label_header = tk.Label(results_frame, text="RESULTS", fg="black", font=("Arial", 24), bg="white")
    results_label1 = tk.Label(
        results_frame, text="Book 1", fg="black", font=("Arial", 20), bg="white", wraplength=500, justify="center"
    )
    results_label2 = tk.Label(
        results_frame, text="Book 2", fg="black", font=("Arial", 20), bg="white", wraplength=500, justify="center"
    )
    results_label3 = tk.Label(
        results_frame, text="Book 3", fg="black", font=("Arial", 20), bg="white", wraplength=500, justify="center"
    )
    results_label4 = tk.Label(
        results_frame, text="Book 4", fg="black", font=("Arial", 20), bg="white", wraplength=500, justify="center"
    )
    results_label5 = tk.Label(
        results_frame, text="Book 5", fg="black", font=("Arial", 20), bg="white", wraplength=500, justify="center"
    )

    # packing all labels
    results_label_header.pack(pady=30)
    results_label1.pack(pady=10)
    results_label2.pack(pady=10)
    results_label3.pack(pady=10)
    results_label4.pack(pady=10)
    results_label5.pack(pady=10)

    # MAIN LOOP STARTS HERE
    root.mainloop()

    return


if __name__ == "__main__":

    main()
