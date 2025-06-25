import imageio
import os
import requests
from PIL import Image

DISALLOWED_CHARACTERS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']

class EmojiDownloader:
    def __init__(self, usertoken, guild_id, folder, update_status_callback):
        self.usertoken = usertoken
        self.guild_id = guild_id
        self.folder = folder
        self.update_status = update_status_callback
        self.servername = ""
        self.data_emoji = []
        self.data_sticker = []

    def download_content(self):
        """
        Downloads all emojis and stickers from the specified Discord guild.

        This method fetches the guild's emoji and sticker data, creates the necessary
        folders for saving the files, and downloads each emoji and sticker to disk.
        The download progress is periodically updated via the provided status callback.

        Returns:
            int: The total number of emojis and stickers downloaded.

        Raises:
            Exception: If access to the guild is missing or no emojis/stickers are found.
        """
        self._fetch_guild_data()
        total_count = len(self.data_emoji) + len(self.data_sticker)
        downloaded_count = 0

        if self.data_emoji:
            self._create_folder("Emojis")
        if self.data_sticker:
            self._create_folder("Stickers")

        for is_emoji, item in (
            [(True, emoji) for emoji in self.data_emoji] +
            [(False, sticker) for sticker in self.data_sticker]
        ):
            if is_emoji:
                self._download_emoji(item)
            else:
                self._download_sticker(item)
            downloaded_count += 1
            if downloaded_count % 5 == 0 or downloaded_count == total_count:
                self.update_status(f'Downloading {downloaded_count}/{total_count}...')

        return downloaded_count

    def _fetch_guild_data(self):
        """
        Fetches the guild's metadata, emojis, and stickers from the Discord API.

        This method iterates through the provided user tokens, attempting to access the specified guild.
        If access is granted, it retrieves the guild's name, emoji list, and sticker list, storing them
        in the corresponding instance variables. If no valid token is found or the guild contains no
        emojis or stickers, an exception is raised.

        Raises:
            Exception: If none of the tokens have access to the guild ("Missing Access").
            Exception: If the guild contains no emojis or stickers ("No Emojis or Stickers found").
        """
        base_url = f"https://discord.com/api/v6/guilds/{self.guild_id}"
        urls = {
            "guild": base_url,
            "emoji": f"{base_url}/emojis",
            "sticker": f"{base_url}/stickers"
        }

        for token in self.usertoken:
            headers = {'authorization': token}
            with requests.Session() as session:
                session.headers.update(headers)
                guild_response = session.get(urls["guild"])
                if guild_response.status_code != 200:
                    continue

                self.servername = guild_response.json().get('name', '')
                emoji_response = session.get(urls["emoji"])
                sticker_response = session.get(urls["sticker"])
                self.data_emoji = emoji_response.json() if emoji_response.status_code == 200 else []
                self.data_sticker = sticker_response.json() if sticker_response.status_code == 200 else []
                break
        else:
            raise Exception("Missing Access")

        if not self.data_emoji and not self.data_sticker:
            raise Exception("No Emojis or Stickers found")

    def _download_emoji(self, emoji):
        """
        Downloads a single emoji from the Discord CDN and saves it to disk.

        Args:
            emoji (dict): The emoji metadata dictionary containing at least 'id', 'name', and optionally 'animated'.

        The method determines the file extension based on whether the emoji is animated,
        constructs the download URL, sanitizes the filename, and saves the file to the appropriate folder.
        """
        ext = 'gif' if emoji.get('animated') else 'png'
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji['id']}.{ext}"
        file_name = self._sanitize_filename(f"{emoji['name']}.{ext}")
        save_path = os.path.join(self.folder, self.servername, "Emojis", file_name)
        self._download_file(emoji_url, save_path)

    def _download_sticker(self, sticker):
        """
        Downloads a single sticker from the Discord CDN and saves it to disk.

        Args:
            sticker (dict): The sticker metadata dictionary containing at least 'id', 'name', and 'format_type'.

        The method determines the file extension and CDN base URL based on the sticker's format type,
        constructs the download URL, sanitizes the filename, and saves the file to the appropriate folder.
        If the sticker is an APNG (format_type == 2), it converts the file to GIF after downloading.
        """
        sticker_id = sticker['id']
        format_type = sticker['format_type']
        ext = 'png' if format_type in (1, 2) else 'gif'
        base_url = "https://media.discordapp.net" if format_type == 4 else "https://cdn.discordapp.com"
        sticker_url = f"{base_url}/stickers/{sticker_id}.{ext}"
        file_name = self._sanitize_filename(f"{sticker['name']}.{ext}")
        save_path = os.path.join(self.folder, self.servername, "Stickers", file_name)
        new_path = self._download_file(sticker_url, save_path)

        if format_type == 2 and new_path:
            self._convert_apng_to_gif(new_path)

    def _download_file(self, url, path):
        """
        Downloads a file from the specified URL and saves it to the given path.

        Args:
            url (str): The URL of the file to download.
            path (str): The local file path where the downloaded file will be saved.

        Returns:
            str: The path to the saved file.

        Raises:
            requests.HTTPError: If the HTTP request returned an unsuccessful status code.
        """
        with requests.get(url, stream=True) as response:
            response.raise_for_status()
            with open(path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
        return path

    def _sanitize_filename(self, name):
        """
        Removes disallowed characters from the provided filename.

        This method uses a translation table to strip out any characters that are not allowed
        in file names on most operating systems, as defined by the DISALLOWED_CHARACTERS list.

        Args:
            name (str): The original filename to sanitize.

        Returns:
            str: The sanitized filename with disallowed characters removed.
        """
        if not hasattr(self, '_translation_table'):
            self._translation_table = str.maketrans('', '', ''.join(DISALLOWED_CHARACTERS))
        return name.translate(self._translation_table)

    def _create_folder(self, folder_type):
        """
        Creates a directory for storing emojis or stickers.

        This method constructs the full path using the base folder, server name, and the specified folder type
        (either "Emojis" or "Stickers"), and ensures that the directory exists. If the directory already exists,
        no error is raised.

        Args:
            folder_type (str): The type of folder to create ("Emojis" or "Stickers").
        """
        os.makedirs(os.path.join(self.folder, self.servername, folder_type), exist_ok=True)

    def _convert_apng_to_gif(self, apng_path):
        """
        Converts an APNG (Animated PNG) file to a GIF format.

        This method opens the provided APNG file, extracts all frames, and saves them as a GIF
        using the imageio library. The duration for each frame is determined from the APNG metadata,
        defaulting to 100ms if not specified. After successful conversion, the original APNG file is deleted.

        Args:
            apng_path (str): The file path to the APNG image to be converted.

        Raises:
            Exception: If an error occurs during the conversion process, an error message is printed.
        """
        try:
            gif_path = apng_path.replace('.png', '.gif')
            with Image.open(apng_path) as img:
                duration = img.info.get('duration', 100) / 1000
                images = [img.copy().convert("RGBA")]
                for _ in range(1, getattr(img, "n_frames", 1)):
                    img.seek(img.tell() + 1)
                    images.append(img.copy().convert("RGBA"))
                imageio.mimsave(gif_path, images, format='GIF', duration=duration)
            os.remove(apng_path)
        except Exception as e:
            print(f"Error converting APNG to GIF: {e}")
