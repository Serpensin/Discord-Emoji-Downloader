#1.4
import Discord_Emoji_Downloader_support
import Grabber
import os
import requests
import sys
import tkinter as tk
import threading
import winsound as ws
from apnggif import apnggif
from tkinter import filedialog, Tk


root = Tk()
root.withdraw()
root.attributes('-topmost', True)
disallowed_characters = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

def downloader(self):
    def download(self,full_path):
        link = requests.get(self)
        filename = os.path.basename(full_path)

        for character in disallowed_characters:
            filename = filename.replace(character, '')
        new_full_path = os.path.join(os.path.dirname(full_path), filename)

        with open(new_full_path, 'wb') as f:
            f.write(link.content)
        return new_full_path

    def convert_apng_to_gif(input_path, output_path):
        apnggif(input_path, output_path)

    global servername
    for character in disallowed_characters:
        servername = servername.replace(character,"")

    count_total = len(data_emoji) + len(data_sticker)
    count = 0

    if count_total > 0:
        self.Status.configure(text=f'Downloaded {count}/{count_total}')
    elif count_total == 0:
        self.Status.configure(text='No Emojis or Stickers found')
        return False

    if data_emoji != []:
        os.makedirs(os.path.join(folder, servername, "Emojis"), exist_ok=True)
        for event in data_emoji:
            emojiid = event['id']
            animated = event['animated']
            if animated == True:
                emojiurl = "https://cdn.discordapp.com/emojis/"+emojiid+'.gif'
                emoji = os.path.join(folder, servername, "Emojis", event['name']+'.gif')
            else:
                emojiurl = "https://cdn.discordapp.com/emojis/"+emojiid+'.png'
                emoji = os.path.join(folder, servername, "Emojis", event['name']+'.png')
            download(emojiurl,emoji)
            count += 1
            self.Status.configure(text=f'Downloaded {count}/{count_total}')

    if data_sticker != []:
        os.makedirs(os.path.join(folder, servername, "Stickers"), exist_ok=True)
        for event in data_sticker:
            stickerid = event['id']
            format_type = event['format_type']
            if format_type == 1 or format_type == 2:
                stickerurl = "https://cdn.discordapp.com/stickers/"+stickerid+'.png'
                sticker = os.path.join(folder, servername, "Stickers", event['name']+'.png')
            elif format_type == 4:
                stickerurl = "https://media.discordapp.net/stickers/"+stickerid+'.gif'
                sticker = os.path.join(folder, servername, "Stickers", event['name']+'.gif')
            new_path = download(stickerurl,sticker)
            if format_type == 2:
                convert_apng_to_gif(new_path, new_path.replace('.png', '.gif'))
                os.remove(new_path)
            count += 1
            self.Status.configure(text=f'Downloaded {count}/{count_total}')
    return count


def exitProgram():
    sys.exit()


def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    top = MainWindow (root)
    Discord_Emoji_Downloader_support.init(root, top)

    root.mainloop()

