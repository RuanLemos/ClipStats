import os
from datetime import datetime

class Game:
    def __init__(self, name):
        self.name = name
        self.clips = []

    def add_clip(self, clip):
        self.clips.append(clip)

    def clip_amount(self):
        return len(self.clips)
    
    def folder_size(self):
        size = 0
        for clip in self.clips:
            size += clip.size
        return size

    def __str__(self):
        return f"Game: {self.name} - Clip count: {self.clip_amount()} - Folder size: {self.folder_size()}"
    
class Clip:
    def __init__(self, name, date, size):
        self.name = name
        self.date = date
        self.size = size

    def __str__(self):
        return f"Clip: {self.name} - Size: {self.size}"

def scanFolder(path, all_games):
    cont = 0
    prev_folder = None

    for root, dirs, files in os.walk(path):
        if not files:
            continue

        # Get relpath to see if game changed
        relpath = os.path.relpath(root, path)
        folder = relpath.split(os.sep)[0] if relpath else ''
        
        # Verifying if game folder has changed
        if folder != prev_folder:
            if cont != 0:
                all_games.append(game)
            game = Game(folder)
            #print(f"CURRENTLY SCANNING: {game.name}")
            prev_folder = folder
            cont += 1

        for file in files:
            if file.endswith('mp4'):
                fullpath = os.path.join(root, file)
                filesize = os.path.getsize(fullpath)
                filedate = datetime.fromtimestamp(os.path.getmtime(fullpath)).strftime('%Y.%m.%d - %H.%M.%S')
                
                clip = Clip(file, filedate, filesize)
                game.add_clip(clip)

def convert_size(size):
    if size >= 1e9:
        return f"{size / 1e9:.2f} GB"
    else:
        return f"{size / 1e6:.2f} MB"

all_games = []
total_clips = 0
total_size = 0

scanFolder('D:\clipes', all_games)


for game in all_games:
    print(f"Game: {game.name} - Clips founded: {game.clip_amount()} - Folder size: {convert_size(game.folder_size())}")
    total_clips += game.clip_amount()
    total_size += game.folder_size()
    
print(f"\nTotal amount of clips: {total_clips} - Total clips folder size: {convert_size(total_size)}")