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
        self.root.withdraw()

        self.server_id = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready")
        self.folder = None
        self.usertoken = None
        self.accounts = grabber.get_token()

        self.content_frame = tk.Frame(self.root, bg="#36393f")
        self.content_frame.pack(expand=True, fill="both")

        self.handle_token_setup()

    def clear_frame(self):
        """
        Destroy all widgets in the content frame.

        Behavior:
            - Iterates through all child widgets of self.content_frame and destroys them.
            - Effectively clears the frame for new content to be added.
        """
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def handle_token_setup(self):
        """
        Handles the setup process for the user's Discord token.

        - If running as a Nuitka onefile executable, removes the splash feedback file if present.
        - Clears the current content frame and sets the application icon.
        - If no user tokens are detected, prompts the user to enter a token manually.
        - If exactly one user token is detected, sets it and proceeds to the main UI.
        - If multiple user tokens are detected, prompts the user to select an account.
        """
        if "NUITKA_ONEFILE_PARENT" in os.environ:
            splash_filename = os.path.join(
                tempfile.gettempdir(),
                "onefile_%d_splash_feedback.tmp" % int(os.environ["NUITKA_ONEFILE_PARENT"]),
                )
            if os.path.exists(splash_filename):
                os.unlink(splash_filename)

        self.clear_frame()
        self.root.iconphoto(False, PhotoImage(file=get_resource_path(os.path.join("assets", "icon.png"))))
        if self.accounts['unique'] < 1:
            ws.PlaySound('SystemAsterisk', 0)
            self.show_token_input("Couldn't detect your UserToken. Please enter it manually.")
        elif self.accounts['unique'] == 1:
            self.usertoken = [list(self.accounts['accounts'].values())[0]['token']]
            self.show_main_ui()
        else:
            self.show_account_selector(self.accounts["accounts"])

    def show_token_input(self, message):
        """
        Display a prompt for the user to manually enter their Discord user token.

        Args:
            message (str): The message to display above the token entry field.

        Behavior:
            - Shows a label with the provided message.
            - Provides a password-style entry box for the token.
            - On confirmation:
                - If the entry is empty, exits the program.
                - If the token is invalid, plays a sound and prompts again.
                - If the token is valid, stores it and proceeds to the main UI.
        """
        tk.Label(self.content_frame, text=message, fg="white", bg="#36393f", wraplength=350).pack(pady=(20, 10))
        entry = tk.Entry(self.content_frame, show="*")
        entry.pack()

        def confirm():
            """
            Handle the confirmation of the entered token.

            - Retrieves and validates the token.
            - Exits if empty.
            - Prompts again if invalid.
            - Proceeds if valid.
            """
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
        """
        Display a selector for the user to choose among multiple detected Discord accounts.

        Args:
            accounts (dict): A dictionary mapping user IDs to account data, where each value contains
                             at least 'display_name' and 'token' keys.

        Behavior:
            - Shows a label prompting the user to select an account.
            - Displays a combobox listing all available accounts by display name and user ID.
            - On confirmation:
                - Retrieves the selected account's user ID.
                - Sets the user token for the selected account.
                - Proceeds to the main UI.
        """
        tk.Label(self.content_frame, text="Please choose your Discord account:", fg="white", bg="#36393f").pack(pady=(25, 5))
        options = [f"{data['display_name']} ({uid})" for uid, data in accounts.items()]
        combo = ttk.Combobox(self.content_frame, values=options, state="readonly", width=45)
        combo.current(0)
        combo.pack()

        def confirm():
            """
            Handle the confirmation of the selected account.

            - Retrieves the selected account from the combobox.
            - If no selection is made, does nothing.
            - Otherwise, extracts the user ID, sets the corresponding user token,
              and proceeds to the main UI.
            """
            choice = combo.get()
            if not choice:
                return
            uid = choice.split("(")[-1].rstrip(")")
            self.usertoken = [accounts[uid]["token"]]
            self.show_main_ui()

        tk.Button(self.content_frame, text="Confirm", command=confirm, bg="#5865f2", fg="white").pack(pady=10)

    def show_main_ui(self):
        """
        Display the main user interface for downloading Discord emojis and stickers.

        Behavior:
            - Prompts the user to select a folder for saving emojis/stickers.
            - If no folder is selected, exits the program.
            - Displays input for Discord Server ID.
            - Shows a status label for feedback.
            - Provides a Download button to start the download process.
            - Ensures the window is focused after setup.
        """
        self.select_folder()
        if not self.folder:
            self.exit_program()
        self.root.deiconify()

        tk.Label(self.content_frame, text="Discord Server ID:", fg="white", bg="#36393f").place(relx=0.1, rely=0.2)
        tk.Entry(self.content_frame, textvariable=self.server_id).place(relx=0.5, rely=0.2)
        
        self.status_label = tk.Label(self.content_frame, textvariable=self.status_text, fg='#35bf25', bg="#36393f", font="-family {Segoe UI} -size 10")
        self.status_label.place(relx=0.1, rely=0.5, relwidth=0.8)

        self.download_button = tk.Button(self.content_frame, text="Download", bg="#5865f2", fg="white", command=self.start_download)
        self.download_button.place(relx=0.4, rely=0.7)

        self.root.after(100, lambda: self.root.focus_force())

    def start_download(self):
        """
        Initiates the download process for emojis and stickers.

        Behavior:
            - Disables the Download button to prevent multiple clicks.
            - Starts a new thread to fetch and download guild data asynchronously.
        """
        self.download_button.config(state='disabled')
        threading.Thread(target=self.get_guild_data).start()

    def get_guild_data(self):
        """
        Fetches and downloads emojis and stickers from the specified Discord server.

        Behavior:
            - Retrieves the server ID from the input field and validates it.
            - If the server ID is invalid (not all digits), updates the status with an error and re-enables the Download button.
            - If valid, creates an EmojiDownloader instance and updates the status to "Downloading...".
            - Attempts to download emojis and stickers using the downloader.
                - On success, updates the status with the number of items downloaded and the server name.
                - On failure, updates the status with the error message.
            - Re-enables the Download button after completion.

        Exceptions:
            - Catches and displays any exceptions raised during the download process.
        """
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
        """
        Update the status label in the UI with a given message.

        Args:
            message (str): The status message to display.
            error (bool, optional): If True, displays the message in an error color. Defaults to False.

        Behavior:
            - Sets the status text to the provided message.
            - Changes the label color to red if error is True, otherwise green.
        """
        self.status_text.set(message)
        self.status_label.configure(fg='#e21223' if error else '#35bf25')

    def select_folder(self):
        """
        Prompt the user to select a directory for saving emojis and stickers.

        Behavior:
            - Opens a folder selection dialog.
            - Sets the selected folder path to self.folder.
        """
        self.folder = filedialog.askdirectory(title='Select the folder where your emojis should be saved.')

    def exit_program(self):
        """
        Cleanly exit the application.

        Behavior:
            - Quits the Tkinter main loop.
            - Destroys the root window.
            - Exits the Python process with status code 0.
        """
        self.root.quit()
        self.root.destroy()
        sys.exit(0)


def center_window(window, width, height):
    """
    Center the given window on the screen.

    Args:
        window (tk.Tk or tk.Toplevel): The window to center.
        width (int): The width of the window.
        height (int): The height of the window.

    Behavior:
        - Calculates the position to center the window based on the screen size.
        - Sets the geometry of the window so it appears centered.
    """
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def get_resource_path(filename: str):
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, filename)
    else:
        return os.path.join(os.path.dirname(__file__), filename)

def main():
    root = tk.Tk()
    app = EmojiDownloaderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
