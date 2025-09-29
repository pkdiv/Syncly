import os
import hashlib

class File:

    REL = None # To be set by the calling method
    BUFFER_SIZE = 65536
    
    def __init__(self, name, mtime, size):
        self.name = name
        self.size = size
        self.path = self.normalize_rel_path(name) # Store path relative to the sync directory
        self.mtime = mtime
        self.is_dir = os.path.isdir(os.path.join(self.REL, name))
        self.hash = self.compute_hash()

    def __str__(self):
            return (
        f"name: {self.name}\n"
        f"size: {self.size}\n"
        f"path: {self.path}\n"
        f"mtime: {self.mtime}\n"
        f"is_dir: {self.is_dir}\n"
        f"hash: {self.hash}\n"
    )

    def __lt__(self, other):
        return self.name < other.name

    def __eq__(self, other):
        return self.name == other.name 

    def compute_hash(self):

        if not self.is_dir:
            md5 = hashlib.md5()
            with open(os.path.join(File.REL , self.name), 'rb') as file:
                while True:
                    data = file.read(File.BUFFER_SIZE)
                    md5.update(data)
                    if not data:
                        break
        
            return md5.hexdigest()
        
        return None

    
    def normalize_rel_path(self, name):

        normalized_path = 'ABS://' + name
        return normalized_path
    

    def combine_path(self, path):

        combined_path = os.path.join(File.ABS, path)
        return combined_path