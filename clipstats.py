import os

class Game:
    def __init__(self, name):
        self.name = name
        self.clips = []
        self.size = 0

    def add_clip(self, clip):
        self.clips.append(clip)

    def clip_amount(self):
        return len(self.clips)
    
    def folder_size(self):
        for clip in self.clips:
            self.size += clip.size

    def __str__(self):
        return f"Game: {self.name} - Clip count: {self.clip_amount()} - Folder size: {self.folder_size()}"
    
class Clip:
    def __init__(self, name, date, size):
        self.name = name
        self.date = date
        self.size = size

    def __str__(self):
        return f"Clip: {self.name} - Size: {self.size}"

def scanFolder(path):
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
            game = Game(folder)
            print(game.name)
            prev_folder = folder

        for file in files:
            if file.endswith('mp4'):
                fullpath = os.path.join(root, file)
                filesize = os.path.getsize(fullpath)
                print(f"File name: {file} - File size: {filesize} bytes")
                cont += 1

scanFolder('D:\clipes')
    
