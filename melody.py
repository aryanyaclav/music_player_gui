from tkinter import *
import tkinter.messagebox
from pygame import mixer
from tkinter import filedialog
import os
from mutagen.mp3 import MP3
import time
import threading
from tkinter import ttk
from ttkthemes import themed_tk as tk

root = tk.ThemedTk()
root.get_themes()
root.set_theme("radiance")

statusbar = ttk.Label(root,text="welcome to AMP",relief=  SUNKEN, anchor=W,font="Times 10 bold")
statusbar.pack(side= BOTTOM, fill=X)

menubar = Menu(root)
root.config(menu=menubar)

submenu = Menu(menubar,tearoff=0)


playlist = []

def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index,filename_path)
    index+=1

menubar.add_cascade(label="file",menu=submenu)
submenu.add_command(label="open",command= browse_file)
submenu.add_command(label='exit',command=root.destroy)

def about_us():
    tkinter.messagebox.showinfo("AMP-Aryan's Music Player",'Music player,Built using python')

submenu = Menu(menubar,tearoff=0)
menubar.add_cascade(label="Help",menu=submenu)
submenu.add_command(label="about us",command= about_us)

mixer.init() #iitializigthemixture

root.title("AMP")

root.iconbitmap(r'melody.ico')

leftframe= Frame(root)
leftframe.pack(side=LEFT,padx=30,pady=30)

playlistbox =Listbox(leftframe)
playlistbox.pack()

addbtn = ttk.Button(leftframe,text="+ Add",command=browse_file)
addbtn.pack(side=LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

delbtn = ttk.Button(leftframe,text="- Del",command=del_song)
delbtn.pack(side=LEFT)

rightframe= Frame(root)
rightframe.pack(pady=30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label(topframe,text='total length - --:--')
lengthlabel.pack(pady=10)

currentTimeLabel = ttk.Label(topframe,text='current Time - --:--',relief=GROOVE)
currentTimeLabel.pack()

def show_details(play_song):
    file_data = os.path.splitext(play_song)

    if file_data[1]== '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    mins,secs = divmod(total_length,60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = "Total Length" +"-"+ timeformat

    t1 = threading.Thread(target=start_count,args=(total_length,))
    t1.start()

def start_count(t):
    global paused
    while t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(t, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            currentTimeLabel['text'] = 'Current Time -' + timeformat
            time.sleep(1)
            t-=1


def play_Music():
    global paused
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "music Resumed"
        paused=FALSE
    else:
        try:
            stop_Music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "playing Music" + " " + os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('file not found', 'please select a file')




def stop_Music():
    mixer.music.stop()
    statusbar['text'] = "music stopped"

def set_vol(val):
    volume =  float(val)/100
    mixer.music.set_volume(volume) #only takes from 0 to 1

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = 'music paused'

def rewind_music():
    play_Music()
    statusbar['text']="music rewinded"

muted= FALSE

def mute_music():
    global muted
    if muted:
        mixer.music.set_volume(0.7)
        scale.set(70)
        volumebtn.configure(image=volumephoto)
        muted = FALSE
    else:
        mixer.music.set_volume(0)
        scale.set(0)
        volumebtn.configure(image=mutephoto)
        muted = TRUE

middleFrame = Frame(rightframe)
middleFrame.pack(padx=10,pady=30)

bottomframe = Frame(rightframe)
bottomframe.pack(padx=5,pady=5)

mutephoto= PhotoImage(file='images/mute.png')
volumephoto = PhotoImage(file='images/volume.png')
volumebtn= ttk.Button(bottomframe ,image=volumephoto,command=mute_music)
volumebtn.grid(row=0,column=1,padx=8)


playphoto = PhotoImage(file='images/play.png')
playbtn = ttk.Button(middleFrame,image=playphoto,command=play_Music)
playbtn.grid(row=0,column=0,padx=8)

stopphoto = PhotoImage(file='images/stop.png')
stopbtn = ttk.Button(middleFrame,image=stopphoto,command=stop_Music)
stopbtn.grid(row=0,column=1,padx=8)

pausephoto = PhotoImage(file='images/pause.png')
pausebtn = ttk.Button(middleFrame,image=pausephoto,command= pause_music)
pausebtn.grid(row=0,column=2,padx=8)

rewindphoto= PhotoImage(file='images/rewind.png')
rewindbtn = ttk.Button(bottomframe,image=rewindphoto,command=rewind_music)
rewindbtn.grid(row=0,column=0)

scale = ttk.Scale(bottomframe,from_=0,to=100,orient=HORIZONTAL,command=set_vol)
scale.set(70)
mixer.music.set_volume(0.7)
scale.grid(row=0,column=2,padx=15)





def on_closing():
    stop_Music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW",on_closing)
root.mainloop()