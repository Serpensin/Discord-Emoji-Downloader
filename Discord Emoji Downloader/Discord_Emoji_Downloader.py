import Discord_Emoji_Downloader_support
from tkinter import simpledialog, filedialog, Tk
import tkinter.ttk as ttk
import winsound as ws
import tkinter as tk
import requests
import sys
import os
import re


root = Tk()
root.withdraw()
root.attributes('-topmost', True)


def find_tokens(path):
    path += '\\Local Storage\\leveldb'
    <
    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')
    global userid

    paths = {
        'Discord': roaming + '\\discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Opera': roaming + '\\Opera Software\\Opera Stable',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
        'Edge': local + '\\Microsoft\\Edge\\User Data\\Default'
    }

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue
        tokenspre = find_tokens(path)
        prefix = 'mfa.'
        token = [x for x in tokenspre if x.startswith(prefix)]

    try:
        userid = token[0]
        print(userid)
    except:
        ws.PlaySound('SystemAsterisk', 0)
        answer = tk.simpledialog.askstring("DC Emoji Downloader", "Couldn't detect your UserToken. Please enter it manually.")
        if not answer.startswith('mfa.'):
            main()

if __name__ == '__main__':
    main()


folderselect = filedialog.askdirectory(title='Select the folder where your emojis should be saved. A folder with the servers name will be created automatically.')


def downloader():
    global servername
    disallowed_characters = '\/:*?"<>|'
    for character in disallowed_characters:
        servername = servername.replace(character,"")

    if not os.path.exists(os.path.join(folderselect,servername)):
        os.mkdir(os.path.join(folderselect,servername))
    folder = os.path.join(folderselect,servername)

    def download(self,filename):
        link = requests.get(self)
        with open(filename, 'wb') as f:
            f.write(link.content)

    for event in data:
        emojiid = event['id']
        emojiname = event['name']
        animated = event['animated']
        if animated == True:
            emojiurl = "https://cdn.discordapp.com/emojis/"+emojiid+'.gif'
            emoji = os.path.join(folder,event['name']+'.gif')
        else:
            emojiurl = "https://cdn.discordapp.com/emojis/"+emojiid+'.png'
            emoji = os.path.join(folder,event['name']+'.png')
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
            global servername
            global data
            guildid = self.ServerID.get()
            guildurl = "https://discord.com/api/v6/guilds/"+guildid
            url = "https://discord.com/api/v6/guilds/"+guildid+"/emojis"
            headers = {'authorization': userid}
            nameresponse = requests.get(guildurl, headers=headers)
            response = requests.get(url, headers=headers)
            namedata = nameresponse.json()
            data = response.json()
            print(data)
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
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'

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
