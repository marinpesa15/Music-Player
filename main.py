from tkinter import *
from tkinter import ttk, filedialog, messagebox
from PIL import Image, ImageTk
import pygame
import tkinter.font as tkfont

# initialize the window
WIDTH, HEIGHT = 1000, 500
root = Tk()
root.geometry(f"{WIDTH}x{HEIGHT}")
root.title("Music Player")
root.resizable(False, False)
FONT = tkfont.Font(family="Halvetica", size=12, weight="normal", slant="italic")
pygame.mixer.init()

# add song to the playlist
def add_song():
    songs = filedialog.askopenfilenames(initialdir="audio/", title="Choose a Song", filetypes=(("mp3 Files", "*.mp3"), ))
    for song in songs:
        song = song.replace("/mnt/c/Users/pesam/Documents/workspace/music_player/audio/", "")
        song = song.replace(".mp3", "")

        song_box.insert(END, song)

# remove selected song from the playlist
def remove_song():
    try:
        song_box.delete(ANCHOR)
    except:
        messagebox.showinfo("Remove Song", "Please choose a song to remove")


# play the chosen song
def play():
    global paused
    global total_duration
    song = song_box.get(ACTIVE)
    song = f"/mnt/c/Users/pesam/Documents/workspace/music_player/audio/{song}.mp3"
    total_duration = pygame.mixer.Sound(song).get_length()

    try:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        progress()
    except:
        messagebox.showinfo("Play Song", "Please Add/Choose a Song to play")

# global paused variable
global paused
paused = False

# pause the chosen song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.pause()
        paused = True

# play the previous song
def previous():
    prev_song = song_box.curselection()
    prev_song = prev_song[0] - 1
    song = song_box.get(prev_song)
    song = f"/mnt/c/Users/pesam/Documents/workspace/music_player/audio/{song}.mp3"

    try:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    except:
        messagebox.showinfo("Previous Song", "No Previous Song to play")

# play the next song
def next():
    next_song = song_box.curselection()
    next_song = next_song[0] + 1
    song = song_box.get(next_song)
    song = f"/mnt/c/Users/pesam/Documents/workspace/music_player/audio/{song}.mp3"

    try:
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    except:
        messagebox.showinfo("Next Song", "No more songs to play. Please add more Songs to playlist")

# volume function
def volume(x):
    pygame.mixer.music.set_volume(volume_bar.get())

def progress():
    current_time = pygame.mixer.music.get_pos() / 1000

    prog = (current_time / total_duration) * 100

    progress_var.set(prog)

    root.after(100, progress)

# control frame
frame = Frame(root, bg="gray", width=400, height=500)
frame.grid(row=0, column=0)

# seperate frame
sep_frame = Frame(root, bg="white", width=50, height=500)
sep_frame.grid(row=0, column=1)

# listbox
song_box = Listbox(root, fg="white", bg="gray", width=62, height=29, activestyle="none", font=FONT)
song_box.place(x=450, y=0)

# song image frame
song_frame = Frame(frame, bg="salmon", width=355, height=200)
song_frame.place(x=20, y=20)

# buttons frame
btn_frame = Frame(frame, bg="gray")
btn_frame.place(x=30, y=240)

# song image
song_img = PhotoImage(file="images/music_logo.png")
song_img_label = Label(song_frame, image=song_img, borderwidth=0)
song_img_label.place(x=70, y=5)

# buttons images
previous_button_img = PhotoImage(file="images/previous.png")
play_button_img = PhotoImage(file="images/play.png")
pause_button_img = PhotoImage(file="images/pause.png")
next_button_img = PhotoImage(file="images/next.png")

# buttons
previous_button = Button(btn_frame, image=previous_button_img, borderwidth=0, highlightthickness=0, bg="gray", activebackground="gray", command=previous)
play_button = Button(btn_frame, image=play_button_img, borderwidth=0, highlightthickness=0, bg="gray", activebackground="gray", command=play)
pause_button = Button(btn_frame, image=pause_button_img, borderwidth=0, highlightthickness=0, bg="gray", activebackground="gray", command=lambda: pause(paused))
next_button = Button(btn_frame, image=next_button_img, borderwidth=0, highlightthickness=0, bg="gray", activebackground="gray", command=next)

previous_button.grid(row=0, column=0)
play_button.grid(row=0, column=1, padx=20)
pause_button.grid(row=0, column=2)
next_button.grid(row=0, column=3, padx=20)

# progress bar
progress_var = DoubleVar()
progress_bar = ttk.Progressbar(orient=HORIZONTAL, variable=progress_var, length=355, mode="determinate")
progress_bar.place(x=20, y=330)

# volume
vol_frame = Frame(frame, bg="gray")
vol_frame.place(x=20, y=375)

mute_img = PhotoImage(file="images/mute.png")
mute_img_label = Label(vol_frame, image=mute_img, borderwidth=0, background="gray")
mute_img_label.grid(row=0, column=0, padx=20)
volume_img = PhotoImage(file="images/volume.png")
volume_img_label = Label(vol_frame, image=volume_img, borderwidth=0, background="gray")
volume_img_label.grid(row=0, column=2, padx=20)

volume_bar = ttk.Scale(vol_frame, orient=HORIZONTAL, from_=0, to=1, length=237, value=0.5, command=volume)
volume_bar.grid(row=0, column=1)

# add / remove songs
add_song_img = PhotoImage(file="images/add_song.png")
remove_song_img = PhotoImage(file="images/remove_song.png")
add_song_btn = Button(frame, image=add_song_img, borderwidth=0, highlightthickness=0, bg="gray", activebackground="gray", command=add_song)
add_song_btn.place(x=120, y=430)
remove_song_btn = Button(frame, image=remove_song_img, borderwidth=0, highlightthickness=0, bg="gray", activebackground="gray", command=remove_song)
remove_song_btn.place(x=235, y=430)

# main loop
root.mainloop()

