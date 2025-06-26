#2.0.0
import grabber
import os
import sys
import tempfile
import threading
import tkinter as tk
import winsound as ws
from downloader import EmojiDownloader
from tkinter import filedialog, PhotoImage, ttk


class EmojiDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DC Emoji Downloader")
        self.root.geometry("400x250")
        self.root.configure(background="#36393f")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.exit_program)
        
        center_window(self.root, 400, 250)

        self.server_id = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.folder = None
        self.usertoken = None
        self.accounts = grabber.get_token()

        self.content_frame = tk.Frame(self.root, bg="#36393f")
        self.content_frame.pack(expand=True, fill="both")

        self.handle_token_setup()

    def clear_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def handle_token_setup(self):
        if "NUITKA_ONEFILE_PARENT" in os.environ:
            splash_filename = os.path.join(
                tempfile.gettempdir(),
                "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
                )
            if os.path.exists(splash_filename):
                os.unlink(splash_filename)

        self.clear_frame()
        self.root.iconphoto(False, PhotoImage(file="assets/icon.png"))
        if self.accounts['unique'] < 1:
            ws.PlaySound('SystemAsterisk', 0)
            self.show_token_input("Couldn't detect your UserToken. Please enter it manually.")
        elif self.accounts['unique'] == 1:
            self.usertoken = [list(self.accounts['accounts'].values())[0]['token']]
            self.show_main_ui()
        else:
            self.show_account_selector(self.accounts["accounts"])

    def show_token_input(self, message):
        tk.Label(self.content_frame, text=message, fg="white", bg="#36393f", wraplength=350).pack(pady=(20, 10))
        entry = tk.Entry(self.content_frame, show="*")
        entry.pack()

        def confirm():
            token = entry.get().strip()
            if not token:
                self.exit_program()
            elif not grabber.HazardTokenGrabberV2().checkToken(token):
                ws.PlaySound('SystemAsterisk', 0)
                self.show_token_input("Invalid Token. Please enter a valid UserToken.")
            else:
                self.usertoken = [token]
                self.show_main_ui()

        tk.Button(self.content_frame, text="Confirm", command=confirm, bg="#5865f2", fg="white").pack(pady=10)

    def show_account_selector(self, accounts: dict):
        tk.Label(self.content_frame, text="Please choose your Discord account:", fg="white", bg="#36393f").pack(pady=(25, 5))
        options = [f"{data['display_name']} ({uid})" for uid, data in accounts.items()]
        combo = ttk.Combobox(self.content_frame, values=options, state="readonly", width=45)
        combo.current(0)
        combo.pack()

        def confirm():
            choice = combo.get()
            if not choice:
                return
            uid = choice.split("(")[-1].rstrip(")")
            self.usertoken = [accounts[uid]["token"]]
            self.show_main_ui()

        tk.Button(self.content_frame, text="Confirm", command=confirm, bg="#5865f2", fg="white").pack(pady=10)

    def show_main_ui(self):
        self.clear_frame()
        self.select_folder()
        if not self.folder:
            self.exit_program()

        tk.Label(self.content_frame, text="Discord Server ID:", fg="white", bg="#36393f").place(relx=0.1, rely=0.2)
        tk.Entry(self.content_frame, textvariable=self.server_id).place(relx=0.5, rely=0.2)
        
        self.status_label = tk.Label(self.content_frame, textvariable=self.status_text, fg='#35bf25', bg="#36393f", font="-family {Segoe UI} -size 10")
        self.status_label.place(relx=0.1, rely=0.5, relwidth=0.8)

        self.download_button = tk.Button(self.content_frame, text="Download", bg="#5865f2", fg="white", command=self.start_download)
        self.download_button.place(relx=0.4, rely=0.7)

        self.root.after(100, lambda: self.root.focus_force())

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

    def exit_program(self):
        self.root.quit()
        self.root.destroy()
        sys.exit(0)


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