w = None
def create_MainWindow(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_MainWindow(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    top = MainWindow (w)
    Discord_Emoji_Downloader_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_MainWindow():
    global w
    w.destroy()
    w = None

class MainWindow():
    def __init__(self, top=None):
        def isValidGuild():
            if not self.ServerID.get().isdigit():
                return False
            elif type(data_emoji) == list:
                return True
            try:
                if data_emoji.get('code') == 10004:
                    return False
            except KeyError:
                return True

        def getID():
            global servername, data_emoji, data_sticker
            guildid = self.ServerID.get()
            url_guild = f"https://discord.com/api/v6/guilds/{guildid}"
            url_emoji = f"https://discord.com/api/v6/guilds/{guildid}/emojis"
            url_sticker = f"https://discord.com/api/v6/guilds/{guildid}/stickers"
            for entry in usertoken:
                headers = {'authorization': entry}
                nameresponse = requests.get(url_guild, headers=headers)
                response_emoji = requests.get(url_emoji, headers=headers)
                response_stickers = requests.get(url_sticker, headers=headers)

                namedata = nameresponse.json()
                data_emoji = response_emoji.json()
                data_sticker = response_stickers.json()
                if "{'message': 'Missing Access', 'code': 50001}" in str(data_emoji) or "{'message': 'Missing Access', 'code': 50001}" in str(data_sticker):
                    self.Status.configure(text='Missing Access')
                    break
                else:
                    if not isValidGuild():
                        self.Status.configure(font="-family {Segoe UI} -size 16")
                        self.Status.configure(foreground='#e21223')
                        self.Status.configure(text="That's not a valid ServerID!")
                        break
                    self.Status.configure(font="-family {Segoe UI} -size 10")
                    self.Status.configure(foreground='#35bf25')
                    self.Status.configure(text='Downloading...')
                    servername = namedata['name']
                    downloaded = downloader(self)
                    if not downloaded:
                        self.Status.configure(text='No Emojis or Stickers found')
                    else:
                        self.Status.configure(foreground='#35bf25')
                        self.Status.configure(font="-family {Segoe UI} -size 10")
                        self.Status.configure(text=f'Downloaded {downloaded} Emojis and Stickers from\n'+servername)
                    break
            self.Download.configure(state='normal')
            self.ServerID.configure(state='normal')

        def thread():
            self.Download.configure(state='disabled')
            self.ServerID.configure(state='disabled')
            threading.Thread(target=getID).start()

        #'''This class configures and populates the toplevel window.
        #   top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'

        top.geometry("309x144+993+452")
        top.minsize(120, 1)
        top.maxsize(5764, 2141)
        top.resizable(0,  0)
        top.attributes('-topmost', True)
        top.title("DC Emoji Downloader")
        top.configure(background="#36393f")
        top.configure(highlightbackground="#d9d9d9")
        top.configure(highlightcolor="black")
        top.protocol("WM_DELETE_WINDOW", exitProgram)

        self.ServerID = tk.Entry(top)
        self.ServerID.place(relx=0.392, rely=0.16, height=20, relwidth=0.498)
        self.ServerID.configure(background="white")
        self.ServerID.configure(disabledforeground="#a3a3a3")
        self.ServerID.configure(font="TkFixedFont")
        self.ServerID.configure(foreground="#000000")
        self.ServerID.configure(highlightbackground="#d9d9d9")
        self.ServerID.configure(highlightcolor="black")
        self.ServerID.configure(insertbackground="black")
        self.ServerID.configure(selectbackground="blue")
        self.ServerID.configure(selectforeground="white")

        self.Label1 = tk.Label(top)
        self.Label1.place(relx=0.065, rely=0.16, height=19, width=88)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(activeforeground="black")
        self.Label1.configure(background="#36393f")
        self.Label1.configure(disabledforeground="#a3a3a3")
        self.Label1.configure(foreground="#ffffff")
        self.Label1.configure(highlightbackground="#d9d9d9")
        self.Label1.configure(highlightcolor="black")
        self.Label1.configure(text='''Discord ServerID''')

        self.Download = tk.Button(top)
        self.Download.place(relx=0.291, rely=0.694, height=34, width=137)
        self.Download.configure(activebackground="#1120d5")
        self.Download.configure(activeforeground="white")
        self.Download.configure(activeforeground="#ffffff")
        self.Download.configure(background="#5865f2")
        self.Download.configure(disabledforeground="#a3a3a3")
        self.Download.configure(foreground="#ffffff")
        self.Download.configure(highlightbackground="#d9d9d9")
        self.Download.configure(highlightcolor="black")
        self.Download.configure(pady="0")
        self.Download.configure(text='''Download''')
        self.Download.configure(command=thread)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Status = tk.Message(top)
        self.Status.place(relx=0.065, rely=0.347, relheight=0.299, relwidth=0.874)

        self.Status.configure(background="#36393f")
        self.Status.configure(font="-family {Segoe UI} -size 14")
        self.Status.configure(foreground='#35bf25')
        self.Status.configure(highlightbackground="#36393f")
        self.Status.configure(highlightcolor="black")
        self.Status.configure(text='Ready')
        self.Status.configure(width=270)


if __name__ == '__main__':
    global userid
    usertoken = Grabber.get_token()
    print(usertoken)
    if usertoken == []:
        ws.PlaySound('SystemAsterisk', 0)
        usertoken = tk.simpledialog.askstring("DC Emoji Downloader", "Couldn't detect your UserToken. Please enter it manually.")

    def folderselect():
        global folder
        folder = filedialog.askdirectory(title='Select the folder where your emojis should be saved. A folder with the servers name will be created automatically.')
        if folder == '':
            folderselect()

    folderselect()
    vp_start_gui()
