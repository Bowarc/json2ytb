from typing import List

class Song:
    def __init__(self, title: str, album: str, artist: List[str]):
        self.title: str = title
        self.album: str= album
        self.artist: List[str] = artist

    def __repr__(self):
        return f"Song(title={self.title}, album={self.album}, artist={self.artist})"
