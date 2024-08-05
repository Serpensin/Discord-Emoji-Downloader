import os
import requests
import imageio
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
        self.fetch_guild_data()
        total_count = len(self.data_emoji) + len(self.data_sticker)
        downloaded_count = 0

        if self.data_emoji:
            self.create_folder("Emojis")
            for index, emoji in enumerate(self.data_emoji):
                self.download_emoji(emoji)
                downloaded_count += 1
                self.update_status(f'Downloading {downloaded_count}/{total_count}...')

        if self.data_sticker:
            self.create_folder("Stickers")
            for index, sticker in enumerate(self.data_sticker):
                self.download_sticker(sticker)
                downloaded_count += 1
                self.update_status(f'Downloading {downloaded_count}/{total_count}...')

        return downloaded_count

    def fetch_guild_data(self):
        urls = {
            "guild": f"https://discord.com/api/v6/guilds/{self.guild_id}",
            "emoji": f"https://discord.com/api/v6/guilds/{self.guild_id}/emojis",
            "sticker": f"https://discord.com/api/v6/guilds/{self.guild_id}/stickers"
        }

        for token in self.usertoken:
            headers = {'authorization': token}
            guild_response = requests.get(urls["guild"], headers=headers)
            emoji_response = requests.get(urls["emoji"], headers=headers)
            sticker_response = requests.get(urls["sticker"], headers=headers)

            if guild_response.status_code == 200:
                self.servername = guild_response.json().get('name', '')
                self.data_emoji = emoji_response.json()
                self.data_sticker = sticker_response.json()
                break
            else:
                raise Exception("Missing Access")

        if not self.data_emoji and not self.data_sticker:
            raise Exception("No Emojis or Stickers found")

    def download_emoji(self, emoji):
        emoji_id = emoji['id']
        is_animated = emoji['animated']
        ext = 'gif' if is_animated else 'png'
        emoji_url = f"https://cdn.discordapp.com/emojis/{emoji_id}.{ext}"
        file_name = self.sanitize_filename(f"{emoji['name']}.{ext}")
        save_path = os.path.join(self.folder, self.servername, "Emojis", file_name)
        self.download_file(emoji_url, save_path)

    def download_sticker(self, sticker):
        sticker_id = sticker['id']
        format_type = sticker['format_type']
        ext = 'png' if format_type in [1, 2] else 'gif'
        if format_type == 4:
            sticker_url = f"https://media.discordapp.net/stickers/{sticker_id}.{ext}"
        else:
            sticker_url = f"https://cdn.discordapp.com/stickers/{sticker_id}.{ext}"
        file_name = self.sanitize_filename(f"{sticker['name']}.{ext}")
        save_path = os.path.join(self.folder, self.servername, "Stickers", file_name)
        new_path = self.download_file(sticker_url, save_path)

        if format_type == 2:
            self.convert_apng_to_gif(new_path)

    def download_file(self, url, path):
        response = requests.get(url)
        with open(path, 'wb') as file:
            file.write(response.content)
        return path

    def sanitize_filename(self, name):
        for char in DISALLOWED_CHARACTERS:
            name = name.replace(char, '')
        return name

    def create_folder(self, folder_type):
        os.makedirs(os.path.join(self.folder, self.servername, folder_type), exist_ok=True)

    def convert_apng_to_gif(self, apng_path):
        try:
            gif_path = apng_path.replace('.png', '.gif')
            img = Image.open(apng_path)
            images = []
    
            for frame in range(img.n_frames):
                img.seek(frame)
                images.append(img.convert("RGBA"))
    
            imageio.mimsave(gif_path, images, format='GIF', duration=img.info['duration'] / 1000)
            img.close()
            os.remove(apng_path)
        except Exception as e:
            print(f"Error converting APNG to GIF: {e}")
