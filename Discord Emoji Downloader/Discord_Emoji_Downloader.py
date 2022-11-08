#1.2.1
from tkinter import filedialog, Tk
import Discord_Emoji_Downloader_support
import winsound as ws
import tkinter as tk
import requests
import sys
import os
import Grabber


root = Tk()
root.withdraw()
root.attributes('-topmost', True)


#def find_tokens():
#    tokens = []
#    tokens.append(Grabber.get_token())
#    return tokens


def main():
    global userid
    userid = Grabber.get_token()
    if userid == []:   
        ws.PlaySound('SystemAsterisk', 0)
        userid = tk.simpledialog.askstring("DC Emoji Downloader", "Couldn't detect your UserToken. Please enter it manually.")



if __name__ == '__main__':
    main()

def folderselect():
    global folder
    folder = filedialog.askdirectory(title='Select the folder where your emojis should be saved. A folder with the servers name will be created automatically.')
    if folder == '':
        folderselect()
folderselect()
    

def downloader():
    global servername
    disallowed_characters = '\/:*?"<>|'
    for character in disallowed_characters:
        servername = servername.replace(character,"")

    if not os.path.exists(os.path.join(folder,servername)):
        os.mkdir(os.path.join(folder,servername))
    downloadfolder = os.path.join(folder,servername)

    def download(self,filename):
        link = requests.get(self)
        with open(filename, 'wb') as f:
            f.write(link.content)
            
    for event in data:
        emojiid = event['id']
        animated = event['animated']
        if animated == True:
            emojiurl = "https://cdn.discordapp.com/emojis/"+emojiid+'.gif'
            emoji = os.path.join(downloadfolder,event['name']+'.gif')
        else:
            emojiurl = "https://cdn.discordapp.com/emojis/"+emojiid+'.png'
            emoji = os.path.join(downloadfolder,event['name']+'.png')
        download(emojiurl,emoji)


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

class MainWindow:
    def __init__(self, top=None):
        def validate():
            try:
                if 'Unknown Guild' in data['message']:
                    return 'error'
            except:
                return 'ok'
        def validate2():
            try:
                if 'snowflake' in data['guild_id']:
                    return 'error'
            except:
                return 'ok'


        def getID():
            tk.messagebox.showinfo("DC Emoji Downloader", "The download will now start.\nDuring that time the window will freeze.\nJust wait until it's done.")
            global servername
            global data
            guildid = self.ServerID.get()
            guildurl = "https://discord.com/api/v6/guilds/"+guildid
            url = "https://discord.com/api/v6/guilds/"+guildid+"/emojis"
            for entry in userid:
                headers = {'authorization': entry}
                nameresponse = requests.get(guildurl, headers=headers)
                response = requests.get(url, headers=headers)
                namedata = nameresponse.json()
                data = response.json()
                if "{'message': 'Missing Access', 'code': 50001}" in str(data):
                    continue
                else:
                    self.Status.configure(text='Downloading...')
                    break
            test = format(validate())
            test2 = format(validate2())


            if test != test2:
                self.Status.configure(font="-family {Segoe UI} -size 16")
                self.Status.configure(foreground='#e21223')
                self.Status.configure(text="That's not a valid ServerID!")
                return
                            

            servername = namedata['name']
            downloader()
            self.Status.configure(foreground='#35bf25')
            self.Status.configure(font="-family {Segoe UI} -size 10")
            self.Status.configure(text='Downloaded all Emojis from\n'+servername)


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
        self.Download.configure(command=getID)

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
    vp_start_gui()
